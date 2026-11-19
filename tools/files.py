from pathlib import Path
import ast
import re
from config import WORKSPACE, MAX_FILE_BYTES

def safe_path(rel):
    if not isinstance(rel,str) or not rel.strip():
        raise ValueError("A non-empty relative path is required.")
    p=(WORKSPACE/rel).resolve()
    if p != WORKSPACE and WORKSPACE not in p.parents:
        raise ValueError("Path is outside the workspace.")
    return p

def list_files(args):
    path=safe_path(args.get("path","."))
    if not path.exists() or not path.is_dir():
        return {"error":"Directory not found."}
    entries=[]
    for p in sorted(path.iterdir()):
        if p.name.startswith(".") or p.name=="__pycache__":
            continue
        entries.append({"name":p.name,"type":"directory" if p.is_dir() else "file"})
    return {"path":str(path.relative_to(WORKSPACE)) if path!=WORKSPACE else ".","entries":entries[:200]}

def read_file(args):
    path=safe_path(args.get("path"))
    if not path.exists() or not path.is_file():
        return {"error":"File not found."}
    if path.stat().st_size>MAX_FILE_BYTES:
        return {"error":"File is too large to read through this tool."}
    return {"path":str(path.relative_to(WORKSPACE)),"content":path.read_text(encoding="utf-8",errors="replace")}

def write_file(args):
    path=safe_path(args.get("path"))
    content=args.get("content")
    if not isinstance(content,str):
        raise ValueError("content must be a string")
    if len(content.encode("utf-8"))>MAX_FILE_BYTES:
        raise ValueError("File exceeds size limit.")
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.is_dir():
        raise ValueError("Path points to a directory.")
    path.write_text(content,encoding="utf-8")
    return {"ok":True,"path":str(path.relative_to(WORKSPACE)),"bytes":len(content.encode("utf-8"))}

def search_files(args):
    query=args.get("query")
    if not isinstance(query,str) or not query:
        raise ValueError("query must be non-empty")
    pattern=args.get("pattern","*")
    matches=[]
    for p in WORKSPACE.rglob(pattern):
        if not p.is_file() or any(part.startswith(".") or part=="__pycache__" for part in p.parts):
            continue
        try:
            if p.stat().st_size>MAX_FILE_BYTES: continue
            lines=p.read_text(encoding="utf-8",errors="replace").splitlines()
            for n,line in enumerate(lines,1):
                if query.lower() in line.lower():
                    matches.append({"file":str(p.relative_to(WORKSPACE)),"line":n,"text":line[:300]})
                    if len(matches)>=100: return {"matches":matches}
        except OSError:
            pass
    return {"matches":matches}

def check_python_syntax(args):
    path=safe_path(args.get("path"))
    if not path.exists() or not path.is_file() or path.suffix!=".py":
        return {"error":"Expected an existing Python file inside the workspace."}
    if path.stat().st_size>MAX_FILE_BYTES:
        return {"error":"File too large."}
    source=path.read_text(encoding="utf-8",errors="replace")
    try:
        ast.parse(source,filename=str(path))
        return {"ok":True,"message":"Python syntax is valid. This did not execute the code."}
    except SyntaxError as e:
        return {"ok":False,"error":e.msg,"line":e.lineno,"offset":e.offset}
