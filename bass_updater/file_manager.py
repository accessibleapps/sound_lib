"""Manage Bass library file placement and backup."""
import os
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from .config import X86_DIR, X64_DIR, PLATFORMS


class FileManager:
    """Manage Bass library file installation and backup."""
    
    def __init__(self):
        self.backup_dir = None
        
    def create_backup(self, library_name: str) -> Path:
        """Create backup of current library files before update."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"bass_backup_{library_name}_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup files from both x86 and x64 directories
        for platform_dir in [X86_DIR, X64_DIR]:
            if platform_dir.exists():
                platform_backup = backup_dir / platform_dir.name
                platform_backup.mkdir(exist_ok=True)
                
                # Find and backup library files
                for file_path in platform_dir.glob("*"):
                    if self._is_library_file(file_path, library_name):
                        shutil.copy2(file_path, platform_backup)
                        
        self.backup_dir = backup_dir
        return backup_dir
        
    def install_files(self, platform_files: Dict[str, List[Path]], library_name: str):
        """Install extracted files to appropriate directories.
        
        Args:
            platform_files: Dict mapping platform to list of library files
            library_name: Name of the library being installed
        """
        installed_files = []
        
        try:
            for platform, files in platform_files.items():
                target_dir = self._get_target_directory(platform)
                if not target_dir:
                    continue
                    
                # Ensure target directory exists
                target_dir.mkdir(parents=True, exist_ok=True)
                
                for file_path in files:
                    target_file = target_dir / file_path.name
                    
                    # Copy file to target location
                    shutil.copy2(file_path, target_file)
                    installed_files.append(target_file)
                    print(f"Installed: {target_file}")
                    
        except Exception as e:
            # Rollback on failure
            self._rollback_installation(installed_files)
            raise RuntimeError(f"Failed to install {library_name}: {e}")
            
    def _get_target_directory(self, platform: str) -> Path:
        """Get target directory for platform."""
        platform_mapping = {
            'win32': X86_DIR,
            'win64': X64_DIR,
            'linux': X64_DIR,  # Assume 64-bit Linux
            'macos': X64_DIR   # Assume 64-bit macOS
        }
        return platform_mapping.get(platform)
        
    def _is_library_file(self, file_path: Path, library_name: str) -> bool:
        """Check if file belongs to the specified library."""
        filename = file_path.name.lower()
        
        # Common naming patterns for Bass libraries
        patterns = [
            library_name.lower(),
            library_name.lower().replace('_', ''),
            f"lib{library_name.lower()}",
            f"lib{library_name.lower().replace('_', '')}"
        ]
        
        return any(filename.startswith(pattern) for pattern in patterns)
        
    def _rollback_installation(self, installed_files: List[Path]):
        """Remove files that were installed during failed installation."""
        for file_path in installed_files:
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"Rolled back: {file_path}")
                except OSError:
                    pass  # Best effort rollback
                    
    def restore_from_backup(self, backup_dir: Path):
        """Restore files from backup directory."""
        if not backup_dir.exists():
            return
            
        for platform_backup in backup_dir.iterdir():
            if platform_backup.is_dir():
                # Determine target directory
                if platform_backup.name == 'x86':
                    target_dir = X86_DIR
                elif platform_backup.name == 'x64':
                    target_dir = X64_DIR
                else:
                    continue
                    
                # Restore files
                for backup_file in platform_backup.iterdir():
                    if backup_file.is_file():
                        target_file = target_dir / backup_file.name
                        shutil.copy2(backup_file, target_file)
                        print(f"Restored: {target_file}")
                        
    def cleanup_backup(self, backup_dir: Path):
        """Remove backup directory after successful installation."""
        if backup_dir and backup_dir.exists():
            shutil.rmtree(backup_dir)