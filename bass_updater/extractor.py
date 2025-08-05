"""Extract and identify files from Bass library archives."""
import os
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple
import shutil

from .config import PLATFORMS, TEMP_DIR


class ArchiveExtractor:
    """Extract and organize files from Bass library zip archives."""
    
    def __init__(self):
        self.temp_dir = TEMP_DIR
        
    def extract_archive(self, archive_path: Path, library_name: str) -> Dict[str, List[Path]]:
        """Extract archive and categorize files by platform.
        
        Args:
            archive_path: Path to zip file
            library_name: Name of the library (for organizing extracts)
            
        Returns:
            Dict mapping platform names to lists of extracted library files
        """
        extract_dir = self.temp_dir / f"{library_name}_extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        except zipfile.BadZipFile:
            raise RuntimeError(f"Corrupted zip file: {archive_path}")
            
        # Find and categorize library files
        return self._categorize_files(extract_dir, library_name)
        
    def _categorize_files(self, extract_dir: Path, library_name: str) -> Dict[str, List[Path]]:
        """Categorize extracted files by platform."""
        platform_files = {}
        
        # Walk through extracted files
        for root, dirs, files in os.walk(extract_dir):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                
                # Determine platform and file type
                platform = self._identify_platform(file_path, root_path, extract_dir)
                if platform and self._is_library_file(file_path, library_name):
                    if platform not in platform_files:
                        platform_files[platform] = []
                    platform_files[platform].append(file_path)
                    
        return platform_files
        
    def _identify_platform(self, file_path: Path, root_path: Path, extract_dir: Path) -> str:
        """Identify platform from file extension and directory structure."""
        suffix = file_path.suffix.lower()
        
        # Check for x64 directory structure (common in Bass archives)
        rel_path = root_path.relative_to(extract_dir)
        path_parts = [p.lower() for p in rel_path.parts]
        
        if suffix == '.dll':
            # Windows - check for x64 directory
            if 'x64' in path_parts or '64' in path_parts:
                return 'win64'
            else:
                return 'win32'
        elif suffix == '.so':
            return 'linux'
        elif suffix == '.dylib':
            return 'macos'
            
        return None
        
    def _is_library_file(self, file_path: Path, library_name: str) -> bool:
        """Check if file is a library file we want to keep."""
        filename = file_path.name.lower()
        
        # Common library file patterns for Bass libraries
        library_patterns = [
            library_name.lower(),
            library_name.lower().replace('_', ''),
            f"lib{library_name.lower()}",
            f"lib{library_name.lower().replace('_', '')}"
        ]
        
        # Check if filename starts with any library pattern
        for pattern in library_patterns:
            if filename.startswith(pattern):
                return True
                
        return False
        
    def cleanup_extraction(self, library_name: str):
        """Clean up extraction directory for a specific library."""
        extract_dir = self.temp_dir / f"{library_name}_extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)