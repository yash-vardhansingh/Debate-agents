# Debate-agent

A small demo that runs a multi-agent debate using Autogen-style agent chat components and a Streamlit frontend.

This repo contains two main entry points:

- `app.py` — Streamlit-based UI that starts a debate and streams messages into a chat-like interface.
- `debate.py` — Agent configuration and a CLI-style runner. Defines a host (Jane) and two debaters (John - pro, Alice - con) using the Autogen agent/chat stack.

Quick notes
---------------
- This project expects Python 3.10+.
- The code in `debate.py` uses custom Autogen-related packages (`autogen_ext`, `autogen_core`, `autogen_agentchat`) and an HTTP client (`httpx`).
- `debate.py` currently contains an API key and a base_url for a private LLM endpoint. Replace these with environment variables before running.

Suggested (example) dependencies
-------------------------------
The exact package names for your Autogen stack may vary. If you have a package manager or environment, prefer installing pinned dependencies. Example:

```powershell
# create and activate venv (Windows PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install streamlit httpx
# Install your autogen packages (replace with correct package names available to you)
pip install autogen-core autogen-ext autogen-agentchat
```

Running
-------

- To run the CLI-style runner (prints streamed chunks to stdout):

```powershell
python debate.py
```

- To run the Streamlit UI in a browser (recommended for interactive viewing):

```powershell
streamlit run app.py
```

Security & configuration
------------------------
- `debate.py` currently inflates a model client with a hard-coded `api_key` and `base_url`. Do not commit real keys to source control. Instead, set them from environment variables or a secure vault. For example:

```python
import os
api_key = os.environ.get("DEBATE_API_KEY")
base_url = os.environ.get("DEBATE_BASE_URL")
```

- The project also sets `httpx.AsyncClient(verify=False)` which disables HTTPS verification — avoid this in production.

Files
-----

- `app.py` — Streamlit UI that drives the debate. Uses `team_config` and `debate` from `debate.py`.
- `debate.py` — Agent setup, streaming helpers, and a small `main()` for testing.

Next steps / suggestions
-----------------------
- Add a `requirements.txt` with exact dependency versions.
- Move secrets to environment variables.
- Add a short test or script to simulate a debate without calling a remote model (for local dev).

License
-------
Specify a license if you intend to share this repository publicly.

