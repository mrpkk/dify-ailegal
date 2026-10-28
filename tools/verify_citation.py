from __future__ import annotations

from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

DEFAULT_BASE = "https://ailegal.legal"


class VerifyCitationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        base = (self.runtime.credentials.get("api_base") or DEFAULT_BASE).rstrip("/")
        params = {"code": tool_parameters["code"], "article": tool_parameters.get("article") or ""}
        if tool_parameters.get("jurisdiction"):
            params["jurisdiction"] = tool_parameters["jurisdiction"]
        r = requests.get(f"{base}/api/v2/oracle/citation", params=params, timeout=30,
                         headers={"User-Agent": "dify-ailegal-plugin/0.0.1"})
        r.raise_for_status()
        yield self.create_json_message(r.json())
