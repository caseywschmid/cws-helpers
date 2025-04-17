# YouTube Helper

A utility module for interacting with YouTube videos, extracting video information, validating URLs, and working with captions.

## Installation

This helper is included in the cws-helpers package:

```bash
pip install git+https://github.com/caseywschmid/cws-helpers.git
```

## Dependencies

This helper requires the following dependencies:
- yt-dlp: For extracting video information
- pydantic: For data validation and model definitions

## Usage

### Basic Usage

```python
from cws_helpers import YoutubeHelper

# Initialize the helper
youtube = YoutubeHelper()

# Check if a URL is a valid YouTube URL
is_valid = youtube.is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Extract video ID from a URL
video_id = youtube.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Get detailed information about a video
video_info = youtube.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# List available captions for a video
captions = youtube.list_available_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Working with Captions

```python
from cws_helpers import YoutubeHelper, CaptionExtension

youtube = YoutubeHelper()

# Get preferred captions (default behavior)
preferred_captions = youtube.list_available_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Example output (only preferred captions):
# {
#     'en': [
#         YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='English'),
#         YTDLPCaption(ext=CaptionExtension.JSON3, url='https://www.youtube.com/api/timedtext?...', name='English')
#     ]
# }

# Get all available captions
all_captions = youtube.list_available_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ", return_all_captions=True)

# Example output (all captions):
# {
#     'auto-en': [
#         YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='English'),
#         YTDLPCaption(ext=CaptionExtension.JSON3, url='https://www.youtube.com/api/timedtext?...', name='English')
#     ],
#     'en': [
#         YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='English'),
#         YTDLPCaption(ext=CaptionExtension.JSON3, url='https://www.youtube.com/api/timedtext?...', name='English')
#     ],
#     'es': [
#         YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='Spanish')
#     ],
#     'fr': [
#         YTDLPCaption(ext=CaptionExtension.VTT, url='https://www.youtube.com/api/timedtext?...', name='French')
#     ]
# }

# Note: Automatic captions are prefixed with 'auto-'

# Check if a specific language and format is available
has_english_vtt = any(caption.ext == CaptionExtension.VTT for caption in preferred_captions.get('en', []))
has_auto_english = 'auto-en' in preferred_captions

# Access caption URLs directly
if 'en' in preferred_captions:
    for caption in preferred_captions['en']:
        if caption.ext == CaptionExtension.VTT:
            vtt_url = caption.url
            print(f"English VTT caption URL: {vtt_url}")
            # You can now download the caption using this URL

# Access caption data from video_info
video_info = youtube.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Access automatic captions
if video_info.automatic_captions and hasattr(video_info.automatic_captions, 'root'):
    auto_captions = video_info.automatic_captions.root
    for lang_code, captions in auto_captions.items():
        print(f"Automatic captions in {lang_code}:")
        for caption in captions:
            print(f"  Format: {caption.ext}")
            print(f"  URL: {caption.url}")

# Access manual subtitles
if video_info.subtitles and hasattr(video_info.subtitles, 'root'):
    subtitles = video_info.subtitles.root
    for lang_code, captions in subtitles.items():
        print(f"Subtitles in {lang_code}:")
        for caption in captions:
            print(f"  Format: {caption.ext}")
            print(f"  URL: {caption.url}")
```

### Enhanced Caption Retrieval

The helper now provides improved caption handling with better support for automatic captions and multiple languages:

```python
from cws_helpers import YoutubeHelper

youtube = YoutubeHelper()

# Note: As of v0.10.3, get_video_info always uses default yt-dlp options and ignores custom download_options.
video_info = youtube.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# If you need custom caption handling, use list_available_captions or process captions from video_info manually.
```

### Custom Download Options

```python
from cws_helpers import YoutubeHelper

# Initialize with custom options
youtube = YoutubeHelper({
    'format': 'bestvideo+bestaudio',
    'writesubtitles': True,
    'subtitleslangs': ['en', 'es']
})

# The download_options argument is now ignored in get_video_info.
```

## API Reference

### `YoutubeHelper`

#### `__init__(options: Optional[Dict[str, Any]] = None)`

Initialize the YouTube helper with optional configuration options.

- **Parameters:**
  - `options` (Optional[Dict[str, Any]]): Optional configuration options for yt-dlp.

#### `is_valid_url(url: str) -> bool`

Check if a URL is a valid YouTube URL.

- **Parameters:**
  - `url` (str): The URL to check.
- **Returns:**
  - `bool`: True if the URL is a valid YouTube URL, False otherwise.

#### `extract_video_id(url: str) -> Optional[str]`

Extract the video ID from a YouTube URL.

- **Parameters:**
  - `url` (str): The YouTube URL.
- **Returns:**
  - `Optional[str]`: The extracted video ID, or None if the URL is not a valid YouTube URL.
- **Note:**
  - This method does not raise a ValueError as indicated in the previous documentation.

#### `get_video_info(url: str, download_options: Optional[Dict[str, Any]] = None) -> YTDLPVideoDetails`

Get detailed information about a YouTube video.

- **Parameters:**
  - `url` (str): The YouTube URL.
  - `download_options` (Optional[Dict[str, Any]]): Optional download options for yt-dlp.
- **Returns:**
  - `YTDLPVideoDetails`: A Pydantic model containing the video details.
- **Raises:**
  - `YouTubeVideoUnavailable`: If the video is not available.
  - `YTOAuthTokenExpired`: If the OAuth token has expired.

#### `list_available_captions(url: str, return_all_captions: bool = False) -> Dict[str, List[YTDLPCaption]]`

List available captions for a YouTube video.

- **Parameters:**
  - `url` (str): The YouTube URL.
  - `return_all_captions` (bool): Whether to return all available captions. Default is False, which returns only preferred captions based on predefined preferences (prioritizing English captions with preferred formats).
- **Returns:**
  - `Dict[str, List[YTDLPCaption]]`: A dictionary mapping language codes to lists of available caption objects.
  Example:
  ```python
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
- **Note:**
  - Automatic captions are prefixed with 'auto-' to distinguish them from manual captions.
  - When `return_all_captions=False` (default), only preferred captions are returned.
  - When `return_all_captions=True`, all available captions are returned.
  - Each caption object contains the extension, URL, and name, allowing you to download the captions directly.

### Models

#### `YTDLPVideoDetails`