"""Offline checks for the Mintlify repo: MDX-unsafe characters, broken internal
links and images, docs.json pages that don't exist, and orphan pages."""
import glob, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_TAGS = {"Frame", "img", "CardGroup", "Card", "Note", "Tip", "Warning", "Info"}
problems = []


def walk_pages(items, acc):
    for it in items:
        if isinstance(it, str):
            acc.append(it)
        elif "pages" in it:
            walk_pages(it["pages"], acc)
        elif "groups" in it:
            walk_pages(it["groups"], acc)
    return acc


docs = json.load(open(os.path.join(REPO, "docs.json")))
nav_pages = []
for tab in docs["navigation"]["tabs"]:
    walk_pages(tab["groups"], nav_pages)
for p in nav_pages:
    if not os.path.exists(os.path.join(REPO, p + ".mdx")):
        problems.append(f"docs.json: missing page {p}")
files = sorted(glob.glob(os.path.join(REPO, "**/*.mdx"), recursive=True))
rel = {os.path.relpath(f, REPO)[:-4] for f in files}
for orphan in rel - set(nav_pages):
    problems.append(f"orphan page not in navigation: {orphan}")
if len(nav_pages) != len(set(nav_pages)):
    problems.append("docs.json lists a page twice")

for f in files:
    name = os.path.relpath(f, REPO)
    text = open(f).read()
    if not text.startswith("---\n"):
        problems.append(f"{name}: no frontmatter")
    fm, body = text.split("---\n", 2)[1:] if text.count("---\n") >= 2 else ("", text)
    for ln in fm.splitlines():
        k, _, v = ln.partition(":")
        v = v.strip()
        if v.startswith('"') and (not v.endswith('"') or '"' in v[1:-1]):
            problems.append(f"{name}: bad frontmatter quoting: {ln[:80]}")
    in_code = False
    for n, ln in enumerate(body.splitlines(), 1):
        if ln.startswith("```"):
            in_code = not in_code
            continue
        if in_code or ln.strip().startswith("{/*"):
            continue
        plain = re.sub(r"`[^`]*`", "", ln)
        if re.search(r"(?<!\\)[{}]", re.sub(r"cols=\{\d+\}", "", plain)):
            problems.append(f"{name}:{n}: unescaped brace: {ln[:100]}")
        for tag in re.findall(r"<\/?([A-Za-z][A-Za-z0-9]*)", plain):
            if tag not in ALLOWED_TAGS:
                problems.append(f"{name}:{n}: unexpected tag <{tag}>: {ln[:100]}")
        for target in re.findall(r"\]\((/[^)\s#]*)", plain):
            if target != "/" and target.strip("/") not in rel:
                problems.append(f"{name}:{n}: broken link {target}")
        for src in re.findall(r'src="(/[^"]+)"', ln) + re.findall(r'href="(/[^"]+)"', ln):
            path = os.path.join(REPO, src.lstrip("/"))
            if not (os.path.exists(path) or src.strip("/") in rel):
                problems.append(f"{name}:{n}: missing file {src}")
    if body.count("<Frame>") != body.count("</Frame>"):
        problems.append(f"{name}: unbalanced <Frame>")

print("\n".join(problems) or "OK: no problems")
print(f"{len(files)} pages, {len(nav_pages)} in navigation")
sys.exit(1 if problems else 0)
