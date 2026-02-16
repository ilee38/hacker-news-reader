# AGENTS.md

## Project scope
- This repository is a small Python CLI that fetches and prints Hacker News top stories.
- Runtime code is in `hnreader.py` with argument parsing defined in `cli.py`.

## Setup and validation commands
- Create and activate a virtual environment:
  - `python3 -m venv .venv && source .venv/bin/activate`
- Install dependencies:
  - `pip install -r requirements.txt`
- Run the app:
  - `python3 hnreader.py`
  - `python3 hnreader.py -q 25`
- Validate code:
  - `python3 -m py_compile cli.py hnreader.py`
- Run tests (none are currently committed, but this is the configured discovery command):
  - `python3 -m unittest discover -v`
- Run one unittest when tests exist:
  - `python3 -m unittest tests.test_module.TestClass.test_method`

## Architecture notes
- `hnreader.py` is the entrypoint and contains fetch/format/print flow:
  1. Parse args from imported `parser`.
  2. Fetch story IDs from `/v0/topstories.json`.
  3. Fetch each story from `/v0/item/<id>.json`.
  4. Print title, URL (if present), score, and elapsed time.
- `API_ENDPOINT_PREFIX` is the shared base URL for Hacker News API calls.

## Repository conventions for agents
- Keep CLI argument definitions in `cli.py`; consume them from `hnreader.py`.
- Preserve current terminal output structure unless a task explicitly requests UX changes.
- Keep Hacker News API interactions in helper functions (`get_top_stories`, `get_story_properties`).
- Respect the quantity semantics documented in `README.md` (default 10, API max 500).
