"""Tests for version tracker."""
import json
import tempfile
from pathlib import Path
from bass_updater.version_tracker import VersionTracker

class TestVersionTracker:
    def test_empty_version_file(self):
        tracker = VersionTracker()
        # Use non-existent file
        tracker.version_file = Path("/tmp/nonexistent.json")
        versions = tracker.load_installed_versions()
        assert versions == {}
        
    def test_save_and_load_versions(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tracker = VersionTracker()
            tracker.version_file = Path(f.name)
            
            test_versions = {"bass": "2.4.17", "bassopus": "2.4.3"}
            tracker.save_installed_versions(test_versions)
            
            loaded = tracker.load_installed_versions()
            assert loaded == test_versions
            
    def test_get_updates_needed(self):
        tracker = VersionTracker()
        # Mock installed versions
        tracker.load_installed_versions = lambda: {"bass": "2.4.16", "bassopus": "2.4.3"}
        
        current_versions = {"bass": "2.4.17", "bassopus": "2.4.3", "bassflac": "2.4.5"}
        updates = tracker.get_updates_needed(current_versions)
        
        assert "bass" in updates
        assert updates["bass"] == ("2.4.16", "2.4.17")
        assert "bassopus" not in updates  # Same version
        assert "bassflac" in updates
        assert updates["bassflac"] == (None, "2.4.5")  # New library