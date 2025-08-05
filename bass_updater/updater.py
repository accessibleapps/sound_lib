"""Main Bass library updater orchestration."""
from typing import Dict, List, Optional
from pathlib import Path

from .config import BASS_LIBRARIES, FILES_BASE_URL, PLATFORMS
from .version_parser import VersionParser
from .version_tracker import VersionTracker  
from .downloader import Downloader
from .extractor import ArchiveExtractor
from .file_manager import FileManager


class BassUpdater:
    """Main orchestrator for Bass library updates."""
    
    def __init__(self):
        self.version_parser = VersionParser()
        self.version_tracker = VersionTracker()
        self.downloader = Downloader()
        self.extractor = ArchiveExtractor()
        self.file_manager = FileManager()
        
    def check_for_updates(self) -> Dict[str, tuple]:
        """Check which libraries have updates available.
        
        Returns:
            Dict mapping library name to (old_version, new_version) tuples
        """
        print("Checking for Bass library updates...")
        
        try:
            current_versions = self.version_parser.get_current_versions()
            updates_needed = self.version_tracker.get_updates_needed(current_versions)
            
            if updates_needed:
                print(f"Found {len(updates_needed)} libraries with updates:")
                for lib, (old, new) in updates_needed.items():
                    print(f"  {lib}: {old or 'not installed'} → {new}")
            else:
                print("All libraries are up to date.")
                
            return updates_needed
            
        except Exception as e:
            raise RuntimeError(f"Failed to check for updates: {e}")
            
    def update_library(self, library_name: str, new_version: str, 
                      platforms: Optional[List[str]] = None) -> bool:
        """Update a single library.
        
        Args:
            library_name: Name of library to update
            new_version: Version to update to
            platforms: List of platforms to update (default: all supported)
            
        Returns:
            True if update succeeded
        """
        if library_name not in BASS_LIBRARIES:
            raise ValueError(f"Unknown library: {library_name}")
            
        display_name, file_prefix, has_platform_suffix = BASS_LIBRARIES[library_name]
        
        if platforms is None:
            platforms = self._get_supported_platforms(library_name)
            
        print(f"Updating {display_name} to version {new_version}...")
        
        # Create backup before starting
        backup_dir = self.file_manager.create_backup(library_name)
        
        try:
            # Download and extract files for each platform
            all_platform_files = {}
            
            for platform in platforms:
                archive_path = self._download_platform_archive(
                    library_name, file_prefix, platform, has_platform_suffix
                )
                
                if archive_path:
                    platform_files = self.extractor.extract_archive(archive_path, library_name)
                    all_platform_files.update(platform_files)
                    
            if not all_platform_files:
                raise RuntimeError(f"No files found for {library_name}")
                
            # Install extracted files
            self.file_manager.install_files(all_platform_files, library_name)
            
            # Mark as updated
            self.version_tracker.mark_updated(library_name, new_version)
            
            # Clean up
            self.file_manager.cleanup_backup(backup_dir)
            self.extractor.cleanup_extraction(library_name)
            
            print(f"Successfully updated {display_name} to {new_version}")
            return True
            
        except Exception as e:
            print(f"Update failed for {display_name}: {e}")
            print("Restoring from backup...")
            
            try:
                self.file_manager.restore_from_backup(backup_dir)
                print("Restored from backup successfully")
            except Exception as restore_error:
                print(f"Backup restore also failed: {restore_error}")
                
            return False
            
    def update_all(self, dry_run: bool = False) -> Dict[str, bool]:
        """Update all libraries that have updates available.
        
        Args:
            dry_run: If True, only show what would be updated
            
        Returns:
            Dict mapping library name to update success status
        """
        updates_needed = self.check_for_updates()
        
        if not updates_needed:
            return {}
            
        if dry_run:
            print("DRY RUN - Would update:")
            for lib, (old, new) in updates_needed.items():
                print(f"  {lib}: {old or 'not installed'} → {new}")
            return {lib: True for lib in updates_needed}
            
        results = {}
        for library_name, (old_version, new_version) in updates_needed.items():
            success = self.update_library(library_name, new_version)
            results[library_name] = success
            
        return results
        
    def _download_platform_archive(self, library_name: str, file_prefix: str,
                                  platform: str, has_platform_suffix: bool) -> Optional[Path]:
        """Download archive for specific platform."""
        # Build download URL
        if has_platform_suffix and platform != 'win32':
            # Use platform suffix for non-Win32 platforms
            platform_suffix = PLATFORMS[platform][0]  # e.g., "-linux", "-osx"
            filename = f"{file_prefix}{platform_suffix}.zip"
        else:
            # No suffix (Win32 or libraries without platform suffixes)
            filename = f"{file_prefix}.zip"
            
        url = f"{FILES_BASE_URL}/{filename}"
        
        try:
            return self.downloader.download_file(url, filename)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            return None
            
    def _get_supported_platforms(self, library_name: str) -> List[str]:
        """Get list of platforms supported by a library."""
        # Some libraries are Windows-only
        windows_only = ['basswasapi', 'basswma']
        limited_platform = ['bass_aac', 'bass_alac']
        
        if library_name in windows_only:
            return ['win32', 'win64']
        elif library_name in limited_platform:
            return ['win32', 'win64', 'linux']  # No macOS for these
        else:
            return ['win32', 'win64', 'linux', 'macos']
            
    def cleanup(self):
        """Clean up temporary files."""
        self.downloader.cleanup_downloads()
        # Extractor cleanup is handled per-library