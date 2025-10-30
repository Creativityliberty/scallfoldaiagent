import pytest
from backend.core.shared import Shared, TraceEntry, NodeStatus
from datetime import datetime

def test_shared_initialization():
    """Test l'initialisation du Shared."""
    shared = Shared()

    assert "context" in shared
    assert "results" in shared
    assert "trace" in shared
    assert "metadata" in shared
    assert isinstance(shared["context"], dict)
    assert isinstance(shared["results"], dict)
    assert isinstance(shared["trace"], list)

def test_context_operations():
    """Test les opérations sur le contexte."""
    shared = Shared()

    # Set
    shared.set_context("key1", "value1")
    assert shared.get_context("key1") == "value1"

    # Get with default
    assert shared.get_context("nonexistent", "default") == "default"

    # Update
    shared.update_context({"key2": "value2", "key3": "value3"})
    assert shared.get_context("key2") == "value2"
    assert shared.get_context("key3") == "value3"

def test_results_operations():
    """Test les opérations sur les résultats."""
    shared = Shared()

    # Set result
    shared.set_result("node1", {"data": "test"})
    assert shared.get_result("node1") == {"data": "test"}

    # Get nested result
    assert shared.get_result("node1", "data") == "test"

    # Get nonexistent
    assert shared.get_result("nonexistent") is None

def test_trace_operations():
    """Test les opérations sur la trace."""
    shared = Shared()

    # Add trace
    entry = TraceEntry(
        timestamp=datetime.now(),
        node="test_node",
        status=NodeStatus.SUCCESS,
        duration_ms=10.5,
        data={"info": "test"}
    )

    shared.add_trace(entry)
    trace = shared.get_trace()

    assert len(trace) == 1
    assert trace[0].node == "test_node"
    assert trace[0].status == NodeStatus.SUCCESS
    assert trace[0].duration_ms == 10.5

def test_metadata_operations():
    """Test les opérations sur les métadonnées."""
    shared = Shared()

    # Set metadata
    shared.set_metadata("flow_id", "test-123")
    assert shared.get_metadata("flow_id") == "test-123"

    # Get nonexistent
    assert shared.get_metadata("nonexistent") is None

def test_shared_to_dict():
    """Test la conversion en dictionnaire."""
    shared = Shared()

    shared.set_context("ctx_key", "ctx_value")
    shared.set_result("node1", {"result": "ok"})
    shared.add_trace(TraceEntry(
        timestamp=datetime.now(),
        node="test",
        status=NodeStatus.SUCCESS,
        duration_ms=5.0
    ))

    dict_repr = shared.to_dict()

    assert "context" in dict_repr
    assert "results" in dict_repr
    assert "trace" in dict_repr
    assert "metadata" in dict_repr
    assert dict_repr["context"]["ctx_key"] == "ctx_value"
    assert dict_repr["results"]["node1"] == {"result": "ok"}
    assert len(dict_repr["trace"]) == 1
