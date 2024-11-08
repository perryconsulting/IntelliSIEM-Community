import pytest
from src.python.asset_ingestion.base_plugin import AssetSourcePlugin

def test_abstract_class_instantiation():
    """Test that AssetSourcePlugin cannot be instantiated directly."""
    with pytest.raises(TypeError):
        # Trying to instantiate the abstract base class directly should raise a TypeError
        plugin = AssetSourcePlugin()

def test_subclass_without_implementation():
    """Test that a subclass without the required methods raises an error."""

    # Create a subclass without implementing the abstract methods
    class IncompletePlugin(AssetSourcePlugin):
        pass

    # Check that trying to instantiate an incomplete plugin raises an error
    with pytest.raises(TypeError):
        incomplete_plugin = IncompletePlugin()

def test_connect_method():
    """Test that the connect method is abstract and must be implemented."""

    # Create a subclass that does not implement the connect method
    class MissingConnectPlugin(AssetSourcePlugin):
        def fetch_assets(self):
            return []

    # Check that trying to instantiate the plugin without a connect method raises an error
    with pytest.raises(TypeError):
        plugin = MissingConnectPlugin()

def test_fetch_assets_method():
    """Test that the fetch_assets method is abstract and must be implemented."""

    # Create a subclass that does not implement fetch_assets method
    class MissingFetchPlugin(AssetSourcePlugin):
        def connect(self):
            pass

    # Check that trying to instantiate the plugin without a fetch_assets method raises an error
    with pytest.raises(TypeError):
        plugin = MissingFetchPlugin()

def test_disconnect_method():
    """Test that the disconnect method is abstract and must be implemented."""

    # Create a subclass that does not implement the disconnect method
    class MissingDisconnectPlugin(AssetSourcePlugin):
        def connect(self):
            pass
        def fetch_assets(self):
            return []

    # Check that trying to instantiate the plugin without a disconnect method raises an error
    with pytest.raises(TypeError):
        plugin = MissingDisconnectPlugin()

def test_subclass_compliance():
    """Test that a fully implemented subclass of AssetSourcePlugin does not raise errors."""

    # Define a mock subclass that implements all required methods
    class MockPlugin(AssetSourcePlugin):
        def connect(self):
            pass

        def fetch_assets(self):
            return []

        def disconnect(self):
            pass

    # Instantiate the mock subclass and confirm no errors are raised
    try:
        mock_plugin = MockPlugin()
    except TypeError as e:
        pytest.fail(f"Fully implemented subclass should not raise TypeError: {e}")

def test_multiple_incomplete_subclasses():
    """Test that various incomplete subclasses cannot be instantiated."""

    # Subclass without connect method
    class MissingConnectPlugin(AssetSourcePlugin):
        def fetch_assets(self):
            return []
        def disconnect(self):
            pass

    # Subclass without fetch_assets method
    class MissingFetchPlugin(AssetSourcePlugin):
        def connect(self):
            pass
        def disconnect(self):
            pass

    # Subclass without disconnect method
    class MissingDisconnectPlugin(AssetSourcePlugin):
        def connect(self):
            pass
        def fetch_assets(self):
            return []

    with pytest.raises(TypeError):
        MissingConnectPlugin()

    with pytest.raises(TypeError):
        MissingFetchPlugin()

    with pytest.raises(TypeError):
        MissingDisconnectPlugin()

import inspect

def test_method_docstrings():
    """Test that all methods in AssetSourcePlugin have docstrings."""
    for name, method in inspect.getmembers(AssetSourcePlugin, predicate=inspect.isfunction):
        assert method.__doc__, f"Method {name} is missing a docstring."

