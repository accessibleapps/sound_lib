"""Robust file downloader with progress and retry support."""
import os
import requests
from pathlib import Path
from typing import Optional, Callable
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from .config import (
    DOWNLOAD_TIMEOUT,
    MAX_RETRIES, 
    RETRY_BACKOFF_FACTOR,
    CHUNK_SIZE,
    TEMP_DIR
)


class Downloader:
    """Robust file downloader with progress tracking."""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_retries()
        
    def setup_retries(self):
        """Configure retry strategy for robust downloading."""
        retry_strategy = Retry(
            total=MAX_RETRIES,
            status_forcelist=[403, 429, 500, 502, 503, 504],
            backoff_factor=RETRY_BACKOFF_FACTOR,
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def download_file(self, url: str, filename: str, 
                     progress_callback: Optional[Callable] = None) -> Path:
        """Download a file with progress tracking.
        
        Args:
            url: URL to download from
            filename: Local filename to save as
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to downloaded file
            
        Raises:
            RuntimeError: If download fails
        """
        # Ensure temp directory exists
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        filepath = TEMP_DIR / filename
        
        try:
            response = self.session.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT)
            response.raise_for_status()
            
            # Get total size for progress bar
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                if total_size > 0:
                    # Download with progress bar
                    with tqdm(total=total_size, unit='B', unit_scale=True, 
                             desc=filename) as pbar:
                        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                                if progress_callback:
                                    progress_callback(len(chunk))
                else:
                    # Download without progress (unknown size)
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            
            return filepath
            
        except Exception as e:
            # Clean up partial download
            if filepath.exists():
                filepath.unlink()
            raise RuntimeError(f"Failed to download {url}: {e}")
            
    def cleanup_downloads(self):
        """Remove temporary download directory."""
        if TEMP_DIR.exists():
            import shutil
            shutil.rmtree(TEMP_DIR)