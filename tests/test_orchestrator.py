import asyncio
import json
import pytest

from backend.core.orchestrator import Orchestrator
from backend.core.shared import Shared
from backend.nodes.reasoning import ReasoningNode

class DummyGemini:
    async def generate(self, prompt: str, **kwargs) -> str:
        return json.dumps({
            "steps": [
                {"id": 1, "action": "analyze", "rationale": "test"},
                {"id": 2, "action": "answer", "rationale": "test"}
            ]
        })

@pytest.mark.asyncio
async def test_orchestrator_flow(monkeypatch):
    orch = Orchestrator()
    # Monkeypatch ReasoningNode's Gemini client
    for node in orch.pipeline:
        if isinstance(node, ReasoningNode):
            node.gemini = DummyGemini()
    
    shared = Shared()
    shared.set_context("user_input", "Bonjour, peux-tu résumer ceci ?")
    
    result = await orch.run(shared)
    assert "answer" in result
    assert result["confidence"] >= 0.0
    # Ensure trace has entries
    assert len(shared.get_trace()) >= 3
