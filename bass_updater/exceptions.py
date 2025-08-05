"""Custom exceptions for Bass updater."""

class BassUpdaterError(Exception):
    """Base exception for Bass updater errors."""
    pass

class VersionParseError(BassUpdaterError):
    """Error parsing version information."""
    pass

class DownloadError(BassUpdaterError):
    """Error downloading files."""
    pass

class ExtractionError(BassUpdaterError):
    """Error extracting archives."""
    pass

class InstallationError(BassUpdaterError):
    """Error installing files."""
    pass

class NetworkError(BassUpdaterError):
    """Network-related errors."""
    pass