from tools.files import list_files,read_file,write_file,search_files,check_python_syntax

TOOL_SPECS=[
 {"type":"function","function":{"name":"list_files","description":"List entries in a workspace directory.","parameters":{"type":"object","properties":{"path":{"type":"string","description":"Relative directory path, or ."}},"required":["path"]}}},
 {"type":"function","function":{"name":"read_file","description":"Read a UTF-8 text file within the workspace.","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
 {"type":"function","function":{"name":"write_file","description":"Create or overwrite a workspace text file. Keep changes relevant.","parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
 {"type":"function","function":{"name":"search_files","description":"Search text within workspace files.","parameters":{"type":"object","properties":{"query":{"type":"string"},"pattern":{"type":"string","description":"Glob pattern, such as *.py"}},"required":["query"]}}},
 {"type":"function","function":{"name":"check_python_syntax","description":"Parse a Python file to check syntax. Does not execute it.","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}}
]
DISPATCH={"list_files":list_files,"read_file":read_file,"write_file":write_file,"search_files":search_files,"check_python_syntax":check_python_syntax}

def execute_tool(name,args):
    if name not in DISPATCH:
        return {"error":"Tool not allowed."}
    return DISPATCH[name](args)
