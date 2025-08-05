"""Parse version information from un4seen.com Bass page."""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from .config import BASS_PAGE_URL, BASS_LIBRARIES, DOWNLOAD_TIMEOUT


class VersionParser:
    """Parse version information from the Bass download page."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = DOWNLOAD_TIMEOUT
        
    def fetch_page(self) -> str:
        """Fetch the Bass download page HTML."""
        response = self.session.get(BASS_PAGE_URL)
        response.raise_for_status()
        return response.text
        
    def parse_versions(self, html: str) -> Dict[str, str]:
        """Parse version numbers from the HTML."""
        soup = BeautifulSoup(html, 'lxml')
        versions = {}
        
        # Parse main Bass version from "Version: 2.4.17" pattern
        main_version_match = re.search(r'Version:\s*([\d.]+)', html)
        if main_version_match:
            versions['bass'] = main_version_match.group(1)
            
        # Parse add-on versions from library name + version patterns
        for lib_key, (display_name, _, _) in BASS_LIBRARIES.items():
            if lib_key == 'bass':  # Already handled above
                continue
                
            # Look for patterns like "BASSOPUS 2.4.3" or "Tags 19"
            pattern = rf'<b>{re.escape(display_name)}</b>\s*([\d.]+)'
            match = re.search(pattern, html)
            if match:
                versions[lib_key] = match.group(1)
                
        return versions
        
    def get_current_versions(self) -> Dict[str, str]:
        """Get current versions from the website."""
        try:
            html = self.fetch_page()
            return self.parse_versions(html)
        except Exception as e:
            raise RuntimeError(f"Failed to parse versions: {e}")