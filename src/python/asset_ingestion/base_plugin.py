from abc import ABC, abstractmethod

class AssetSourcePlugin(ABC):
    """Abstract base class for asset ingestion plugins.

    This class defines the basic interface for any plugin used to fetch asset data
    from various sources (e.g., Tenable, Nmap, or CSV). Any subclass must implement
    the following methods: `connect`, `fetch_assets`, and `disconnect`.

    Attributes:
        None
    """

    @abstractmethod
    def connect(self):
        """Establishes a connection to the asset source.

        This method should implement the logic for connecting to the asset source,
        such as setting up API connections or preparing file reads. It should raise
        appropriate exceptions if the connection cannot be established.

        Raises:
            ValueError: If the connection fails due to missing configuration or credentials.
        """
        pass

    @abstractmethod
    def fetch_assets(self):
        """Fetches asset data from the source.

        Returns:
            list: A list of assets, each represented as a dictionary containing fields like
                  "id", "hostname", "ip_address", etc.

        Raises:
            Exception: If the data fetching fails due to connection issues or invalid data format.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnects from the asset source.

        This method should close any active connections to the asset source, such as
        API sessions or file handles.
        """
        pass
