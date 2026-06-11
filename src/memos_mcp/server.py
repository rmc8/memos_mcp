import os
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from memos_mcp.client import MemosClient
from memos_mcp.models import Memo, User, ListMemosResponse

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("memos")

def get_client() -> MemosClient:
    """Create and return a MemosClient using credentials from environment variables."""
    base_url = os.getenv("MEMOS_URL")
    token = os.getenv("MEMOS_TOKEN")

    if not base_url or not token:
        raise ValueError(
            "MEMOS_URL and MEMOS_TOKEN environment variables must be set. "
            "Please configure them in your .env file."
        )
    return MemosClient(base_url, token)

@mcp.tool()
async def get_user_info() -> User:
    """
    Get the authenticated user's information.
    Useful for checking connectivity and verifying the access token.
    """
    async with get_client() as client:
        return await client.get_user_info()

@mcp.tool()
async def list_memos(
    limit: int = 50,
    state: str = "NORMAL",
    filter_str: Optional[str] = None,
    order_by: Optional[str] = None,
    page_token: Optional[str] = None
) -> ListMemosResponse:
    """
    List memos from the Memos server with pagination and filtering.

    Args:
        limit: Max number of memos to retrieve (default 50).
        state: State of memos to list ('NORMAL' or 'ARCHIVED').
        filter_str: Optional AIP-160 CEL filter string (e.g. "tag_search == ['Work']").
        order_by: Optional sorting order (e.g. "pinned desc, create_time desc").
        page_token: Optional page token for pagination.
    """
    async with get_client() as client:
        return await client.list_memos(
            page_size=limit,
            page_token=page_token or "",
            state=state,
            order_by=order_by or "",
            filter_str=filter_str or ""
        )

@mcp.tool()
async def get_memo(name: str) -> Memo:
    """
    Get a specific memo by its ID or resource name.

    Args:
        name: The memo ID or resource name (e.g. '123' or 'memos/123').
    """
    async with get_client() as client:
        return await client.get_memo(name)

@mcp.tool()
async def create_memo(
    content: str,
    visibility: str = "PRIVATE",
    pinned: bool = False
) -> Memo:
    """
    Create a new memo.

    Args:
        content: The text content of the memo in Markdown format.
        visibility: The visibility of the memo ('PRIVATE', 'PROTECTED', or 'PUBLIC').
        pinned: Whether the memo is pinned.
    """
    async with get_client() as client:
        return await client.create_memo(content, visibility, pinned)

@mcp.tool()
async def update_memo(
    name: str,
    content: Optional[str] = None,
    visibility: Optional[str] = None,
    pinned: Optional[bool] = None,
    state: Optional[str] = None
) -> Memo:
    """
    Update fields of an existing memo.

    Args:
        name: The memo ID or resource name to update (e.g. '123' or 'memos/123').
        content: Optional new Markdown text content.
        visibility: Optional new visibility ('PRIVATE', 'PROTECTED', or 'PUBLIC').
        pinned: Optional pin state (True or False).
        state: Optional state of the memo ('NORMAL' or 'ARCHIVED').
    """
    async with get_client() as client:
        return await client.update_memo(
            name=name,
            content=content,
            visibility=visibility,
            pinned=pinned,
            state=state
        )

@mcp.tool()
async def delete_memo(name: str) -> str:
    """
    Delete a memo by its ID or resource name.

    Args:
        name: The memo ID or resource name to delete (e.g. '123' or 'memos/123').
    """
    async with get_client() as client:
        await client.delete_memo(name)
        return f"Memo '{name}' successfully deleted."

@mcp.tool()
async def search_memos(
    query: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 50
) -> ListMemosResponse:
    """
    Search memos by content text and/or hashtag.

    Args:
        query: Optional text snippet to search within memo content.
        tag: Optional hashtag to filter memos (e.g. 'todo' or '#todo').
        limit: Max number of results to retrieve (default 50).
    """
    filters = []
    if query:
        filters.append(f"content_search == ['{query}']")
    if tag:
        clean_tag = tag.lstrip("#")
        filters.append(f"tag_search == ['{clean_tag}']")

    filter_str = " && ".join(filters) if filters else ""

    return await list_memos(limit=limit, filter_str=filter_str)

def main():
    """Entrypoint for the MCP server CLI command."""
    mcp.run()

if __name__ == "__main__":
    main()
