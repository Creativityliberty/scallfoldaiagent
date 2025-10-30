import pytest
from backend.mcp.artifacts import (
    create_artifact,
    save_artifact,
    list_artifacts,
    update_artifact,
    delete_artifact
)
from backend.mcp.artifact_store import artifact_store

@pytest.fixture(autouse=True)
def clear_store():
    """Clear the artifact store before each test."""
    artifact_store.clear()
    yield
    artifact_store.clear()

@pytest.mark.asyncio
async def test_create_artifact_code():
    """Test creating a code artifact."""
    result = await create_artifact(
        name="test.py",
        type="code",
        content="print('Hello World')"
    )

    assert result["success"] is True
    assert result["artifact"]["name"] == "test.py"
    assert result["artifact"]["type"] == "code"
    assert result["artifact"]["language"] == "python"
    assert result["artifact"]["content"] == "print('Hello World')"
    assert result["artifact"]["lines"] == 1

@pytest.mark.asyncio
async def test_create_artifact_document():
    """Test creating a document artifact."""
    result = await create_artifact(
        name="README.md",
        type="document",
        content="# Hello\n\nThis is a test."
    )

    assert result["success"] is True
    assert result["artifact"]["type"] == "document"
    assert result["artifact"]["language"] == "markdown"

@pytest.mark.asyncio
async def test_create_artifact_invalid_type():
    """Test creating an artifact with invalid type."""
    result = await create_artifact(
        name="test.txt",
        type="invalid_type",
        content="test"
    )

    assert result["success"] is False
    assert "error" in result

@pytest.mark.asyncio
async def test_create_artifact_with_metadata():
    """Test creating an artifact with metadata."""
    result = await create_artifact(
        name="script.py",
        type="code",
        content="print('test')",
        description="Test script",
        metadata={"author": "Test", "version": "1.0"}
    )

    assert result["success"] is True
    assert result["artifact"]["description"] == "Test script"
    assert result["artifact"]["metadata"]["author"] == "Test"
    assert result["artifact"]["metadata"]["version"] == "1.0"

@pytest.mark.asyncio
async def test_list_artifacts():
    """Test listing artifacts."""
    # Create some artifacts
    await create_artifact("test1.py", "code", "print('1')")
    await create_artifact("test2.py", "code", "print('2')")
    await create_artifact("doc.md", "document", "# Doc")

    # List all
    result = await list_artifacts()
    assert result["success"] is True
    assert len(result["artifacts"]) == 3

    # List with filter
    result = await list_artifacts(type_filter="code")
    assert len(result["artifacts"]) == 2

@pytest.mark.asyncio
async def test_update_artifact():
    """Test updating an artifact."""
    # Create
    create_result = await create_artifact(
        "test.py",
        "code",
        "print('old')"
    )
    artifact_id = create_result["artifact"]["id"]

    # Update
    update_result = await update_artifact(
        artifact_id=artifact_id,
        content="print('new')",
        description="Updated"
    )

    assert update_result["success"] is True
    assert "content" in update_result["updated_fields"]
    assert update_result["artifact"]["content"] == "print('new')"
    assert update_result["artifact"]["description"] == "Updated"

@pytest.mark.asyncio
async def test_update_nonexistent_artifact():
    """Test updating a non-existent artifact."""
    result = await update_artifact(
        artifact_id="nonexistent",
        content="test"
    )

    assert result["success"] is False
    assert "error" in result

@pytest.mark.asyncio
async def test_delete_artifact():
    """Test deleting an artifact."""
    # Create
    create_result = await create_artifact(
        "test.py",
        "code",
        "print('test')"
    )
    artifact_id = create_result["artifact"]["id"]

    # Delete
    delete_result = await delete_artifact(artifact_id)

    assert delete_result["success"] is True

    # Verify deleted
    list_result = await list_artifacts()
    assert len(list_result["artifacts"]) == 0

@pytest.mark.asyncio
async def test_delete_nonexistent_artifact():
    """Test deleting a non-existent artifact."""
    result = await delete_artifact("nonexistent")

    assert result["success"] is False
    assert "error" in result

@pytest.mark.asyncio
async def test_artifact_store_max_limit():
    """Test that the store respects max artifact limit."""
    # Set a small limit for testing
    original_max = artifact_store.max_artifacts
    artifact_store.max_artifacts = 3

    try:
        # Create more than max
        for i in range(5):
            await create_artifact(f"test{i}.py", "code", f"print({i})")

        # Should only have 3 (max)
        result = await list_artifacts(limit=10)
        assert len(result["artifacts"]) == 3

    finally:
        artifact_store.max_artifacts = original_max

@pytest.mark.asyncio
async def test_language_auto_detection():
    """Test automatic language detection from filename."""
    test_cases = [
        ("script.py", "python"),
        ("app.js", "javascript"),
        ("main.go", "go"),
        ("component.tsx", "tsx"),
        ("styles.css", "css"),
        ("config.yaml", "yaml"),
    ]

    for filename, expected_lang in test_cases:
        result = await create_artifact(
            name=filename,
            type="code",
            content="test"
        )

        assert result["artifact"]["language"] == expected_lang

def test_artifact_store_stats():
    """Test artifact store statistics."""
    # Clear and create artifacts
    artifact_store.clear()

    # Create via store directly for testing
    artifact_store.add({
        "id": "1",
        "type": "code",
        "size_bytes": 100,
        "created_at": "2025-01-01"
    })
    artifact_store.add({
        "id": "2",
        "type": "code",
        "size_bytes": 200,
        "created_at": "2025-01-02"
    })
    artifact_store.add({
        "id": "3",
        "type": "document",
        "size_bytes": 150,
        "created_at": "2025-01-03"
    })

    stats = artifact_store.get_stats()

    assert stats["total_artifacts"] == 3
    assert stats["by_type"]["code"] == 2
    assert stats["by_type"]["document"] == 1
    assert stats["total_size_bytes"] == 450

def test_artifact_store_export_import(tmp_path):
    """Test artifact store export and import."""
    # Create artifacts
    artifact_store.clear()
    artifact_store.add({
        "id": "test1",
        "content": "test content",
        "type": "code"
    })

    # Export
    export_file = tmp_path / "artifacts.json"
    artifact_store.export_to_file(str(export_file))

    assert export_file.exists()

    # Clear and import
    artifact_store.clear()
    count = artifact_store.import_from_file(str(export_file))

    assert count == 1
    assert artifact_store.get("test1") is not None
