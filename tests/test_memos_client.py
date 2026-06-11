import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from memos_mcp.client import MemosClient
from memos_mcp.models import Memo, User

def test_url_formatting():
    # URL formatting test
    client1 = MemosClient("http://localhost:5230", "token")
    assert client1.base_url == "http://localhost:5230/api/v1"

    client2 = MemosClient("http://localhost:5230/", "token")
    assert client2.base_url == "http://localhost:5230/api/v1"

    client3 = MemosClient("http://localhost:5230/api/v1", "token")
    assert client3.base_url == "http://localhost:5230/api/v1"

    client4 = MemosClient("http://localhost:5230/api/v1/", "token")
    assert client4.base_url == "http://localhost:5230/api/v1"

@pytest.mark.asyncio
async def test_get_user_info():
    client = MemosClient("http://localhost:5230", "dummy-token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "users/testuser",
        "username": "testuser",
        "displayName": "Test User",
        "role": "USER"
    }

    with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        info = await client.get_user_info()
        assert isinstance(info, User)
        assert info.username == "testuser"
        assert info.display_name == "Test User"
        mock_request.assert_called_once_with(
            "GET",
            "http://localhost:5230/api/v1/auth/me"
        )
    await client.close()

@pytest.mark.asyncio
async def test_create_memo():
    client = MemosClient("http://localhost:5230", "dummy-token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "memos/123",
        "content": "Hello World"
    }

    with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        res = await client.create_memo("Hello World", "PRIVATE", True)
        assert isinstance(res, Memo)
        assert res.name == "memos/123"
        assert res.content == "Hello World"
        mock_request.assert_called_once_with(
            "POST",
            "http://localhost:5230/api/v1/memos",
            json={
                "memo": {
                    "content": "Hello World",
                    "visibility": "PRIVATE",
                    "pinned": True
                }
            }
        )
    await client.close()

@pytest.mark.asyncio
async def test_update_memo():
    client = MemosClient("http://localhost:5230", "dummy-token")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "memos/123",
        "content": "Updated World"
    }

    with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        res = await client.update_memo("123", content="Updated World", pinned=False)
        assert isinstance(res, Memo)
        assert res.content == "Updated World"
        mock_request.assert_called_once_with(
            "PATCH",
            "http://localhost:5230/api/v1/memos/123",
            params={"updateMask": "content,pinned"},
            json={
                "memo": {
                    "name": "memos/123",
                    "content": "Updated World",
                    "pinned": False
                }
            }
        )
    await client.close()
