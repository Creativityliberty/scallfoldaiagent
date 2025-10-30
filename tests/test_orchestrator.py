import pytest
from backend.core.orchestrator import Orchestrator
from backend.core.shared import Shared
import uuid

@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test que l'orchestrateur s'initialise correctement."""
    orchestrator = Orchestrator()

    assert orchestrator is not None
    assert len(orchestrator.pipeline) > 0
    assert all(hasattr(node, 'name') for node in orchestrator.pipeline)

@pytest.mark.asyncio
async def test_orchestrator_run():
    """Test l'exécution complète du pipeline."""
    orchestrator = Orchestrator()
    shared = Shared()

    shared.set_metadata("flow_id", str(uuid.uuid4()))
    shared.set_metadata("user_id", "test_user")
    shared.set_context("user_input", "Bonjour, comment vas-tu ?")

    result = await orchestrator.run(shared)

    assert result is not None
    assert "answer" in result
    assert "confidence" in result
    assert "trace" in result
    assert len(shared.get_trace()) > 0

@pytest.mark.asyncio
async def test_orchestrator_with_empty_input():
    """Test avec un input vide."""
    orchestrator = Orchestrator()
    shared = Shared()

    shared.set_metadata("flow_id", str(uuid.uuid4()))
    shared.set_context("user_input", "")

    result = await orchestrator.run(shared)

    # L'orchestrateur devrait gérer gracieusement l'input vide
    assert result is not None
    assert "answer" in result

@pytest.mark.asyncio
async def test_pipeline_info():
    """Test la récupération d'infos sur le pipeline."""
    orchestrator = Orchestrator()
    info = orchestrator.get_pipeline_info()

    assert "nodes" in info
    assert "total_nodes" in info
    assert info["total_nodes"] == len(orchestrator.pipeline)
    assert all("name" in node and "type" in node for node in info["nodes"])

@pytest.mark.asyncio
async def test_partial_run():
    """Test l'exécution partielle du pipeline."""
    orchestrator = Orchestrator()
    shared = Shared()

    shared.set_metadata("flow_id", str(uuid.uuid4()))
    shared.set_context("user_input", "Test de run partiel")

    result = await orchestrator.run_partial(
        shared,
        start_node="perception",
        end_node="interpretation"
    )

    assert result is not None
    assert "status" in result
    assert result["status"] == "partial_completed"
