"""Tests for version parser."""
import pytest
from unittest.mock import Mock, patch
from bass_updater.version_parser import VersionParser

class TestVersionParser:
    def test_parse_main_bass_version(self):
        html = '<h3><span>Download: <a href="files/bass24.zip">Win32</a></span>Version: 2.4.17</h3>'
        parser = VersionParser()
        versions = parser.parse_versions(html)
        assert versions['bass'] == '2.4.17'
        
    def test_parse_addon_versions(self):
        html = '<h3><span><a href="files/bassopus24.zip">Win32</a></span><b>BASSOPUS</b> 2.4.3</h3>'
        parser = VersionParser()
        versions = parser.parse_versions(html)
        assert versions.get('bassopus') == '2.4.3'
        
    @patch('requests.Session.get')
    def test_fetch_page_error_handling(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        parser = VersionParser()
        
        with pytest.raises(RuntimeError):
            parser.get_current_versions()