from __future__ import annotations

import json
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

DEFAULT_BASE = "https://ailegal.legal"


class LegalBreakdownTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        base = (self.runtime.credentials.get("api_base") or DEFAULT_BASE).rstrip("/")
        payload = {"text": tool_parameters["text"],
                   "jurisdiction": tool_parameters.get("jurisdiction") or "ru",
                   "locale": tool_parameters.get("locale") or "en"}
        r = requests.post(f"{base}/api/v2/ask", json=payload, timeout=60,
                          headers={"User-Agent": "dify-ailegal-plugin/0.0.2"})
        r.raise_for_status()
        data = r.json()
        result = data.get("result") or {}
        norms = [{"code": n.get("code"), "article": n.get("article"),
                  "title": n.get("title") or n.get("summary_en"),
                  "source_url": n.get("source_url"), "verified": bool(n.get("verified"))}
                 for n in (result.get("norms") or [])]
        yield self.create_json_message({
            "answer": result.get("answer") or "",
            "norms": norms,
            "jurisdiction": data.get("jurisdiction"),
            "refused": bool(data.get("refuse")),
            "note": "Legal information, not legal advice.",
        })
