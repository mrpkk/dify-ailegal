from __future__ import annotations

from typing import Any

import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

DEFAULT_BASE = "https://ailegal.legal"


class AILegalProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        base = (credentials.get("api_base") or DEFAULT_BASE).rstrip("/")
        if not base.startswith(("http://", "https://")):
            raise ToolProviderCredentialValidationError("api_base must be an absolute http(s) URL")
        try:
            r = requests.get(f"{base}/api/v2/oracle/stats", timeout=10,
                             headers={"User-Agent": "dify-ailegal-plugin/0.0.1"})
            r.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            raise ToolProviderCredentialValidationError(f"AILegal is not reachable at {base}: {exc}") from exc
