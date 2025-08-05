"""Configuration for Bass library updater."""
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Library directories
LIB_DIR = PROJECT_ROOT / "sound_lib" / "lib"
X86_DIR = LIB_DIR / "x86" 
X64_DIR = LIB_DIR / "x64"

# Version tracking file
VERSION_FILE = PROJECT_ROOT / "bass_versions.json"

# Un4seen website configuration
BASS_BASE_URL = "https://www.un4seen.com"
BASS_PAGE_URL = f"{BASS_BASE_URL}/bass.html"
FILES_BASE_URL = f"{BASS_BASE_URL}/files"

# Library definitions: (display_name, file_prefix, has_platform_suffix)
BASS_LIBRARIES = {
    "bass": ("BASS", "bass24", True),
    "bassopus": ("BASSOPUS", "bassopus24", True), 
    "bassflac": ("BASSFLAC", "bassflac24", True),
    "bassmidi": ("BASSMIDI", "bassmidi24", True),
    "bassmix": ("BASSmix", "bassmix24", True),
    "bassenc": ("BASSenc", "bassenc24", True),
    "basswasapi": ("BASSWASAPI", "basswasapi24", False),  # Windows only
    "basswma": ("BASSWMA", "basswm24", False),  # Windows only
    "bass_aac": ("BASS_AAC", "bass_aac24", False),  # Some platforms
    "bass_alac": ("BASSALAC", "bassalac24", False),  # Some platforms  
    "bass_fx": ("BASS FX", "bass_fx24", True),
    "tags": ("Tags", "tags19", True)
}

# Platform mappings: (un4seen_suffix, our_directory, file_extensions)
PLATFORMS = {
    "win32": ("", X86_DIR, [".dll"]),
    "win64": ("", X64_DIR, [".dll"]), 
    "linux": ("-linux", X64_DIR, [".so"]),
    "macos": ("-osx", X64_DIR, [".dylib"])
}

# Download settings
DOWNLOAD_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 1
CHUNK_SIZE = 8192

# Temp directory for downloads
TEMP_DIR = PROJECT_ROOT / "temp_bass_update"