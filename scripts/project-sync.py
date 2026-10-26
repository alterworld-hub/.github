#!/usr/bin/env python3
"""Keep the org project consistent. Idempotent; safe to run any time.

Board holds issues only; PRs are visible on their issues (Linked pull requests).

1. Add open issues of the org that are not in the project.
2. Area empty -> set from repository (AREA_BY_REPO, else option named like the repo).
3. Phase empty -> inherit from parent issue.
4. Open issue in Backlog/Next with an open PR closing it -> In progress.
5. Open Epic whose sub-issues are all closed -> close it.
6. No Status -> Backlog.
7. Closed/merged issue or PR not in Done -> Done.
Rules 6-7 replace the built-in project workflows (not configurable via API).

Env: GH_TOKEN, ORG, PROJECT_NUMBER, DRY_RUN=1 to only print.
"""
import json
import os
import subprocess
import sys

ORG = os.environ.get("ORG", "alterworld-hub")
NUMBER = int(os.environ.get("PROJECT_NUMBER", "2"))
DRY = os.environ.get("DRY_RUN") == "1"
AREA_BY_REPO = {".github": "ci", "gitops": "gitops", "frontend": "frontend"}


def gql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    res = subprocess.run(args, capture_output=True, text=True)
    data = json.loads(res.stdout or "{}")
    if res.returncode or data.get("errors"):
        sys.exit(f"graphql error: {res.stdout}{res.stderr}")
    return data["data"]


def act(msg, fn, *a):
    print(("DRY " if DRY else "") + msg)
    if not DRY:
        fn(*a)


project = gql("""query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id
  fields(first:30){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}""", o=ORG, n=NUMBER)["organization"]["projectV2"]
PID = project["id"]
FIELDS = {f["name"]: (f["id"], {o["name"]: o["id"] for o in f["options"]}) for f in project["fields"]["nodes"] if f}

ITEMS_Q = """query($p:ID!,$c:String){node(id:$p){... on ProjectV2{items(first:100,after:$c){
  pageInfo{hasNextPage endCursor}
  nodes{id
    fieldValues(first:20){nodes{... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2SingleSelectField{name}}}}}
    content{__typename
      ... on Issue{id number state repository{name} issueType{name}
        parent{id} subIssuesSummary{total completed}}
      ... on PullRequest{id number state repository{name}
        closingIssuesReferences(first:10){nodes{id}}}}}}}}}"""


def load_items():
    items, cursor = [], None
    while True:
        args = {"p": PID}
        if cursor:
            args["c"] = cursor
        page = gql(ITEMS_Q, **args)["node"]["items"]
        items += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return items
        cursor = page["pageInfo"]["endCursor"]


def values(item):
    return {v["field"]["name"]: v["name"] for v in item["fieldValues"]["nodes"] if v and v.get("field")}


def set_field(item_id, field, option):
    fid, opts = FIELDS[field]
    gql("""mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:
      {projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}}""",
        p=PID, i=item_id, f=fid, o=opts[option])


def add(content_id):
    gql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}", p=PID, c=content_id)


def close(issue_id):
    gql("mutation($i:ID!){closeIssue(input:{issueId:$i,stateReason:COMPLETED}){issue{id}}}", i=issue_id)


# 1. missing open issues/PRs
missing = gql("""query($q:String!){search(query:$q,type:ISSUE,first:100){nodes{
  ... on Issue{id number repository{name}}}}}""",
              q=f"org:{ORG} is:issue is:open -project:{ORG}/{NUMBER}")["search"]["nodes"]
for c in missing:
    if c:
        act(f"add {c['repository']['name']}#{c['number']}", add, c["id"])

items = load_items()
by_content = {i["content"]["id"]: i for i in items if i.get("content") and "id" in i["content"]}
prs = gql("""query($q:String!){search(query:$q,type:ISSUE,first:100){nodes{
  ... on PullRequest{closingIssuesReferences(first:10){nodes{id}}}}}}""", q=f"org:{ORG} is:pr is:open")["search"]["nodes"]
closing = {iss["id"] for pr in prs if pr for iss in pr["closingIssuesReferences"]["nodes"]}

for item in items:
    c = item.get("content")
    if not c or "repository" not in c:
        continue
    ref = f"{c['repository']['name']}#{c['number']}"
    v = values(item)

    # 2. Area from repository
    if "Area" not in v:
        repo = c["repository"]["name"]
        area = AREA_BY_REPO.get(repo, repo)
        if area in FIELDS["Area"][1]:
            act(f"{ref}: Area={area}", set_field, item["id"], "Area", area)

    # 6-7. Status lifecycle
    if c["state"] in ("CLOSED", "MERGED"):
        if v.get("Status") != "Done":
            act(f"{ref}: Status=Done ({c['state'].lower()})", set_field, item["id"], "Status", "Done")
        continue
    if "Status" not in v:
        act(f"{ref}: Status=Backlog", set_field, item["id"], "Status", "Backlog")
        v["Status"] = "Backlog"

    if c["__typename"] != "Issue":
        continue

    # 3. Phase from parent
    parent = c.get("parent")
    if "Phase" not in v and parent and parent["id"] in by_content:
        phase = values(by_content[parent["id"]]).get("Phase")
        if phase:
            act(f"{ref}: Phase={phase} (from parent)", set_field, item["id"], "Phase", phase)

    # 4. open PR closes it -> In progress
    if c["state"] == "OPEN" and c["id"] in closing and v.get("Status") in (None, "Backlog", "Next"):
        act(f"{ref}: Status=In progress (open PR)", set_field, item["id"], "Status", "In progress")

    # 5. Epic with all sub-issues done -> close
    s = c["subIssuesSummary"]
    if (c["state"] == "OPEN" and (c.get("issueType") or {}).get("name") == "Epic"
            and s["total"] and s["completed"] == s["total"]):
        act(f"{ref}: close epic ({s['completed']}/{s['total']} done)", close, c["id"])

print(f"checked {len(items)} items")
