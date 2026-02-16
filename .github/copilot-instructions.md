# Copilot Instructions for `hacker-news-reader`

## Build, test, and lint commands

- Set up dependencies:
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Run the CLI:
  - `python3 hnreader.py`
  - `python3 hnreader.py -q 25`
- Test suite (unittest discovery; currently no committed tests):
  - `python3 -m unittest discover -v`
- Run a single unittest (when tests are present):
  - `python3 -m unittest tests.test_module.TestClass.test_method`
- Linting: no linter is configured in this repository.
- Fast code validity check:
  - `python3 -m py_compile cli.py hnreader.py`

## High-level architecture

- `hnreader.py` is the runtime entrypoint and contains the app logic.
- `cli.py` defines a shared module-level `argparse` parser (`-q/--quantity`, default `10`) that `hnreader.py` imports.
- Data flow in `hnreader.py`:
  1. Parse CLI args in `main()`.
  2. Call `get_top_stories()` to fetch top story IDs from `https://hacker-news.firebaseio.com/v0/topstories.json`.
  3. Call `print_stories(...)`, which fetches each story via `/item/<id>.json`, formats title/url/score/elapsed time, and prints to stdout.
- Display behavior is terminal-first (header banner + separator lines), with elapsed time calculated by `get_elapsed_time(...)`.

## Key repository conventions

- Keep argument parsing in `cli.py`; `hnreader.py` should consume `parser.parse_args()` rather than redefining CLI options.
- Keep Hacker News API access centralized around `API_ENDPOINT_PREFIX` and helper functions (`get_top_stories`, `get_story_properties`).
- Preserve the existing output format structure (header block, numbered stories, score/time line, separator) unless intentionally changing CLI UX.
- Respect current behavior around story quantity and the Hacker News API max (500 stories) documented in `README.md`.
