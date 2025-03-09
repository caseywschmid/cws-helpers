"""
Enums related to YouTube functionality.

This module contains enums used across the YouTube-related functionality in the application.
Each enum is documented with its purpose and usage locations.
"""

from enum import Enum

class CaptionExtension(str, Enum):
    """
    Enumeration of supported YouTube caption extensions.
    
    Used in:
    - helpers/youtube_helper.py: CaptionInfo type and _extract_captions method
    - Any other modules that need to handle YouTube caption formats
    
    The string values correspond to the extension formats returned by the YouTube API
    and yt-dlp library.
    """
    JSON3 = "json3"  # JSON format version 3
    SRV1 = "srv1"    # SubRip format version 1
    SRV2 = "srv2"    # SubRip format version 2
    SRV3 = "srv3"    # SubRip format version 3
    TTML = "ttml"    # Timed Text Markup Language
    VTT = "vtt"      # WebVTT (Web Video Text Tracks)
    M3U8 = "m3u8_native"  # HLS manifest format

# Set of supported caption formats for easy validation
CAPTION_FORMATS = {
    CaptionExtension.TTML,
    CaptionExtension.VTT,
    CaptionExtension.SRV1,
    CaptionExtension.M3U8,
} 