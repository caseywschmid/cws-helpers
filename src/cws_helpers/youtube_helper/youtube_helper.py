# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
import pathlib
from typing import Optional, Any, Dict, List
from urllib import parse
from datetime import datetime, timezone
import yt_dlp
from yt_dlp.utils import ExtractorError, DownloadError

# Local imports
from .enums.youtube_helper_enums import CaptionExtension, CAPTION_FORMATS
from .models.youtube_helper_models import (
    YTDLPVideoDetails,
    YTDLPCaption,
    YTDLPAutomaticCaption,
    YTDLPSubtitle,
)

# ------------------ Constants ------------------ #
DEFAULT_YDL_OPTIONS: Dict[str, Any] = {
    'format': 'best',
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'ignoreerrors': False,
}

# ------------------ Custom Exceptions ------------------ #
class YouTubeVideoUnavailable(DownloadError):
    """Raised when a YouTube video is not available."""
    pass

class YTOAuthTokenExpired(DownloadError):
    """Raised when the YouTube OAuth token has expired."""
    pass

class YoutubeHelper():
    # List of valid YouTube domains
    VALID_DOMAINS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com"
    }

    # List of valid path prefixes that contain video IDs
    VALID_VIDEO_PATHS = {
        "v",
        "embed",
        "shorts",
        "live",
        "e"
    }

    # List of paths that can contain video IDs but need additional validation
    SPECIAL_PATHS = {
        "watch"  # watch paths need either a v parameter or a direct video ID
    }
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the YoutubeHelper with custom options.
        
        This constructor allows you to customize the behavior of yt_dlp by providing
        your own options dictionary. Any provided options will be merged with the default
        options, with your custom options taking precedence.
        
        Args:
            options (Optional[Dict[str, Any]]): Custom options to pass to yt_dlp.
                                               These will be merged with the default options.
        
        Example:
            ```python
            # Initialize with default options
            helper = YoutubeHelper()
            
            # Initialize with custom options
            helper = YoutubeHelper({
                'format': 'bestvideo+bestaudio',
                'writesubtitles': True,
                'subtitleslangs': ['en', 'es']
            })
            ```
        """
        # Start with default options
        self.options = DEFAULT_YDL_OPTIONS.copy()
        
        # Update with any custom options
        if options:
            self.options.update(options)
            
        log.debug(f"Initialized YoutubeHelper with options: {self.options}")

    def is_valid_url(self, url: str) -> bool:
        """
        Validate if a given URL is a valid YouTube URL.
        This method checks the URL structure and ensures it contains a video ID.

        Args:
            url (str): The URL to validate

        Returns:
            bool: True if the URL is a valid YouTube URL with a video ID, False otherwise
        """
        if not url or not isinstance(url, str):
            return False

        try:
            # Parse the URL
            components = parse.urlparse(url)
            
            # Must have a hostname
            if not components.hostname:
                return False
                
            # Special case for ytimg.com - not a valid YouTube video URL
            if components.hostname.endswith("ytimg.com"):
                return False

            # Check if domain is valid
            base_domain = components.hostname.replace("m.", "").replace("www.", "")
            if base_domain not in self.VALID_DOMAINS:
                return False

            # Must have a path (even if it's just /)
            if not components.path:
                return False

            # Get the first path component
            path = pathlib.Path(components.path)
            if not path.parts:
                return False

            path_type = path.parts[1] if len(path.parts) > 1 else path.parts[0]
            queries = parse.parse_qs(components.query)
            
            # For youtu.be URLs, must have a non-empty path
            if base_domain == "youtu.be":
                return bool(path.name and len(path.name) > 0)
            
            # For watch URLs with v parameter
            if path_type == "watch" and 'v' in queries:
                return bool(queries['v'][0])  # v parameter must not be empty
            
            # For watch URLs with direct video ID
            if path_type == "watch" and len(path.parts) > 2:
                return bool(path.parts[-1])  # Must have a non-empty video ID
            
            # For other valid paths (shorts, live, etc)
            if path_type in self.VALID_VIDEO_PATHS and len(path.parts) > 1:
                return bool(path.parts[-1])  # Must have a non-empty video ID

            return False

        except Exception as e:
            log.error(f"Error validating YouTube URL {url}: {str(e)}")
            return False

    def get_video_info(self, url: str) -> YTDLPVideoDetails:
        """
        Fetches YouTube video information using yt_dlp and returns it as a YoutubeVideoDetails object.

        Args:
            url (str): The YouTube URL.

        Returns:
            YTDLPVideoDetails: An object containing video information.

        Raises:
            YouTubeVideoUnavailable: If the video is not available.
            YTOAuthTokenExpired: If the OAuth token has expired.
            DownloadError: For other YouTube-DL related errors.
        """
        log.debug(f"Fetching video info for URL: {url}")
        try:
            with yt_dlp.YoutubeDL(self.options) as ydl:
                try:
                    result = ydl.extract_info(url, download=False)
                    if not result:
                        raise YouTubeVideoUnavailable("No video information returned")
                    return YTDLPVideoDetails.model_validate(self._extract_video_info(result))
                except yt_dlp.utils.UnavailableVideoError as e:
                    # Specific error for unavailable videos
                    log.error(f"Video unavailable: {str(e)}")
                    raise YouTubeVideoUnavailable(str(e))
                except yt_dlp.utils.GeoRestrictedError as e:
                    # Specific error for geo-restricted videos
                    log.error(f"Video geo-restricted: {str(e)}")
                    raise YouTubeVideoUnavailable(f"Video is geo-restricted: {str(e)}")
                except ExtractorError as e:
                    log.error(f"YouTube extractor error: {str(e)}")
                    error_msg = str(e)
                    if "Sign in to confirm you're not a bot" in error_msg:
                        log.error("OAuth token has expired")
                        raise YTOAuthTokenExpired("YouTube OAuth token has expired")
                    elif "Video unavailable" in error_msg:
                        log.error("Video is not available")
                        raise YouTubeVideoUnavailable("The YouTube video is not available")
                    elif "Private video" in error_msg:
                        log.error("Video is private")
                        raise YouTubeVideoUnavailable("The YouTube video is private")
                    else:
                        log.error(f"YouTube-DL error: {error_msg}")
                        raise YouTubeVideoUnavailable(error_msg)

        except (YouTubeVideoUnavailable, YTOAuthTokenExpired):
            raise
        except Exception as e:
            log.error(f"Unexpected error: {str(e)}")
            raise YouTubeVideoUnavailable(f"Unexpected error: {str(e)}")

    def _extract_video_info(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts relevant video information from the YouTube API result.

        Args:
            result (Dict[str, Any]): The raw result dictionary from yt-dlp.

        Returns:
            Dict[str, Any]: A dictionary containing formatted video information.
        """
        log.debug("Extracting video information from result")
        
        # Convert timestamp to datetime if present
        timestamp = result.get("timestamp")
        published_at = (
            datetime.fromtimestamp(timestamp, tz=timezone.utc)
            if timestamp else None
        )

        # Extract basic video information
        video_info = {
            "title": result.get("title", "No Video Title"),
            "duration": result.get("duration", 0),
            "youtube_id": result.get("id", "No Video ID"),
            "channel": result.get("channel", "No Channel"),
            "description": result.get("description", "No Video Description"),
            "video_url": result.get("original_url", "No Video URL"),
            "index": result.get("playlist_index"),
            "view_count": result.get("view_count", 0),
            "like_count": result.get("like_count", 0),
            "channel_follower_count": result.get("channel_follower_count", 0),
            "published_at": published_at,
            
            # Captions
            "automatic_captions": YTDLPAutomaticCaption.model_validate(result.get("automatic_captions", {})),
            "subtitles": YTDLPSubtitle.model_validate(result.get("subtitles", {})),
            
            # Additional metadata
            "thumbnail": result.get("thumbnail"),
            "tags": result.get("tags", []),
            "categories": result.get("categories", []),
            "is_live": result.get("is_live", False),
            "was_live": result.get("was_live", False),
            "age_restricted": result.get("age_restricted", False),
        }
        
        # Add all remaining fields from the result
        video_info.update({
            k: v for k, v in result.items() 
            if k not in video_info and not k.startswith('_')
        })
        
        return video_info

    def _extract_captions(self, result: Dict[str, Any]) -> Dict[str, List[YTDLPCaption]]:
        """
        Extracts caption information from the video result.

        Args:
            result (Dict[str, Any]): The raw result dictionary from yt-dlp.

        Returns:
            Dict[str, List[YoutubeCaption]]: A dictionary mapping language codes to lists of caption formats.
        """
        log.debug("Extracting caption information")
        captions: Dict[str, List[YTDLPCaption]] = {}

        # Try automatic captions first
        automatic_captions = result.get("automatic_captions", {})
        regular_captions = result.get("subtitles", {})

        # Define caption format preferences with language names
        caption_preferences = [
            ("en-orig", CAPTION_FORMATS, "English (Original)"),
            ("en", CAPTION_FORMATS, "English"),
        ]

        # Try both automatic and regular captions
        for captions_dict in [automatic_captions, regular_captions]:
            for lang_code, formats, lang_name in caption_preferences:
                caption_set = captions_dict.get(lang_code, [])
                current_captions: List[YTDLPCaption] = []
                
                for caption in caption_set:
                    caption_ext = caption.get("ext")
                    caption_protocol = caption.get("protocol")
                    
                    # Try to convert the extension to our enum
                    try:
                        ext = CaptionExtension(caption_ext) if caption_ext else None
                    except ValueError:
                        # Skip if the extension is not in our supported formats
                        continue

                    if ext in formats or caption_protocol in [f.value for f in formats]:
                        caption_info = YTDLPCaption(
                            ext=ext,
                            url=caption.get("url"),
                            name=caption.get("name", lang_name)
                        )
                        current_captions.append(caption_info)
                        # Found a matching caption, no need to check other formats
                        break
                
                if current_captions:
                    captions[lang_code] = current_captions

        return captions

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract the video ID from various YouTube URL formats.
        This works for all URL formats listed in the documentation.

        Args:
            url (str): The YouTube URL to extract the video ID from.

        Returns:
            Optional[str]: The video ID if found and valid, None otherwise.
        """
        if not url or not isinstance(url, str):
            return None

        try:
            # Handle URLs with & before ?
            normalized_url = url.replace("&", "?", 1) if "?" not in url else url
            components = parse.urlparse(normalized_url)
            
            # Validate domain
            if not components.hostname:
                return None
                
            # Special case for ytimg.com
            if components.hostname.endswith("ytimg.com"):
                try:
                    return pathlib.Path(components.path).parts[2]
                except (IndexError, AttributeError):
                    return None

            # Validate YouTube domain
            base_domain = components.hostname.replace("m.", "").replace("www.", "")
            if base_domain not in {"youtube.com", "youtu.be", "youtube-nocookie.com"}:
                return None

            # Parse query parameters
            queries = parse.parse_qs(components.query)

            # Handle oembed URLs
            if components.path == "/oembed" and "url" in queries:
                try:
                    embedded_url = parse.unquote(queries["url"][0])
                    return self.extract_video_id(embedded_url)
                except (KeyError, IndexError):
                    return None
            
            # Handle attribution links
            if components.path == "/attribution_link" and "u" in queries:
                try:
                    # Extract the encoded URL and parse it
                    encoded_url = queries["u"][0]
                    # Handle both URL-encoded and partially encoded URLs
                    if encoded_url.startswith('/'):
                        # Handle relative URLs
                        encoded_url = f"https://youtube.com{encoded_url}"
                    decoded_url = parse.unquote(encoded_url)
                    # Convert encoded parameters to proper URL
                    decoded_url = decoded_url.replace("%3D", "=").replace("%26", "&")
                    return self.extract_video_id(decoded_url)
                except (KeyError, IndexError):
                    return None

            # Check for video ID in query parameter
            if 'v' in queries:
                return queries['v'][0]

            # Handle direct video paths (shorts, live, etc.)
            path = pathlib.Path(components.path)
            if not path.parts:
                return None

            # Get the first path component
            path_type = path.parts[1] if len(path.parts) > 1 else path.parts[0]
            
            # For youtu.be URLs, the video ID is the path
            if base_domain == "youtu.be":
                return path.name if path.name else None
                
            # For other URLs, validate the path type
            if path_type in self.VALID_VIDEO_PATHS and len(path.parts) > 1:
                return path.parts[-1]
                
            # Handle special paths that need additional validation
            if path_type in self.SPECIAL_PATHS:
                # For watch paths, we need either a v parameter (handled above) or a direct video ID
                if path_type == "watch" and len(path.parts) > 2:
                    return path.parts[-1]
                return None

            return None

        except Exception as e:
            log.error(f"Error extracting video ID from URL {url}: {str(e)}")
            return None

    def list_available_captions(self, url: str) -> Dict[str, List[CaptionExtension]]:
        """
        List available captions for a YouTube video.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            Dict[str, List[CaptionExtension]]: A dictionary mapping language codes to lists of available caption formats.
            Example:
            ```
            {
                'en': [CaptionExtension.VTT, CaptionExtension.SRV1],
                'es': [CaptionExtension.VTT]
            }
            ```
        """
        log.debug(f"Listing available captions for URL: {url}")
        
        # Check if the URL is valid
        if not self.is_valid_url(url):
            log.warning(f"Invalid YouTube URL: {url}")
            return {}
        
        try:
            # Get video info
            video_info = self.get_video_info(url)
            
            # Combine automatic captions and regular subtitles
            result: Dict[str, List[CaptionExtension]] = {}
            
            # Process automatic captions
            for lang_code, captions in video_info.automatic_captions.root.items():
                # Add 'auto-' prefix to distinguish automatic captions
                auto_lang_code = f"auto-{lang_code}"
                if auto_lang_code not in result:
                    result[auto_lang_code] = []
                
                for caption in captions:
                    if caption.ext not in result[auto_lang_code]:
                        result[auto_lang_code].append(caption.ext)
            
            # Process regular subtitles
            for lang_code, captions in video_info.subtitles.root.items():
                if lang_code not in result:
                    result[lang_code] = []
                
                for caption in captions:
                    if caption.ext not in result[lang_code]:
                        result[lang_code].append(caption.ext)
            
            return result
        except YouTubeVideoUnavailable:
            log.warning(f"Video unavailable: {url}")
            return {}
