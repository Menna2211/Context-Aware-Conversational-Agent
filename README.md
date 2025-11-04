# Context-Aware Conversational Agent

A small project that builds a context-aware conversational agent. The agent inspects user messages for contextual information, evaluates relevance, and—when needed—performs web searches to enrich responses. This repository includes the agent implementation, a Gradio-based UI, and small tools for context-splitting, relevance checking, and web search.

## Quick Overview

- **Language:** Python
- **Purpose:** Demo a conversation agent that is aware of and uses provided context
- **UI:** Gradio interface at `ui/gradio_ui.py`

## Features

- Detects whether user input includes context
- Splits longer context into chunks when necessary
- Checks context relevance to the user query
- Performs a web search when the agent lacks sufficient context
- Gradio UI with chat-like experience and typing animation

## Repository Layout

```
├── main.py                  # Simple CLI/demo runner
├── agents/                  # Agent construction and runner code
├── tools/                   # Helper tools (context, relevance splitter, search)
├── prompts/                 # Prompt templates used by tools/agent
├── ui/
│   └── gradio_ui.py        # Gradio-based user interface
├── tests/                   # Unit tests for tools and workflows
├── fastapiapp/
│   └── appmain.py          # FastAPI server wrapper
├── model_config.py          # LLM client configuration
└── requirements.txt         # Python dependencies
```

## Quickstart

### Prerequisites

- Python 3.10+ recommended
- Create and activate a virtual environment (Windows PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the Demo Script

```powershell
python main.py
```

### Start the Gradio UI

```powershell
python ui\gradio_ui.py
```

Open http://127.0.0.1:7860 in your browser. The UI preloads the agent (or will load on first message) and provides example prompts.

## FastAPI Server

A lightweight FastAPI wrapper is provided in `fastapiapp/appmain.py`. It exposes a minimal stateless chat endpoint and a health check.

### Starting the Server

Run inside the project's virtualenv:

```powershell
python fastapiapp\appmain.py
```

The server listens on `127.0.0.1:8000` by default.

### API Endpoints

**Health Check:**
```
GET http://127.0.0.1:8000/
Response: {"status":"ok","message":"Stateless Chatbot API running!"}
```

**Chat Endpoint:**
```
POST http://127.0.0.1:8000/chat
Request: {"message": "..."}
Response: {"response": "..."}
```

**Example (Windows PowerShell):**
```powershell
$body = '{"message":"What is LangChain used for?"}'
curl -Method POST -Uri http://127.0.0.1:8000/chat -Body $body -ContentType 'application/json'
```

## Model Configuration

`model_config.py` contains helper factories for constructing LLM clients:

- **`get_openrouter_llm()`** — Returns a `ChatOpenAI`-style client configured for OpenRouter
- **`get_ollama_llm()`** — Returns a `ChatOllama` client (local Ollama server at `http://localhost:11434`)

## Tools (Detailed)

This project keeps small, focused tools in the `tools/` folder, implemented with the `@tool` decorator.

### `judge_context_presence(user_input: str) -> str`
**File:** `tools/context_presence_judge.py`

Decides whether a message contains background context or is a standalone question. Uses `prompts/context_judge_prompt.txt`.

**Returns:** `context_provided` or `context_missing`

### `check_context_relevance(context: str, question: str) -> str`
**File:** `tools/context_relevance_checker.py`

Given candidate context and a question, determines relevance to help the agent decide whether to use provided context or run a web search.

**Returns:** `relevant` or `not_relevant`

### `split_context(user_input: str) -> str`
**File:** `tools/context_splitter.py`

Extracts and returns JSON containing `context` and `question` fields when a message mixes background context with a question. Should be used only after relevance is confirmed.

### `web_search(query: str) -> str`
**File:** `tools/web_search_tool.py`

Performs web search using the Tavily API and returns the most relevant snippet found.

**Note:** Replace the example API key with an environment variable before production use.

## Development Notes

- The agent is constructed in `agents/agent_runner.py` and related modules
- The UI imports `build_context_aware_agent` from `agents`
- Prompts are stored as plain text in `prompts/` for quick editing
- Each tool has a focused, single responsibility
- Unit tests in `tests/` exercise tool functionality


## Contract

**Input:** A sequence of user messages (possibly containing context)

**Output:** An agent response object containing messages (LLM-style) and metadata

**Error Modes:** Network/search failures produce friendly error messages in the UI

## Edge Cases Considered

- Empty or whitespace-only user messages (ignored by UI)
- Very long context (split by `tools/context_splitter.py`)
- Web search unavailability — agent degrades gracefully with explanation

## Security & Secrets

- Create a `.env.example` file documenting required environment variables
- **Never commit `.env` files**
- Use environment variables or secret managers for API keys

## Contributing

Small, focused PRs are welcome. Please add tests for new tools or changes to existing logic.

## License

This project is provided under the terms in the repository `LICENSE` file.