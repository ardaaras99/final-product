import final_product


def test_import() -> None:
    """Test that the package can be imported without errors."""
    assert isinstance(final_product.__name__, str)
