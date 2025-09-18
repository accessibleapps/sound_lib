"""Bass library auto-updater package."""
from .updater import BassUpdater
from .version_parser import VersionParser
from .version_tracker import VersionTracker

__version__ = "1.0.0"
__all__ = ["BassUpdater", "VersionParser", "VersionTracker"]