# AGENTS — Project overview (ai-crew-engineering-team)

This document is a **contributor-oriented map** of this repo: where things live, what each module does, and the common dev/run commands.

---

## Repository layout

```
ai-crew-engineering-team/
├── README.md
├── AGENTS.md                 # This file
├── .gitignore
├── .python-version
├── pyproject.toml            # Root workspace config (if any)
├── uv.lock
├── docs/
│   ├── architecture.md       # Flow diagrams, pipelines, run options
│   ├── demo.md               # How to run, console output, pipeline walkthrough
│   └── developers_guide.md   # How to modify agents, tasks, extend the crew
└── src/engineering_team/     # CrewAI project root
    ├── pyproject.toml        # CrewAI project config + dependencies
    ├── uv.lock
    ├── src/engineering_team/ # Python package
    │   ├── main.py           # Entrypoint: run crew
    │   ├── crew.py           # Crew definition (agents, tasks, process)
    │   ├── config/
    │   │   ├── agents.yaml   # Agent roles, goals, backstories, LLMs
    │   │   └── tasks.yaml    # Task descriptions, expected outputs, context
    │   └── tools/
    │       └── custom_tool.py # Template for custom tools (not used by default)
    └── output/               # Generated design, module, app, tests
        ├── {module_name}_design.md
        ├── {module_name}     # e.g. accounts.py
        ├── app.py
        └── test_{module_name}
```

Notes:

- The **CrewAI project** lives under `src/engineering_team/`. Run `crewai run` from that directory.
- The package is installable via `pip install -e .` or `uv sync` inside `src/engineering_team/`.
- Generated files appear under `src/engineering_team/output/` after a run.

---

## Key components (where to start reading)

- **Entrypoint (run crew)**: `src/engineering_team/src/engineering_team/main.py`
  - Sets `inputs = {'requirements': ..., 'module_name': 'accounts.py', 'class_name': 'Account'}` (customize here)
  - Instantiates `EngineeringTeam().crew()` and calls `kickoff(inputs=inputs)`
  - Creates `output/` directory; crew writes design, backend module, Gradio `app.py`, and tests

- **Crew definition**: `src/engineering_team/src/engineering_team/crew.py`
  - `EngineeringTeam` (with `@CrewBase`): defines agents and tasks via decorators
  - **Agents**: `engineering_lead`, `backend_engineer` (Code Interpreter), `frontend_engineer`, `test_engineer` (Code Interpreter)
  - **Tasks**: `design_task` → `code_task` (context: design) → `frontend_task`, `test_task` (context: code_task)
  - **Process**: `Process.sequential`

- **Agent config**: `src/engineering_team/src/engineering_team/config/agents.yaml`
  - `engineering_lead`: role, goal, backstory, LLM `gpt-4o`
  - `backend_engineer`: role, goal, backstory, LLM `openai/gpt-4o-mini`, `allow_code_execution=True`
  - `frontend_engineer`: role, goal, backstory, LLM `openai/gpt-4o-mini`
  - `test_engineer`: role, goal, backstory, LLM `openai/gpt-4o-mini`, `allow_code_execution=True`
  - Placeholders like `{requirements}`, `{module_name}`, `{class_name}` are filled from `kickoff(inputs=...)`

- **Task config**: `src/engineering_team/src/engineering_team/config/tasks.yaml`
  - `design_task`: description, expected output, assigned to `engineering_lead`, `output_file: output/{module_name}_design.md`
  - `code_task`: description, expected output, assigned to `backend_engineer`, `context: [design_task]`, `output_file: output/{module_name}`
  - `frontend_task`: description, expected output, assigned to `frontend_engineer`, `context: [code_task]`, `output_file: output/app.py`
  - `test_task`: description, expected output, assigned to `test_engineer`, `context: [code_task]`, `output_file: output/test_{module_name}`

- **Custom tools**: `src/engineering_team/src/engineering_team/tools/custom_tool.py`
  - `MyCustomTool` template; extend for new agent capabilities
  - Not used by default; agents use Code Interpreter instead. Attach in `crew.py` if needed.

---

## Configuration & environment variables

Create a `.env` in the project root (or `src/engineering_team/`) or export vars. Required keys:

| Variable         | Used by    | Purpose                                |
|------------------|------------|----------------------------------------|
| `OPENAI_API_KEY` | All agents | LLMs (gpt-4o, gpt-4o-mini)             |

Docker must be installed and running for the Backend Engineer and Test Engineer (Code Interpreter uses Docker sandbox).

Example:

```bash
export OPENAI_API_KEY="sk-..."
```

---

## Running locally

### Install dependencies

From `src/engineering_team/`:

```bash
uv sync
# or: crewai install
# or: pip install -e .
```

### Run the crew (recommended)

From `src/engineering_team/`:

```bash
crewai run
```

### Run via Python

```bash
cd src/engineering_team
uv run engineering_team
```

Or, after install:

```bash
engineering_team
```

### Change inputs (requirements, module, class)

Edit `main.py` in `src/engineering_team/src/engineering_team/main.py`:

```python
requirements = """Your natural language requirements here..."""
module_name = "accounts.py"
class_name = "Account"
```

### Run the generated app

After the crew completes:

```bash
cd src/engineering_team/output
uv run app.py
```

### Run tests

```bash
cd src/engineering_team/output
uv run pytest test_accounts.py -v
```

---

## Common pitfalls

- **`crewai run` fails / wrong directory**: Run from `src/engineering_team/`, not the repo root. CrewAI expects the project root (where `pyproject.toml` has `[tool.crewai]`) as the working directory.

- **`ModuleNotFoundError` / missing package**: Install inside `src/engineering_team/` with `uv sync` or `pip install -e .`. Use `uv run ...` or the project's venv when running Python scripts.

- **Missing API keys**: Ensure `OPENAI_API_KEY` is set in `.env` or the environment.

- **Code Interpreter / Docker errors**: The Backend Engineer and Test Engineer use Code Interpreter (runs in Docker). Docker must be installed and running. On macOS with Docker Desktop, the project sets `DOCKER_HOST` automatically if needed.

- **Output files not found**: Generated files are written to `output/` relative to the CrewAI project root (`src/engineering_team/`). Paths from repo root: `src/engineering_team/output/{module_name}_design.md`, `src/engineering_team/output/accounts.py`, `src/engineering_team/output/app.py`, `src/engineering_team/output/test_accounts.py`.
