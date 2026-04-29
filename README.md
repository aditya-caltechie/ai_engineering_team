# AI Engineering Team

[![CI](https://github.com/aditya-caltechie/ai_engineering_team/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aditya-caltechie/ai_engineering_team/actions/workflows/ci.yml)

An AI-powered engineering crew that turns **natural language requirements** into:
- a short design document
- a Python backend module
- a Gradio demo UI
- unit tests

Built with [CrewAI](https://crewai.com/) and orchestrated as a **sequential, multi-agent** pipeline. Agents that execute code run inside **Docker** for isolation.

---

## What it generates

Given:
- **requirements**: what you want to build (plain English)
- **module_name**: e.g. `accounts.py`
- **class_name**: e.g. `Account`

The crew writes the following under `src/engineering_team/output/`:
- `{module_name}_design.md`
- `{module_name}`
- `app.py`
- `test_{module_name}`

---

## Architecture (high-level)

```mermaid
flowchart LR
    subgraph Inputs
        REQ[Requirements]
        MOD[module_name]
        CLS[class_name]
    end

    subgraph Crew["Crew (Sequential)"]
        A1[Engineering Lead: Design]
        A2[Backend Engineer: Implement]
        A3[Frontend Engineer: UI]
        A4[Test Engineer: Tests]
    end

    subgraph Outputs
        O1[{module}_design.md]
        O2[{module}.py]
        O3[app.py]
        O4[test_{module}.py]
    end

    Inputs --> A1
    A1 --> A2
    A2 --> A3
    A2 --> A4
    A1 --> O1
    A2 --> O2
    A3 --> O3
    A4 --> O4
```

---

## Quick Start
### Prerequisites

- Python **3.10–3.12**
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (required for agents that execute code)
- An LLM API key in your environment (for example `OPENAI_API_KEY`)

### Install dependencies

From the CrewAI project root:

```bash
cd src/engineering_team
uv sync
```

### Configure environment

Set your API key (shell) or put it in a `.env` file.

```bash
export OPENAI_API_KEY="..."
```

### Run

```bash
cd src/engineering_team
crewai run
```

---

## Configuration

### Customize the generated module

Edit `src/engineering_team/src/engineering_team/main.py`:
- **`requirements`**: natural language spec
- **`module_name`**: e.g. `accounts.py`
- **`class_name`**: e.g. `Account`

### Where agents and tasks are defined

- **Agents**: `src/engineering_team/src/engineering_team/config/agents.yaml`
- **Tasks**: `src/engineering_team/src/engineering_team/config/tasks.yaml`
- **Crew assembly**: `src/engineering_team/src/engineering_team/crew.py`

---

## Outputs

After a successful run, generated artifacts are written to:

`src/engineering_team/output/`

Typical files:
- **Design**: `{module_name}_design.md`
- **Backend module**: `{module_name}`
- **Gradio UI**: `app.py`
- **Unit tests**: `test_{module_name}`

Run the app:

```bash
cd src/engineering_team/output
uv run app.py
```

Run tests:

```bash
cd src/engineering_team/output
uv run pytest test_accounts.py -v
```

---

## Project Structure

```
ai_engineering_team/
├── src/engineering_team/
│   ├── src/engineering_team/
│   │   ├── config/                 # agents.yaml, tasks.yaml
│   │   ├── crew.py                 # Crew definition
│   │   └── main.py                 # Entry point & inputs
│   └── output/                     # Generated design, module, app, tests
└── docs/
    ├── architecture.md             # More detailed diagrams/notes
    └── developers_guide.md         # How to extend the crew
```

---

## Troubleshooting

- **Docker errors / code execution fails**: ensure Docker Desktop is installed and running. The Backend and Test agents execute code in Docker for isolation.
- **Missing API key**: set `OPENAI_API_KEY` (or the provider key you configured in `agents.yaml`).
- **Run fails from repo root**: run from `src/engineering_team/` (this is the CrewAI project root).

---

## Documentation

- `AGENTS.md`: contributor-oriented map of the repo
- `docs/architecture.md`: more detailed diagrams and run options
- `docs/developers_guide.md`: how to extend agents/tasks and customize the crew

