#!/usr/bin/env python3
"""Read-only catalog audit. Findings marked review require human verification."""
import argparse, collections, hashlib, html, itertools, json, re
from pathlib import Path
from urllib.parse import unquote
import yaml

class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader, node):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=True)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(v, deep=True)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
RULES = {
    "commit": r"\bgit\s+commit\b|\bcommit (?:the|your|all) changes\b",
    "push": r"\bgit\s+push\b",
    "install": r"\b(?:pip|npm|pnpm|apt|brew)\s+install\b",
    "destructive": r"\brm\s+-[a-z]*r[a-z]*f\b|shutil\.rmtree|git\s+reset\s+--hard",
    "privilege": r"\bsudo\s+",
    "pipe-shell": r"\|\s*(?:bash|sh)\b",
    "deploy": r"\b(?:vercel\s+--prod|railway\s+up|kubectl\s+apply)\b",
    "network": r"https?://|\b(?:curl|wget)\s+",
    "secret": r"\b(?:api[_ -]?key|access[_ -]?token|password|\.env)\b",
}
COVERAGE = {
    "Flutter/Dart": ["flutter", "dart"], "Next.js": ["next.js", "nextjs", "app router"],
    "PostgreSQL": ["postgresql", "postgres"], "Supabase": ["supabase", "row level security"],
    "Railway": ["railway"], "Vercel": ["vercel"], "MikroTik": ["mikrotik", "routeros"],
    "WhatsApp": ["whatsapp"], "Telegram": ["telegram"], "RTL": ["rtl", "right-to-left"],
    "Multi-tenancy": ["multi-tenant", "tenant isolation"], "Financial ledger": ["double-entry", "financial ledger"],
    "Testing": ["playwright", "vitest", "integration testing"], "Observability": ["opentelemetry", "observability"],
    "PWA": ["pwa", "service worker"], "Yemeni wallets": ["yemeni wallet", "جيب", "جوالي"],
}
def read(p):
    if p.stat().st_size > 5_000_000:
        raise ValueError("file exceeds 5 MB limit")
    return p.read_text(encoding="utf-8")

def audit(root, threshold=.55):
    root = root.resolve()
    findings, skills, bodies = [], [], {}
    hashes, names = collections.defaultdict(list), collections.defaultdict(list)
    directives = collections.defaultdict(lambda: {"allow": set(), "deny": set()})
    def add(kind, path, detail, severity="medium", confidence="confirmed", line=None):
        findings.append(dict(kind=kind,path=str(path),detail=detail,severity=severity,confidence=confidence,line=line))
    def rel(p):
        return p.relative_to(root).as_posix()
    paths = []
    for p in sorted(root.rglob("*")):
        parts = p.relative_to(root).parts
        if any(x in {".git", ".venv", "__pycache__", "node_modules"} for x in parts) or parts[:2] == ("tools", "kayan-auditor"):
            continue
        if p.is_symlink():
            add("symlink", rel(p), "Symlink not followed", "high")
        elif p.is_file() and p.resolve().is_relative_to(root):
            paths.append(p)
    for p in (p for p in paths if p.name == "SKILL.md"):
        sid = rel(p)
        rec = dict(path=sid,name=None,description="",license=None,license_files=[],source_urls=[],dependencies=[],status="ok")
        skills.append(rec)
        try:
            raw = read(p)
            hashes[hashlib.sha256(p.read_bytes()).hexdigest()].append(sid)
        except (OSError, UnicodeError, ValueError) as e:
            rec["status"] = "unreadable"
            add("read",sid,str(e),"high")
            continue
        meta, body = {}, raw
        m = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)",raw,re.S)
        try:
            if not m:
                raise ValueError("Missing YAML frontmatter")
            body = raw[m.end():]
            meta = yaml.load(m[1],Loader=UniqueLoader) or {}
            if not isinstance(meta,dict):
                raise ValueError("metadata must be mapping")
        except (yaml.YAMLError, ValueError, TypeError, RecursionError) as e:
            add("frontmatter",sid,str(e),"high")
            meta = {}
        for field in ("name","description"):
            v = meta.get(field)
            if not isinstance(v,str) or not v.strip():
                add("metadata",sid,f"Missing or invalid {field}","high")
            else:
                rec[field] = v
        if rec["name"]:
            names[rec["name"].casefold()].append(sid)
        rec["license"] = str(meta["license"]) if meta.get("license") else None
        for parent in p.parents:
            if not parent.is_relative_to(root):
                break
            rec["license_files"].extend(rel(f) for f in sorted(parent.iterdir()) if f.is_file() and not f.is_symlink() and re.match(r"^(LICENSE|COPYING|NOTICE)(\.|$)",f.name,re.I))
        if not rec["license"]:
            add("license",sid,"No explicit skill license; inherited files do not establish upstream rights",confidence="review")
        rec["source_urls"] = sorted(set(re.findall(r'https?://[^\s<>\])"\x60]+',raw)))
        if not rec["source_urls"]:
            add("source",sid,"No URL in skill; check manifest","low","review")
        for i,line in enumerate(raw.splitlines(),1):
            for rule,pat in RULES.items():
                if re.search(pat,line,re.I):
                    rec["dependencies"].append(rule)
                    if rule not in ("network","secret"):
                        add("policy-review",sid,rule,"high" if rule in ("destructive","privilege","pipe-shell") else "medium","review",i)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",line):
                target = unquote(target.split("#")[0].strip().strip("<>"))
                if not target or re.match(r"^[a-z]+:",target,re.I) or any(c in target for c in "{}"):
                    continue
                q = p.parent / target
                if not q.resolve().is_relative_to(root):
                    add("external-path",sid,target,"high",line=i)
                elif not q.exists():
                    add("broken-link",sid,target,line=i)
            for action in ("commit","push","install","deploy","delete","upload"):
                if re.search(r"\b(?:never|do not|must not)\b.{0,45}\b"+action+r"\b",line,re.I):
                    directives[action]["deny"].add(sid)
                elif re.search(r"\b(?:must|always|required to)\b.{0,45}\b"+action+r"\b",line,re.I):
                    directives[action]["allow"].add(sid)
        rec["dependencies"] = sorted(set(rec["dependencies"]))
        rec["lines"] = len(raw.splitlines())
        if rec["lines"] > 500:
            add("length",sid,"Over 500 lines","low")
        bodies[sid] = body
    for kind, groups in (("exact-duplicate",hashes),("duplicate-name",names)):
        for ids in groups.values():
            if len(ids)>1:
                add(kind,ids[0]," | ".join(ids))
    sets = {}
    for sid,body in bodies.items():
        t = re.findall(r"\w+",body.casefold())
        sets[sid] = set(zip(t,t[1:],t[2:]))
    for a,b in itertools.combinations(sets,2):
        x,y = sets[a],sets[b]
        if x and y and bodies[a]!=bodies[b]:
            score = len(x&y)/len(x|y)
            if score>=threshold:
                add("text-overlap",a,f"{b}: Jaccard={score:.3f}",confidence="review")
    for action,d in directives.items():
        if d["allow"] and d["deny"]:
            add("potential-conflict","catalog",f'{action}: positive={sorted(d["allow"])}; negative={sorted(d["deny"])}',confidence="review")
    try:
        p = root/"registry/SKILLS_REGISTRY.json"
        if p.is_symlink() or not p.resolve().is_relative_to(root):
            raise ValueError("unsafe registry path")
        registered = [x["path"] for x in json.loads(read(p))["skills"]]
        actual = {s["path"] for s in skills}
        for x in sorted(actual-set(registered)):
            add("registry-missing",x,"Not registered","high")
        for x in sorted(set(registered)-actual):
            add("registry-stale",x,"No matching skill","high")
        for x,n in collections.Counter(registered).items():
            if n>1:
                add("registry-duplicate",x,f"{n} entries")
    except (OSError,ValueError,KeyError,TypeError) as e:
        add("registry","catalog",str(e),"high")
    try:
        p = root/"registry/SOURCES_MANIFEST.json"
        if p.is_symlink() or not p.resolve().is_relative_to(root):
            raise ValueError("unsafe manifest path")
        def walk(x,loc="manifest"):
            if isinstance(x,dict):
                for k,v in x.items():
                    if re.search(r"license|commit|revision|sha|tag",k,re.I) and (v is None or str(v).strip().lower() in ("","unknown","pending","unverified","noassertion")):
                        add("provenance",loc+"."+k,"Unresolved source metadata",confidence="review")
                    walk(v,loc+"."+k)
            elif isinstance(x,list):
                for i,v in enumerate(x):
                    walk(v,f"{loc}[{i}]")
        walk(json.loads(read(p)))
    except (OSError,ValueError,RecursionError) as e:
        add("manifest","catalog",str(e),"high")
    scanned = 0
    for p in paths:
        if p.suffix.lower() not in (".py",".sh",".js",".ts",".ps1",".bat",".rb",".yml",".yaml") and "scripts" not in p.relative_to(root).parts:
            continue
        try:
            content = read(p)
        except (OSError,UnicodeError,ValueError) as e:
            add("support-read",rel(p),str(e),"low")
            continue
        scanned += 1
        for i,line in enumerate(content.splitlines(),1):
            for rule in ("destructive","privilege","pipe-shell"):
                if re.search(RULES[rule],line,re.I):
                    add("script-risk",rel(p),rule,"high","review",i)
    coverage = {k:[sid for sid,body in bodies.items() if any(t.casefold() in (sid+" "+body).casefold() for t in terms)] for k,terms in COVERAGE.items()}
    return dict(schema_version=1,skill_count=len(skills),read_count=len(bodies),support_files_scanned=scanned,threshold=threshold,skills=skills,findings=findings,coverage_keyword_hits=coverage,summary=dict(collections.Counter(f["severity"] for f in findings)))

def reports(result,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/"audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    title = f"Kayan Skill Auditor — {result['read_count']}/{result['skill_count']} skills read"
    fields = ("severity","confidence","kind","path","line","detail")
    skillfields = ("path","name","license","license_files","dependencies","status")
    def md(v):
        return str(v if v is not None else "").replace("|",r"\|").replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
    def mdtable(items,keys):
        return ["| "+" | ".join(keys)+" |","| "+" | ".join("---" for _ in keys)+" |"]+["| "+" | ".join(md(x.get(k)) for k in keys)+" |" for x in items]
    coverage = [dict(topic=k,matches=len(v),paths=v) for k,v in result["coverage_keyword_hits"].items()]
    rows = ["# "+title,"","Review candidates are not confirmed conflicts or license violations.","","## Findings",*mdtable(result["findings"],fields),"","## Skills",*mdtable(result["skills"],skillfields),"","## Coverage (keyword evidence only)",*mdtable(coverage,("topic","matches","paths"))]
    (out/"audit.md").write_text("\n".join(rows)+"\n",encoding="utf-8")
    def esc(v):
        return html.escape(str(v if v is not None else ""))
    def table(items,keys):
        return "<section><table><thead><tr>"+"".join("<th>"+esc(k)+"</th>" for k in keys)+"</tr></thead><tbody>"+"".join("<tr>"+"".join("<td>"+esc(x.get(k))+"</td>" for k in keys)+"</tr>" for x in items)+"</tbody></table></section>"
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+esc(title)+'</title><style>body{font:15px system-ui;margin:2rem;color:#172334}table{border-collapse:collapse;width:100%}td,th{padding:8px;border:1px solid #d4dce5;text-align:start;overflow-wrap:anywhere}th{background:#edf2f7}section{overflow:auto}</style><h1>'+esc(title)+'</h1><p>Static analysis; review candidates require human verification.</p><h2>Findings</h2>'+table(result["findings"],fields)+'<h2>Skills</h2>'+table(result["skills"],skillfields)+'<h2>Coverage</h2>'+table(coverage,("topic","matches","paths"))+'</html>'
    (out/"audit.html").write_text(page,encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root",type=Path)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--threshold",type=float,default=.55)
    parser.add_argument("--fail-on-high",action="store_true")
    a = parser.parse_args()
    root,out = a.root.resolve(),a.out.resolve()
    if not root.is_dir() or out.is_relative_to(root) or not 0<a.threshold<=1:
        parser.error("valid root, output outside repository, threshold in (0,1] required")
    result = audit(root,a.threshold)
    reports(result,out)
    print(f"Read {result['read_count']}/{result['skill_count']} skills; {len(result['findings'])} findings")
    if not result["skill_count"] or result["read_count"]!=result["skill_count"]:
        return 2
    return int(a.fail_on_high and any(f["severity"]=="high" and f["confidence"]=="confirmed" for f in result["findings"]))

if __name__=="__main__":
    raise SystemExit(main())
