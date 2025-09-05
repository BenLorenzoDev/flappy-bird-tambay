# Repository Guidelines

## Project Structure & Module Organization
- `archon/python`: Python services.
  - `src/server`: FastAPI API and services.
  - `src/agents`: PydanticAI agents service.
  - `tests`: Pytest suite (unit + integration).
- `agentic-coding-starter-kit`: Next.js UI (see `src`, `public`).
- `Games`, `Portfolio Sample`: Independent examples; not coupled to core services.

## Build, Test, and Development Commands
- Python (from `archon/python`):
  - Install deps: `uv sync -g all` (uses `pyproject.toml`, Python ≥3.12).
  - Run API: `uv run uvicorn src.server.main:app --reload --port 8050`.
  - Run Agents: `uv run uvicorn src.agents.server:app --reload --port 8052`.
  - Tests: `uv run pytest -q` (coverage: `uv run pytest --cov=src --cov-report=term-missing`).
  - Lint/format: `uv run ruff check .` and `uv run ruff format .`; types: `uv run mypy src`.
- Web UI (from `agentic-coding-starter-kit`):
  - Install: `pnpm install` (or `npm install`).
  - Dev server: `pnpm dev` (or `npm run dev`).

## Coding Style & Naming Conventions
- Python: Ruff-configured (line length 120, double quotes, spaces). Use type hints. `snake_case` for modules/functions, `PascalCase` for classes. Keep functions focused and tested.
- JS/TS: Follow repo ESLint config. `PascalCase` React components, `camelCase` variables, co-locate component styles.
- Files: Prefer descriptive names (e.g., `progress_tracker.py`, `projects_api.py`).

## Testing Guidelines
- Framework: `pytest` with `pytest-asyncio` and `pytest-cov`.
- Location/pattern: under `archon/python/tests`, files `test_*.py`; fixtures in `conftest.py`.
- Expectations: add tests for new behavior; include async paths and error cases. Aim for meaningful coverage; verify with `--cov`.

## Commit & Pull Request Guidelines
- Commits: concise, imperative. Prefer Conventional Commits, e.g. `feat(server): add progress API`, `fix(embeddings): guard empty input`.
- PRs: clear description, linked issues, screenshots for UI changes, and notes on migrations/configs. Ensure CI passes (lint + tests) and include tests for new code.

## Security & Configuration Tips
- Secrets via environment only; never commit `.env`. Agents read `ARCHON_SERVER_PORT` and other keys from the server; see `src/server/config` for required env vars.
- Validate local `.env` before running services; keep ports consistent across services.

