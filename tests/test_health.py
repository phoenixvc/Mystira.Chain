"""Basic health check tests for the gRPC server."""


def test_imports():
    """Verify core modules can be imported."""
    import story_pb2
    import story_pb2_grpc

    assert hasattr(story_pb2, "CreateCollectionRequest")
    assert hasattr(story_pb2, "RegisterAssetRequest")
    assert hasattr(story_pb2_grpc, "StoryServiceServicer")


def test_schemas():
    """Verify Pydantic schemas are valid."""
    from schemas import IPAssetCreate, SPGCollectionCreate

    collection = SPGCollectionCreate(
        name="Test",
        symbol="TST",
        mint_fee_recipient="0x1234567890123456789012345678901234567890",
    )
    assert collection.name == "Test"

    asset = IPAssetCreate(
        text_content="Test content",
        asset_name="Test Asset",
        asset_description="A test asset",
        spg_nft_contract_address="0x1234567890123456789012345678901234567890",
    )
    assert asset.asset_name == "Test Asset"
