from pydantic import BaseModel, HttpUrl, RootModel
from typing import Optional, List, Dict
from ..enums.youtube_helper_enums import CaptionExtension


class YTDLPVideoFragment(BaseModel):
    """
    Represents a fragment of a YouTube video format.
    {
      "url": "https://i.ytimg.com/sb/sM_oHEWxlwU/storyboard3_L0/default.jpg?sqp=-oaymwENSDfyq4qpAwVwAcABBqLzl_8DBgiQ2sSxBg==&sigh=rs$AOn4CLCcJv077C0l4A2VNJ5HG5mC-peaLQ",
      "duration": 621.0
    }
    """

    url: HttpUrl
    duration: float


class YTDLPVideoHttpHeader(BaseModel):
    """
    Represents an HTTP header for a YouTube video format.
    {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-us,en;q=0.5",
      "Sec-Fetch-Mode": "navigate"
    }
    """

    User_Agent: str
    Accept: str
    Accept_Language: str
    Sec_Fetch_Mode: str


class YTDLPVideoFormat(BaseModel):
    """
    Represents a format of a YouTube video.
    
    This model contains detailed information about a specific format variant of a YouTube video,
    including resolution, codecs, bitrates, and other technical specifications.
    
    Used in:
    - youtube_helper.py: get_video_info method returns YTDLPVideoDetails which contains this model
    - Any other modules that need to work with YouTube video format details
    """

    format_id: str  # Unique identifier for this format
    format_note: str  # Human-readable description of the format
    ext: str  # File extension
    protocol: str  # Protocol used for streaming (http, https, etc.)
    acodec: str  # Audio codec
    vcodec: str  # Video codec
    url: HttpUrl  # URL to the video content
    width: int  # Width in pixels
    height: int  # Height in pixels
    fps: float  # Frames per second
    rows: int  # Number of rows in the storyboard
    columns: int  # Number of columns in the storyboard
    fragments: List[YTDLPVideoFragment]  # List of video fragments
    audio_ext: str  # Audio file extension
    video_ext: str  # Video file extension
    vbr: float  # Video bitrate
    abr: float  # Audio bitrate
    tbr: Optional[float]  # Total bitrate (video + audio)
    resolution: str  # Resolution as a string (e.g., "1080p")
    aspect_ratio: float  # Aspect ratio (width/height)
    filesize_approx: Optional[int]  # Approximate file size in bytes
    http_headers: YTDLPVideoHttpHeader  # HTTP headers for requests
    format: str  # Format description


class YTDLPThumbnail(BaseModel):
    """
    Represents a thumbnail of a YouTube video.
    {
      "url": "https://i.ytimg.com/vi/sM_oHEWxlwU/3.jpg",
      "preference": -37,
      "id": "0"
    },
    """

    url: HttpUrl
    preference: int
    id: str


class YTDLPCaption(BaseModel):
    """
    Represents a caption format for a specific language.
    Example:
    {
        "ext": "json3",
        "url": "https://www.youtube.com/api/timedtext?v=...",
        "name": "Arabic"
    }
    """
    ext: CaptionExtension
    url: HttpUrl
    name: str


class YoutubeCaptionTrack(RootModel):
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
    """
    root: Dict[str, List[YTDLPCaption]]


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
    """
    asr: Optional[int]
    filesize: Optional[int]
    format_id: str
    format_note: str
    source_preference: Optional[int]
    fps: Optional[int]
    audio_channels: Optional[int]
    height: Optional[int]
    quality: Optional[float]
    has_drm: bool
    tbr: Optional[float]
    filesize_approx: Optional[int]
    url: HttpUrl
    width: Optional[int]
    language: Optional[str]
    language_preference: Optional[int]
    preference: Optional[int]
    ext: str
    vcodec: str
    acodec: str
    dynamic_range: str
    container: str
    downloader_options: Dict[str, int]
    protocol: str
    video_ext: str
    audio_ext: str
    abr: float
    vbr: float
    resolution: str
    aspect_ratio: float
    http_headers: YTDLPVideoHttpHeader
    format: str


class YTDLPVideoDetails(BaseModel):
    """
    Represents the details of a YouTube video.
    """

    id: str
    title: str
    formats: List[YTDLPVideoFormat]
    thumbnails: List[YTDLPThumbnail]
    thumbnail: HttpUrl
    description: str
    channel_id: str
    channel_url: HttpUrl
    duration: int
    view_count: int
    average_rating: Optional[float] = None
    age_limit: int
    webpage_url: HttpUrl
    categories: List[str]
    tags: List[str]
    playable_in_embed: bool
    live_status: str
    release_timestamp: Optional[int] = None
    _format_sort_fields: List[str]
    automatic_captions: YTDLPAutomaticCaption
    subtitles: YTDLPSubtitle
    comment_count: Optional[int] = None
    chapters: Optional[List[Dict]] = None  # never found in the wild, always null
    heatmap: Optional[dict] = None
    like_count: int
    channel: str
    channel_follower_count: int
    uploader: str
    uploader_id: str
    uploader_url: HttpUrl
    upload_date: str
    timestamp: int
    availability: str
    original_url: HttpUrl
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    playlist: Optional[str] = None
    playlist_index: Optional[int] = None
    display_id: str
    fulltitle: str
    duration_string: str
    release_year: Optional[str] = None
    is_live: bool
    was_live: bool
    requested_subtitles: Optional[str] = None
    _has_drm: Optional[str] = None
    epoch: int
    requested_formats: Optional[List[YTDLPRequestedFormat]] = None
    format: str
    format_id: str
    ext: str
    protocol: str
    language: str
    format_note: str
    filesize_approx: int
    tbr: float
    width: int
    height: int
    resolution: str
    fps: int
    dynamic_range: str
    vcodec: str
    vbr: float
    stretched_ratio: Optional[str] = None
    aspect_ratio: float
    acodec: str
    abr: float
    asr: int
    audio_channels: int
