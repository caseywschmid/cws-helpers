# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
import pathlib
from typing import Optional, Any, Dict, List
from urllib import parse
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
        log.debug("is_valid_url")
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

    def get_video_info(self, url: str, download_options: Optional[Dict[str, Any]] = None) -> YTDLPVideoDetails:
        """
        Get detailed information about a YouTube video.

        Args:
            url (str): The URL of the YouTube video.
            download_options (Optional[Dict[str, Any]]): Optional custom download options to override defaults.

        Returns:
            YTDLPVideoDetails: A model containing detailed information about the video.

        Raises:
            YouTubeVideoUnavailable: If the video is not available.
            YTOAuthTokenExpired: If the OAuth token has expired.
            Exception: For other errors.
        """
        log.debug("get_video_info")
        
        # Use custom download options if provided, otherwise use default options
        options = download_options if download_options is not None else self.options
        
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                try:
                    result = ydl.extract_info(url, download=False)
                    if not result:
                        raise YouTubeVideoUnavailable("No video information returned")
                    
                    # Extract the video info
                    video_info = self._extract_video_info(result)
                    
                    try:
                        # Process automatic captions and subtitles for model validation
                        auto_captions = video_info.get("automatic_captions", {})
                        subtitles = video_info.get("subtitles", {})
                        
                        # Validate the caption models first
                        validated_auto_captions = YTDLPAutomaticCaption.model_validate(auto_captions)
                        validated_subtitles = YTDLPSubtitle.model_validate(subtitles)
                        
                        # Update the video info with validated caption models
                        video_info["automatic_captions"] = validated_auto_captions
                        video_info["subtitles"] = validated_subtitles
                        
                        # Now validate the full video details
                        return YTDLPVideoDetails.model_validate(video_info)
                    except Exception as validation_error:
                        # Log the validation error with more details for debugging
                        log.warning(f"Validation error for video {url}: {str(validation_error)}")
                        
                        # Create a simplified version of the video info with only essential fields
                        # This is more maintainable than the previous approach
                        simplified_info = {
                            "id": video_info.get("youtube_id", "unknown_id"),
                            "title": video_info.get("title", "Unknown Title"),
                            # Empty collections to avoid validation errors
                            "formats": [],
                            "thumbnails": [],
                            # Add automatic captions and subtitles as empty objects
                            "automatic_captions": YTDLPAutomaticCaption.model_validate({"root": {}}),
                            "subtitles": YTDLPSubtitle.model_validate({"root": {}}),
                        }
                        
                        # Copy over any fields that exist in video_info with default values for missing fields
                        # This is more maintainable than listing every field explicitly
                        for field_name in YTDLPVideoDetails.__annotations__:
                            if field_name not in simplified_info and field_name in video_info:
                                simplified_info[field_name] = video_info[field_name]
                        
                        # Try to validate the simplified info
                        return YTDLPVideoDetails.model_validate(simplified_info)
                        
                except yt_dlp.utils.DownloadError as e:
                    error_message = str(e)
                    if "Video unavailable" in error_message:
                        raise YouTubeVideoUnavailable(f"Video not available: {error_message}")
                    elif "This video is not available" in error_message:
                        raise YouTubeVideoUnavailable(f"Video not available: {error_message}")
                    elif "Sign in to confirm your age" in error_message:
                        raise YouTubeVideoUnavailable(f"Age-restricted video: {error_message}")
                    else:
                        raise YouTubeVideoUnavailable(f"Download error: {error_message}")
                except ExtractorError as e:
                    error_message = str(e)
                    if "Sign in to confirm you're not a bot" in error_message:
                        raise YTOAuthTokenExpired(f"OAuth token expired: {error_message}")
                    else:
                        raise YouTubeVideoUnavailable(f"Extractor error: {error_message}")
        except (YouTubeVideoUnavailable, YTOAuthTokenExpired):
            # Re-raise specific exceptions
            raise
        except Exception as e:
            # Log and convert other exceptions to YouTubeVideoUnavailable
            log.error(f"Error getting video info for {url}: {str(e)}")
            raise YouTubeVideoUnavailable(f"Unknown error: {str(e)}")

    def _extract_video_info(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant information from the yt-dlp result.

        Args:
            result (Dict[str, Any]): The raw result dictionary from yt-dlp.

        Returns:
            Dict[str, Any]: A dictionary containing the extracted video information.
        """
        log.debug("_extract_video_info")
        
        # Create a dictionary to hold the video information
        video_info = {}
        
        # Extract the YouTube ID
        video_info["youtube_id"] = result.get("id", "")
        
        # Extract basic video information
        video_info["id"] = result.get("id", "")
        video_info["title"] = result.get("title", "")
        video_info["formats"] = result.get("formats", [])
        video_info["thumbnails"] = result.get("thumbnails", [])
        
        # Process automatic captions and subtitles
        auto_captions = result.get("automatic_captions", {})
        subtitles = result.get("subtitles", {})
        
        # Process captions for model validation
        processed_auto_captions = self._process_captions_for_model(auto_captions)
        processed_subtitles = self._process_captions_for_model(subtitles)
        
        # Convert to the appropriate model types
        video_info["automatic_captions"] = YTDLPAutomaticCaption.model_validate(processed_auto_captions)
        video_info["subtitles"] = YTDLPSubtitle.model_validate(processed_subtitles)
        
        # Add all remaining fields from the result
        video_info.update({
            k: v for k, v in result.items() 
            if k not in video_info and not k.startswith('_')
        })
        
        return video_info
        
    def _process_captions_for_model(self, captions_dict: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Process captions dictionary from yt-dlp into a format suitable for our models.
        
        Args:
            captions_dict (Dict[str, List[Dict[str, Any]]]): Raw captions dictionary from yt-dlp
            
        Returns:
            Dict[str, Any]: Processed captions dictionary with proper structure for model validation
        """
        # Create a dictionary to hold processed captions
        processed_captions = {"root": {}}
        
        # Process each language in the captions dictionary
        for lang_code, caption_formats in captions_dict.items():
            if not caption_formats:
                continue
                
            # Create a list to hold processed caption formats for this language
            processed_formats = []
            
            # Process each caption format
            for caption_format in caption_formats:
                # Extract caption extension
                caption_ext = caption_format.get("ext")
                
                # Try to convert the extension to our enum
                try:
                    ext = CaptionExtension(caption_ext) if caption_ext else None
                except ValueError:
                    # Use the string value if not in our enum
                    ext = caption_ext
                
                # Create a caption object
                caption_info = {
                    "ext": ext,
                    "url": caption_format.get("url"),
                    "name": caption_format.get("name", f"Caption for {lang_code}")
                }
                
                # Add any other fields from the original caption format
                for key, value in caption_format.items():
                    if key not in caption_info:
                        caption_info[key] = value
                
                # Add the processed caption format to the list
                processed_formats.append(caption_info)
            
            # Add the processed formats to the root dictionary
            if processed_formats:
                processed_captions["root"][lang_code] = processed_formats
        
        return processed_captions

    def _extract_captions(self, result: Dict[str, Any]) -> Dict[str, List[YTDLPCaption]]:
        """
        Extracts caption information from the video result.

        Args:
            result (Dict[str, Any]): The raw result dictionary from yt-dlp.

        Returns:
            Dict[str, List[YTDLPCaption]]: A dictionary mapping language codes to lists of caption formats.
            Automatic captions are prefixed with 'auto-' in the language code.
        """
        log.debug("_extract_captions")
        captions: Dict[str, List[YTDLPCaption]] = {}

        # Define caption format preferences with language names
        caption_preferences = [
            ("en-orig", CAPTION_FORMATS, "English (Original)"),
            ("en", CAPTION_FORMATS, "English"),
        ]
        
        # Process automatic captions
        automatic_captions = result.get("automatic_captions", {})
        for lang_code, caption_set in automatic_captions.items():
            # Create a key with 'auto-' prefix to distinguish automatic captions
            auto_lang_code = f"auto-{lang_code}"
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

                # Check if this is a preferred language and format
                is_preferred = False
                for pref_lang, pref_formats, lang_name in caption_preferences:
                    if lang_code == pref_lang and (ext in pref_formats or caption_protocol in [f.value for f in pref_formats]):
                        is_preferred = True
                        break
                
                # Include the caption if it's in a supported format
                if ext:
                    caption_info = YTDLPCaption(
                        ext=ext,
                        url=caption.get("url"),
                        name=caption.get("name", f"Auto {lang_code}")
                    )
                    current_captions.append(caption_info)
            
            if current_captions:
                captions[auto_lang_code] = current_captions
        
        # Process regular captions
        regular_captions = result.get("subtitles", {})
        for lang_code, caption_set in regular_captions.items():
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

                # Check if this is a preferred language and format
                is_preferred = False
                for pref_lang, pref_formats, lang_name in caption_preferences:
                    if lang_code == pref_lang and (ext in pref_formats or caption_protocol in [f.value for f in pref_formats]):
                        is_preferred = True
                        break
                
                # Include the caption if it's in a supported format
                if ext:
                    caption_info = YTDLPCaption(
                        ext=ext,
                        url=caption.get("url"),
                        name=caption.get("name", lang_code)
                    )
                    current_captions.append(caption_info)
            
            if current_captions:
                # If we already have automatic captions for this language, keep them separate
                if lang_code in captions:
                    captions[lang_code].extend(current_captions)
                else:
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
        log.debug("extract_video_id")
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

    def list_available_captions(self, url: str, return_all_captions: bool = False) -> Dict[str, List[YTDLPCaption]]:
        """
        List available captions for a YouTube video.
        
        By default, this method returns only the preferred captions based on the preferences
        defined in _extract_captions (prioritizing English captions with preferred formats).
        
        Args:
            url (str): The URL of the YouTube video.
            return_all_captions (bool): If True, returns all available captions instead of just preferred ones.
                                       Default is False (only preferred captions).

        Returns:
            Dict[str, List[YTDLPCaption]]: A dictionary mapping language codes to lists of available caption objects.
            Example:
            ```
            {
                'en': [
                    YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='English'),
                    YTDLPCaption(ext=CaptionExtension.JSON3, url='https://www.youtube.com/api/timedtext?...', name='English')
                ],
                'es': [
                    YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='Spanish')
                ]
            }
            ```
        """
        log.debug("list_available_captions")
        
        # Check if the URL is valid
        if not self.is_valid_url(url):
            log.warning(f"Invalid YouTube URL: {url}")
            return {}
        
        try:
            # Get video info with options that include all caption formats
            options = self.options.copy()
            options.update({
                'writesubtitles': True,
                'allsubtitles': True,
                'skip_download': True,
            })
            
            with yt_dlp.YoutubeDL(options) as ydl:
                try:
                    # Extract info without downloading
                    result = ydl.extract_info(url, download=False)
                    if not result:
                        log.warning(f"No video information returned for {url}")
                        return {}
                    
                    # Get all captions using _extract_captions
                    all_captions = self._extract_captions(result)
                    
                    # If we only want preferred captions, filter the results
                    if not return_all_captions:
                        # Define preferred languages
                        preferred_languages = ["en-orig", "en", "auto-en", "auto-en-orig"]
                        
                        # Filter to only include preferred languages
                        preferred_captions = {
                            lang: captions for lang, captions in all_captions.items()
                            if lang in preferred_languages
                        }
                        
                        # Log the result for debugging
                        if preferred_captions:
                            log.debug(f"Found preferred captions for video {url}: {preferred_captions}")
                        else:
                            log.debug(f"No preferred captions found for video {url}")
                        
                        return preferred_captions
                    
                    # Return all captions
                    if all_captions:
                        log.debug(f"Found all captions for video {url}: {all_captions}")
                    else:
                        log.debug(f"No captions found for video {url}")
                    
                    return all_captions
                    
                except yt_dlp.utils.DownloadError as e:
                    error_message = str(e)
                    log.warning(f"Download error for video {url}: {error_message}")
                    return {}
                except ExtractorError as e:
                    error_message = str(e)
                    log.warning(f"Extractor error for video {url}: {error_message}")
                    return {}
                
        except Exception as e:
            log.warning(f"Error listing captions for video {url}: {str(e)}")
            return {}
