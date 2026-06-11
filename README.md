# Memos MCP Server

A Model Context Protocol (MCP) server to interact with [usememos/memos](https://github.com/usememos/memos) (an open-source, self-hosted memo hub). Built using the official Python MCP SDK with `FastMCP` and `Pydantic v2` for type-safe validation.

## Features

This server exposes a set of tools to any MCP-compatible client (e.g., Claude Desktop, Cursor) allowing them to manage your Memos instance:

- **Get User Info**: Retrieve details about the authenticated user and verify connectivity.
- **List Memos**: List memos with support for sorting, state filtering (`NORMAL`/`ARCHIVED`), and pagination.
- **Get Memo**: Fetch a specific memo by ID or resource name.
- **Create Memo**: Create new memos with optional visibility (`PRIVATE`, `PROTECTED`, `PUBLIC`) and pinning.
- **Update Memo**: Update existing memo content, visibility, pin state, or archival status.
- **Delete Memo**: Permanently delete a memo.
- **Search Memos**: Easily search memos by content text and/or hashtags.

## Prerequisites

- **Python**: `>=3.14` (configured via `pyproject.toml`)
- **uv**: Modern Python package manager
- **Memos**: A running Memos instance (compatible with Memos v1 API)
- **Access Token**: A Personal Access Token (PAT) from your Memos account settings

## Setup

1. **Clone the Repository**
2. **Create Environment Configuration**
   Copy the example environment file:
   ```bash
   cp .example.env .env
   ```
   Edit `.env` and fill in your Memos server details:
   ```env
   MEMOS_URL="https://your-memos-instance.com"
   MEMOS_TOKEN="your_personal_access_token_here"
   ```

## Configuration

To integrate this server with **Claude Desktop**, add the following configuration to your Claude Desktop config file (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS).

### Option 1: Running with `uvx` (Recommended, no cloning required)
You can run the server directly from PyPI using `uvx` without setting up a local repository:

```json
{
  "mcpServers": {
    "memos": {
      "command": "uvx",
      "args": ["rmc-memos-mcp"],
      "env": {
        "MEMOS_URL": "https://your-memos-instance.com",
        "MEMOS_TOKEN": "your_personal_access_token_here"
      }
    }
  }
}
```

### Option 2: Running from Local Source
If you are developing locally and want to run the server from this cloned repository, use the following configuration:

```json
{
  "mcpServers": {
    "memos": {
      "command": "uv",
      "args": ["run", "-m", "memos_mcp"],
      "cwd": "/absolute/path/to/memos_mcp",
      "env": {
        "MEMOS_URL": "https://your-memos-instance.com",
        "MEMOS_TOKEN": "your_personal_access_token_here"
      }
    }
  }
}
```
*Make sure to replace `/absolute/path/to/memos_mcp` with your actual directory path.*

## Development & Testing

This project uses `uv` for dependency management, and includes linting, type-checking, and test tools.

### Installing Dependencies
```bash
uv sync
```

### Running Linter and Formatter (Ruff)
```bash
uv run ruff check .
```

### Running Type Checker (Mypy)
```bash
uv run mypy .
```

### Running Unit Tests (Pytest)
```bash
PYTHONPATH=src uv run pytest
```

### Debugging with MCP Inspector
You can debug the MCP server interactively using the official Inspector tool:
```bash
npx @modelcontextprotocol/inspector uv run -m memos_mcp
```
This launches a web interface to test the tools manually.
