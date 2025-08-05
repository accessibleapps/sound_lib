"""Track installed Bass library versions."""
import json
import os
from typing import Dict, Optional
from .config import VERSION_FILE


class VersionTracker:
    """Track and compare Bass library versions."""
    
    def __init__(self):
        self.version_file = VERSION_FILE
        
    def load_installed_versions(self) -> Dict[str, str]:
        """Load currently installed versions from disk."""
        if not self.version_file.exists():
            return {}
            
        try:
            with open(self.version_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
            
    def save_installed_versions(self, versions: Dict[str, str]) -> None:
        """Save installed versions to disk."""
        try:
            self.version_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.version_file, 'w') as f:
                json.dump(versions, f, indent=2, sort_keys=True)
        except IOError as e:
            raise RuntimeError(f"Failed to save versions: {e}")
            
    def get_updates_needed(self, current_versions: Dict[str, str]) -> Dict[str, tuple]:
        """Compare versions and return libraries that need updates.
        
        Returns:
            Dict mapping library name to (old_version, new_version) tuples
        """
        installed = self.load_installed_versions()
        updates_needed = {}
        
        for lib_name, new_version in current_versions.items():
            old_version = installed.get(lib_name)
            if old_version != new_version:
                updates_needed[lib_name] = (old_version, new_version)
                
        return updates_needed
        
    def mark_updated(self, library: str, version: str) -> None:
        """Mark a single library as updated to the specified version."""
        versions = self.load_installed_versions()
        versions[library] = version
        self.save_installed_versions(versions)