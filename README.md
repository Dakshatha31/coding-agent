# CodePilot — Personal AI Coding Agent

A learning MVP with a tool-calling loop and workspace-limited file tools.

## Safety limitations
- File tools are confined to `workspace/`.
- The agent can read, search, and write workspace files.
- Python syntax checking uses AST parsing and does not execute the file.
- There is no unrestricted terminal tool or automatic test execution.
- Review generated files before manually running them.

## Setup (Windows PowerShell)

1. Install Python 3.11+.
2. Open this folder in PowerShell.
3. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and insert your API key.

6. Start:

   ```powershell
   streamlit run main.py
   ```

## Tools
- `list_files`
- `read_file`
- `write_file`
- `search_files`
- `check_python_syntax`

## Project layout
- `agent.py`: iterative model/tool controller
- `tools/`: restricted tools and dispatch
- `workspace/`: files the agent can access
- `main.py`: Streamlit interface
