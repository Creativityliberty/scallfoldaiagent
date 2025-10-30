import pytest
from backend.nodes.perception import PerceptionNode
from backend.nodes.interpretation import InterpretationNode
from backend.nodes.reasoning import ReasoningNode
from backend.core.shared import Shared

@pytest.mark.asyncio
async def test_perception_node():
    """Test le node de perception."""
    node = PerceptionNode()
    shared = Shared()

    result, _ = await node.run(shared, "Bonjour, comment ça va ?")

    assert result is not None
    assert "clean_input" in result
    assert "raw" in result
    assert "language" in result
    assert result["language"] == "fr"

@pytest.mark.asyncio
async def test_perception_with_whitespace():
    """Test perception avec des espaces excessifs."""
    node = PerceptionNode()
    shared = Shared()

    result, _ = await node.run(shared, "  Test   avec   espaces  ")

    assert result["clean_input"] == "Test avec espaces"
    assert result["length"] == len("Test avec espaces")

@pytest.mark.asyncio
async def test_interpretation_node():
    """Test le node d'interprétation."""
    # Setup
    shared = Shared()
    perception_node = PerceptionNode()
    interpretation_node = InterpretationNode()

    # Perception
    perception_result, _ = await perception_node.run(shared, "Comment créer un fichier Python ?")

    # Interpretation
    result, _ = await interpretation_node.run(shared, perception_result)

    assert result is not None
    assert "intent" in result
    assert "task_type" in result
    assert result["intent"] in ["information_seeking", "question", "instruction"]

@pytest.mark.asyncio
async def test_reasoning_node_simple():
    """Test le node de raisonnement en mode simple."""
    shared = Shared()

    # Setup context
    shared.set_result("perception", {"clean_input": "Bonjour"})
    shared.set_result("interpretation", {
        "intent": "conversation",
        "task_type": "general",
        "complexity": "simple"
    })

    node = ReasoningNode()
    result, _ = await node.run(shared, {
        "intent": "conversation",
        "task_type": "general",
        "clean_input": "Bonjour",
        "complexity": "simple"
    })

    assert result is not None
    assert "decision" in result
    assert "confidence" in result
    assert result["mode"] == "simple"

@pytest.mark.asyncio
async def test_node_error_handling():
    """Test la gestion d'erreur dans un node."""
    node = PerceptionNode()
    shared = Shared()

    # Un input None devrait être géré
    result, _ = await node.run(shared, None)

    assert result is not None
    assert result["clean_input"] == ""
