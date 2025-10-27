import json
import pytest

from backend.core.shared import Shared
from backend.nodes.perception import PerceptionNode
from backend.nodes.interpretation import InterpretationNode
from backend.nodes.reasoning import ReasoningNode
from backend.nodes.synthesis import SynthesisNode
from backend.nodes.action import ActionNode

class DummyGemini:
    async def generate(self, prompt: str, **kwargs) -> str:
        return json.dumps({
            "steps": [
                {"id": 1, "action": "check", "rationale": "ok"},
                {"id": 2, "action": "reply", "rationale": "ok"}
            ]
        })

@pytest.mark.asyncio
async def test_nodes_sequence(monkeypatch):
    shared = Shared()

    # Perception
    p = PerceptionNode()
    p_result, _ = await p.run(shared, "  Hello?  ")
    assert p_result["clean_input"] == "Hello?"

    # Interpretation
    i = InterpretationNode()
    i_result, _ = await i.run(shared, p_result)
    assert i_result["intent"] == "question"

    # Reasoning with mocked Gemini
    r = ReasoningNode()
    r.gemini = DummyGemini()
    r_input = {
        "intent": i_result["intent"],
        "task_type": i_result["task_type"],
        "clean_input": p_result["clean_input"],
        "memory_context": []
    }
    r_result, _ = await r.run(shared, r_input)
    assert r_result["confidence"] >= 0.5
    assert len(r_result["steps"]) == 2

    # Synthesis
    s = SynthesisNode()
    s_input = {"reasoning": r_result, "input": p_result["clean_input"]}
    s_result, _ = await s.run(shared, s_input)
    assert "Synthèse basée" in s_result["draft"]

    # Action
    a = ActionNode()
    a_result, _ = await a.run(shared, {"synthesis": s_result})
    assert a_result["final"].startswith("Synthèse bas")
