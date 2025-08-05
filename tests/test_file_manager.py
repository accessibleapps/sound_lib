"""Tests for file manager."""
import tempfile
import shutil
from pathlib import Path
from bass_updater.file_manager import FileManager

class TestFileManager:
    def test_get_target_directory(self):
        manager = FileManager()
        
        # Mock the directory paths for testing
        x86_dir = Path("/tmp/test_x86")
        x64_dir = Path("/tmp/test_x64")
        
        # Patch the config directories
        import bass_updater.file_manager
        bass_updater.file_manager.X86_DIR = x86_dir
        bass_updater.file_manager.X64_DIR = x64_dir
        
        assert manager._get_target_directory('win32') == x86_dir
        assert manager._get_target_directory('win64') == x64_dir  
        assert manager._get_target_directory('linux') == x64_dir
        assert manager._get_target_directory('macos') == x64_dir
        
    def test_is_library_file(self):
        manager = FileManager()
        
        # Test various file naming patterns
        assert manager._is_library_file(Path("bass.dll"), "bass")
        assert manager._is_library_file(Path("libbass.so"), "bass")
        assert manager._is_library_file(Path("bassopus.dll"), "bassopus")
        assert manager._is_library_file(Path("bass_fx.dll"), "bass_fx")
        
        # Test non-matching files
        assert not manager._is_library_file(Path("something_else.dll"), "bass")
        assert not manager._is_library_file(Path("readme.txt"), "bass")