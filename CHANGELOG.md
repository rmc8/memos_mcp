# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-06-12

### Added
- Registered package-identical script alias (`rmc-memos-mcp`) to enable direct execution via `uvx rmc-memos-mcp`.
- Documented `uvx` setup instructions in `README.md`.

## [0.1.0] - 2026-06-12

### Added
- Initial release of Memos MCP Server.
- Implemented `MemosClient` in `libs/memos_client.py` using `httpx` to interface with Memos API v1.
- Implemented MCP Server endpoints in `main.py` using `FastMCP`:
  - `get_user_info`
  - `list_memos`
  - `get_memo`
  - `create_memo`
  - `update_memo`
  - `delete_memo`
  - `search_memos`
- Integrated Pydantic v2 models in `libs/models.py` for Memos, Users, and Lists to ensure type-safe inputs and outputs.
- Configured environment variables loading with `python-dotenv` (via `.env` / `.example.env`).
- Created asynchronous unit tests in `tests/test_memos_client.py` using `pytest` and `pytest-asyncio`.
- Configured development toolchain with `ruff` for linting/formatting and `mypy` for static type checking.
