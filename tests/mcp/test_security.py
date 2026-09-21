"""Security regression tests: fail-closed auth, log hygiene, bind host, task arg injection."""

import importlib
import json
import logging
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from clinemcp.mcp.auth import log_auth_config, verify_token_dependency
from clinemcp.mcp.tools import handle_cline_start


class TestFailClosedAuth:
    @pytest.mark.asyncio
    @patch.dict(os.environ, {"CLINEMCP_ALLOW_NO_AUTH": "1"}, clear=True)
    async def test_explicit_opt_out_allows_without_token(self):
        assert await verify_token_dependency(None) is True

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"CLINEMCP_ALLOW_NO_AUTH": "true"}, clear=True)
    async def test_opt_out_requires_exact_value_1(self):
        with pytest.raises(Exception) as exc_info:
            await verify_token_dependency(None)
        assert exc_info.value.status_code == 401

    @patch.dict(os.environ, {}, clear=True)
    def test_startup_warns_when_no_token(self, caplog):
        with caplog.at_level(logging.WARNING, logger="clinemcp.mcp.auth"):
            log_auth_config()
        assert "No CLINEMCP_AUTH_TOKEN configured" in caplog.text
        assert "reject" in caplog.text

    @patch.dict(os.environ, {"CLINEMCP_AUTH_TOKEN": "tok"}, clear=True)
    def test_startup_silent_when_token_set(self, caplog):
        with caplog.at_level(logging.WARNING, logger="clinemcp.mcp.auth"):
            log_auth_config()
        assert caplog.text == ""


class TestSseLogging:
    @patch.dict(os.environ, {"CLINEMCP_AUTH_TOKEN": "super-secret-token"}, clear=True)
    def test_sse_does_not_log_authorization_header(self, caplog):
        from clinemcp.mcp.server import create_app

        app = create_app()
        app.state.sse_transport = MagicMock()  # connect_sse is not an async CM -> handled 500
        app.state.mcp_server = MagicMock()
        client = TestClient(app)  # lifespan not started

        with caplog.at_level(logging.DEBUG, logger="clinemcp.mcp.server"):
            client.get("/sse", headers={"Authorization": "Bearer super-secret-token"})

        assert "path=/sse" in caplog.text
        assert "super-secret-token" not in caplog.text
        assert "authorization" not in caplog.text.lower()


class TestBindHost:
    def test_default_bind_host_is_localhost(self, monkeypatch):
        import clinemcp.mcp.server as server_module

        monkeypatch.delenv("MCP_HOST", raising=False)
        assert importlib.reload(server_module).MCP_HOST == "127.0.0.1"

    def test_bind_host_env_override(self, monkeypatch):
        import clinemcp.mcp.server as server_module

        monkeypatch.setenv("MCP_HOST", "0.0.0.0")
        assert importlib.reload(server_module).MCP_HOST == "0.0.0.0"
        monkeypatch.delenv("MCP_HOST")
        importlib.reload(server_module)


class TestTaskArgInjection:
    @pytest.mark.asyncio
    async def test_task_starting_with_dash_rejected(self):
        with patch("clinemcp.mcp.tools.SessionStore") as mock_store_class, \
             patch("clinemcp.mcp.tools.start_session") as mock_start:
            mock_store = MagicMock()
            mock_store.init_db = AsyncMock()
            mock_store.get_active_session = AsyncMock(return_value=None)
            mock_store.create_session = AsyncMock()
            mock_store_class.return_value = mock_store

            result = json.loads(await handle_cline_start({
                "task": "--config C:\\evil",
                "model": "qwen2.5-coder:7b",
            }))

        assert result["session_id"] is None
        assert "must not start with '-'" in result["error"]
        mock_store.create_session.assert_not_called()
        mock_start.assert_not_called()
