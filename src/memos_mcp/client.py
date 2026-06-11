import httpx
from typing import Any, Dict, Optional
from memos_mcp.models import Memo, User, ListMemosResponse

class MemosClient:
    """Memos API v1 Client with Pydantic support"""

    def __init__(self, base_url: str, token: str):
        # Remove trailing slash
        base_url = base_url.rstrip("/")
        # Append /api/v1 if not present
        if not base_url.endswith("/api/v1"):
            self.base_url = f"{base_url}/api/v1"
        else:
            self.base_url = base_url

        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def close(self):
        """Close the HTTP client session."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json()
                message = error_detail.get("message", str(e))
            except Exception:
                message = e.response.text or str(e)
            raise ValueError(f"Memos API Error ({e.response.status_code}): {message}")
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Memos server: {e}")

    async def get_user_info(self) -> User:
        """Get the authenticated user's info (checks connection & auth token)."""
        data = await self._request("GET", "auth/me")
        return User.model_validate(data)

    async def list_memos(
        self,
        page_size: int = 50,
        page_token: str = "",
        state: str = "NORMAL",
        order_by: str = "",
        filter_str: str = ""
    ) -> ListMemosResponse:
        """List memos with pagination and filters."""
        params: Dict[str, Any] = {}
        if page_size:
            params["pageSize"] = page_size
        if page_token:
            params["pageToken"] = page_token
        if state:
            params["state"] = state
        if order_by:
            params["orderBy"] = order_by
        if filter_str:
            params["filter"] = filter_str

        data = await self._request("GET", "memos", params=params)
        return ListMemosResponse.model_validate(data)

    async def get_memo(self, name: str) -> Memo:
        """Get a specific memo by resource name (e.g. 'memos/123' or '123')."""
        if not name.startswith("memos/"):
            name = f"memos/{name}"
        data = await self._request("GET", name)
        return Memo.model_validate(data)

    async def create_memo(
        self,
        content: str,
        visibility: str = "PRIVATE",
        pinned: bool = False
    ) -> Memo:
        """Create a new memo."""
        body = {
            "memo": {
                "content": content,
                "visibility": visibility,
                "pinned": pinned
            }
        }
        data = await self._request("POST", "memos", json=body)
        return Memo.model_validate(data)

    async def update_memo(
        self,
        name: str,
        content: Optional[str] = None,
        visibility: Optional[str] = None,
        pinned: Optional[bool] = None,
        state: Optional[str] = None
    ) -> Memo:
        """Update fields of an existing memo using an update mask."""
        if not name.startswith("memos/"):
            name = f"memos/{name}"

        memo_data: Dict[str, Any] = {"name": name}
        update_fields = []

        if content is not None:
            memo_data["content"] = content
            update_fields.append("content")
        if visibility is not None:
            memo_data["visibility"] = visibility
            update_fields.append("visibility")
        if pinned is not None:
            memo_data["pinned"] = pinned
            update_fields.append("pinned")
        if state is not None:
            memo_data["state"] = state
            update_fields.append("state")

        if not update_fields:
            raise ValueError("No fields specified to update.")

        params = {"updateMask": ",".join(update_fields)}
        body = {"memo": memo_data}
        data = await self._request("PATCH", name, params=params, json=body)
        return Memo.model_validate(data)

    async def delete_memo(self, name: str) -> None:
        """Delete a memo."""
        if not name.startswith("memos/"):
            name = f"memos/{name}"
        await self._request("DELETE", name)
