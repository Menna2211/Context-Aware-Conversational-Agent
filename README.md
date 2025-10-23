# Context-Aware Conversational Agent

A small research/demo project that builds a context-aware conversational agent. The agent inspects user messages for contextual information, evaluates relevance, and—when needed—performs web searches to enrich responses. This repository includes the agent implementation, a Gradio-based UI, and small tools for context-splitting, relevance checking, and web search.

## Quick overview

- Language: Python
- Purpose: demo a conversation agent that is aware of and uses provided context
- UI: Gradio interface at `ui/gradio_ui.py`

## Features

- Detects whether user input includes context
- Splits longer context into chunks when necessary
- Checks context relevance to the user query
- Performs a web search when the agent lacks sufficient context
- Gradio UI with chat-like experience and typing animation

## Repo layout

- `main.py` — simple CLI/demo runner that builds the agent and runs example queries
- `agents/` — agent construction and runner code
- `tools/` — helper tools: context presence/judge, relevance checker, splitter, web search
- `prompts/` — prompt templates used by the tools/agent
- `ui/gradio_ui.py` — Gradio-based user interface
- `tests/` — unit tests for the tools and workflows
- `requirements.txt` — Python dependencies

## Quickstart

Prerequisites

- Python 3.10+ recommended
- Create and activate a virtual environment (Windows PowerShell example):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the demo script

```powershell
python main.py
```

Start the Gradio UI

```powershell
python ui\gradio_ui.py
```

Open http://127.0.0.1:7860 in your browser. The UI preloads the agent (or will load on first message) and provides example prompts.

## Development notes

- The agent is constructed in `agents/agent_runner.py` (and related modules). The UI imports `build_context_aware_agent` from `agents`.
- Prompts used by the tools live in `prompts/` and are intentionally stored as plain text for quick editing.
- Tools are in `tools/` and each has a focused responsibility (single-responsibility). Unit tests in `tests/` exercise these tools.

## Tests

## Contract (short)

- Input: a sequence of user messages (possibly containing context)
- Output: an agent response object containing messages (LLM-style) and metadata
- Error modes: network/search failures produce a friendly error message in the UI

## Edge cases considered

- Empty or whitespace-only user messages (ignored by UI)
- Very long context (split by `tools/context_splitter.py`)
- Failures when web search is unavailable — the agent will degrade to an explanation and suggest trying later

## Contributing

Small, focused PRs are welcome. Please add tests for new tools or changes to existing logic.

## License

This project is provided under the terms in the repository `LICENSE` file.

---