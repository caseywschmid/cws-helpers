from pydantic import BaseModel, HttpUrl, RootModel
from typing import Optional, List, Dict, Any
from ..enums.youtube_helper_enums import CaptionExtension


class YTDLPVideoFragment(BaseModel):
    """
    Represents a fragment of a YouTube video format.
    {
      "url": "https://i.ytimg.com/sb/sM_oHEWxlwU/storyboard3_L0/default.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgiQ2sSxBg==&sigh=rs$AOn4CLCcJv077C0l4A2VNJ5HG5mC-peaLQ",
      "duration": 621.0
    }
    
    Note: Fields are made optional to handle different fragment structures returned by yt-dlp.
    """

    url: Optional[str] = None
    duration: Optional[float] = 0.0
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPVideoHttpHeader(BaseModel):
    """
    Represents an HTTP header for a YouTube video format.
    {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-us,en;q=0.5",
      "Sec-Fetch-Mode": "navigate"
    }
    
    Note: These fields are made optional to handle different header formats returned by yt-dlp.
    """

    User_Agent: Optional[str] = None
    Accept: Optional[str] = None
    Accept_Language: Optional[str] = None
    Sec_Fetch_Mode: Optional[str] = None
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPVideoFormat(BaseModel):
    """
    Represents a format of a YouTube video.
    
    This model contains detailed information about a specific format variant of a YouTube video,
    including resolution, codecs, bitrates, and other technical specifications.
    
    Used in:
    - youtube_helper.py: get_video_info method returns YTDLPVideoDetails which contains this model
    - Any other modules that need to work with YouTube video format details
    
    Note: Many fields are made optional to handle different format structures returned by yt-dlp.
    """

    format_id: str  # Unique identifier for this format
    format_note: Optional[str] = None  # Human-readable description of the format
    ext: Optional[str] = None  # File extension
    protocol: Optional[str] = None  # Protocol used for streaming (http, https, etc.)
    acodec: Optional[str] = None  # Audio codec
    vcodec: Optional[str] = None  # Video codec
    url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    width: Optional[int] = None  # Width in pixels
    height: Optional[int] = None  # Height in pixels
    fps: Optional[float] = None  # Frames per second
    rows: Optional[int] = None  # Number of rows in the storyboard
    columns: Optional[int] = None  # Number of columns in the storyboard
    fragments: Optional[List[YTDLPVideoFragment]] = None  # List of video fragments
    audio_ext: Optional[str] = None  # Audio file extension
    video_ext: Optional[str] = None  # Video file extension
    vbr: Optional[float] = None  # Video bitrate
    abr: Optional[float] = None  # Audio bitrate
    tbr: Optional[float] = None  # Total bitrate (video + audio)
    resolution: Optional[str] = None  # Resolution as a string (e.g., "1080p")
    aspect_ratio: Optional[float] = None  # Aspect ratio (width/height)
    filesize_approx: Optional[int] = None  # Approximate file size in bytes
    http_headers: Optional[YTDLPVideoHttpHeader] = None  # HTTP headers for requests
    format: Optional[str] = None  # Format description
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPThumbnail(BaseModel):
    """
    Represents a thumbnail of a YouTube video.
    {
      "url": "https://i.ytimg.com/vi/sM_oHEWxlwU/3.jpg",
      "preference": -37,
      "id": "0"
    },
    
    Note: Fields are made optional to handle different thumbnail structures returned by yt-dlp.
    """

    url: str  # Changed from HttpUrl to str for more flexibility
    preference: Optional[int] = 0
    id: Optional[str] = "0"
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPCaption(BaseModel):
    """
    Represents a caption format for a specific language.
    Example:
    {
        "ext": "json3",
        "url": "https://www.youtube.com/api/timedtext?v=...",
        "name": "Arabic"
    }
    
    Note: Fields are made optional to handle different caption structures returned by yt-dlp.
    """
    ext: Optional[CaptionExtension] = None
    url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    name: Optional[str] = ""
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YoutubeCaptionTrack(BaseModel):
    """
    Represents a collection of caption formats for a specific language.
    The key is the language code (e.g., "ar", "en", "en-US").
    Example:
    {
        "ar": [
            {"ext": "json3", "url": "...", "name": "Arabic"},
            {"ext": "srv1", "url": "...", "name": "Arabic"},
            ...
        ]
    }
    
    Note: Changed from RootModel to BaseModel with a root field for more flexibility.
    """
    root: Optional[Dict[str, List[YTDLPCaption]]] = {}
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPAutomaticCaption(YoutubeCaptionTrack):
    """
    Represents automatically generated captions.
    Inherits from YoutubeCaptionTrack as it has the same structure.
    """
    pass


class YTDLPSubtitle(YoutubeCaptionTrack):
    """
    Represents manually created subtitles.
    Inherits from YoutubeCaptionTrack as it has the same structure.
    """
    pass


class YTDLPRequestedFormat(BaseModel):
    """
    Represents a requested format for a YouTube video.
    Example:
    {
        "asr": null,
        "filesize": 361422016,
        "format_id": "399",
        "format_note": "1080p",
        ...
    }
    
    Note: Many fields are made optional to handle different format structures returned by yt-dlp.
    """
    asr: Optional[int] = None
    filesize: Optional[int] = None
    format_id: str
    format_note: Optional[str] = None
    source_preference: Optional[int] = None
    fps: Optional[int] = None
    audio_channels: Optional[int] = None
    height: Optional[int] = None
    quality: Optional[float] = None
    has_drm: Optional[bool] = False
    tbr: Optional[float] = None
    filesize_approx: Optional[int] = None
    url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    width: Optional[int] = None
    language: Optional[str] = None
    language_preference: Optional[int] = None
    preference: Optional[int] = None
    ext: Optional[str] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    dynamic_range: Optional[str] = None
    container: Optional[str] = None
    downloader_options: Optional[Dict[str, int]] = None
    protocol: Optional[str] = None
    video_ext: Optional[str] = None
    audio_ext: Optional[str] = None
    abr: Optional[float] = None
    vbr: Optional[float] = None
    resolution: Optional[str] = None
    aspect_ratio: Optional[float] = None
    http_headers: Optional[YTDLPVideoHttpHeader] = None
    format: Optional[str] = None
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"


class YTDLPVideoDetails(BaseModel):
    """
    Represents the details of a YouTube video.
    
    Note: Many fields are made optional to handle different data structures returned by yt-dlp.
    """

    id: str
    title: str
    formats: Optional[List[YTDLPVideoFormat]] = []
    thumbnails: Optional[List[YTDLPThumbnail]] = []
    thumbnail: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    description: Optional[str] = ""
    channel_id: Optional[str] = ""
    channel_url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    duration: Optional[int] = 0
    view_count: Optional[int] = 0
    average_rating: Optional[float] = None
    age_limit: Optional[int] = 0
    webpage_url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    categories: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    playable_in_embed: Optional[bool] = True
    live_status: Optional[str] = "not_live"
    release_timestamp: Optional[int] = None
    _format_sort_fields: Optional[List[str]] = []
    automatic_captions: Optional[YTDLPAutomaticCaption] = None
    subtitles: Optional[YTDLPSubtitle] = None
    comment_count: Optional[int] = None
    chapters: Optional[List[Dict]] = None
    heatmap: Optional[Any] = None  # Changed from dict to Any to handle both dict and list
    like_count: Optional[int] = 0
    channel: Optional[str] = ""
    channel_follower_count: Optional[int] = 0
    uploader: Optional[str] = ""
    uploader_id: Optional[str] = ""
    uploader_url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    upload_date: Optional[str] = ""
    timestamp: Optional[int] = 0
    availability: Optional[str] = ""
    original_url: Optional[str] = None  # Changed from HttpUrl to str for more flexibility
    webpage_url_basename: Optional[str] = ""
    webpage_url_domain: Optional[str] = ""
    extractor: Optional[str] = ""
    extractor_key: Optional[str] = ""
    playlist: Optional[str] = None
    playlist_index: Optional[int] = None
    display_id: Optional[str] = ""
    fulltitle: Optional[str] = ""
    duration_string: Optional[str] = ""
    release_year: Optional[str] = None
    is_live: Optional[bool] = False
    was_live: Optional[bool] = False
    requested_subtitles: Optional[str] = None
    _has_drm: Optional[str] = None
    epoch: Optional[int] = 0
    requested_formats: Optional[List[YTDLPRequestedFormat]] = None
    format: Optional[str] = ""
    format_id: Optional[str] = ""
    ext: Optional[str] = ""
    protocol: Optional[str] = ""
    language: Optional[str] = ""
    format_note: Optional[str] = ""
    filesize_approx: Optional[int] = 0
    tbr: Optional[float] = 0.0
    width: Optional[int] = 0
    height: Optional[int] = 0
    resolution: Optional[str] = ""
    fps: Optional[int] = 0
    dynamic_range: Optional[str] = ""
    vcodec: Optional[str] = ""
    vbr: Optional[float] = 0.0
    stretched_ratio: Optional[str] = None
    aspect_ratio: Optional[float] = 0.0
    acodec: Optional[str] = ""
    abr: Optional[float] = 0.0
    asr: Optional[int] = 0
    audio_channels: Optional[int] = 0
    
    # Allow additional fields to be included
    class Config:
        extra = "allow"
