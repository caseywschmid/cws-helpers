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
#     'en': [CaptionExtension.VTT, CaptionExtension.JSON3]
# }

# Get all available captions
all_captions = youtube.list_available_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ", return_all_captions=True)

# Example output (all captions):
# {
#     'auto-en': [CaptionExtension.VTT, CaptionExtension.JSON3, CaptionExtension.SRV1],
#     'en': [CaptionExtension.VTT, CaptionExtension.JSON3, CaptionExtension.SRV1],
#     'es': [CaptionExtension.VTT],
#     'fr': [CaptionExtension.VTT]
# }

# Note: Automatic captions are prefixed with 'auto-'

# Check if a specific language and format is available
has_english_vtt = CaptionExtension.VTT in preferred_captions.get('en', [])
has_auto_english = 'auto-en' in preferred_captions

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

# Use custom download options to improve caption retrieval
video_info = youtube.get_video_info(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    download_options={
        "writesubtitles": True,        # Enable subtitle downloading
        "writeautomaticsub": True,     # Enable automatic subtitle downloading
        "subtitleslangs": ["en", "es", "fr", "de"],  # Specify languages
        "skip_download": True,         # Skip video download (captions only)
    }
)
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

# Or provide options for a specific download
video_info = youtube.get_video_info(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    download_options={
        'format': 'bestvideo+bestaudio',
        'writesubtitles': True,
        'subtitleslangs': ['en', 'es']
    }
)
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

#### `list_available_captions(url: str, return_all_captions: bool = False) -> Dict[str, List[CaptionExtension]]`

List available captions for a YouTube video.

- **Parameters:**
  - `url` (str): The YouTube URL.
  - `return_all_captions` (bool): Whether to return all available captions. Default is False, which returns only preferred captions based on predefined preferences (prioritizing English captions with preferred formats).
- **Returns:**
  - `Dict[str, List[CaptionExtension]]`: A dictionary mapping language codes to lists of available caption formats.
- **Note:**
  - Automatic captions are prefixed with 'auto-' to distinguish them from manual captions.
  - When `return_all_captions=False` (default), only preferred captions are returned.
  - When `return_all_captions=True`, all available captions are returned.

### Models

#### `YTDLPVideoDetails`

A Pydantic model representing detailed information about a YouTube video.

- **Fields:**
  - `id` (str): The video ID.
  - `title` (str): The video title.
  - `description` (Optional[str]): The video description.
  - `duration` (Optional[int]): The video duration in seconds.
  - `view_count` (Optional[int]): The number of views.
  - `like_count` (Optional[int]): The number of likes.
  - `dislike_count` (Optional[int]): The number of dislikes.
  - `average_rating` (Optional[float]): The average rating.
  - `age_limit` (Optional[int]): The age limit.
  - `webpage_url` (Optional[str]): The webpage URL.
  - `categories` (Optional[List[str]]): The video categories.
  - `tags` (Optional[List[str]]): The video tags.
  - `formats` (List[YTDLPVideoFormat]): The available video formats.
  - `thumbnails` (List[YTDLPThumbnail]): The available thumbnails.
  - `automatic_captions` (YTDLPAutomaticCaption): The automatic captions.
  - `subtitles` (YTDLPSubtitle): The manual subtitles.

#### `YTDLPAutomaticCaption` and `YTDLPSubtitle`

Pydantic models representing automatic captions and manual subtitles.

- **Structure:**
  - Both models have a `root` field which is a dictionary mapping language codes to lists of caption formats.
  - Each caption format is represented by a `YTDLPCaption` model.

#### `YTDLPCaption`

A Pydantic model representing a caption format.

- **Fields:**
  - `ext` (Optional[CaptionExtension]): The caption extension.
  - `url` (Optional[str]): The caption URL.
  - `name` (Optional[str]): The caption name.

#### `CaptionExtension`

An enum representing supported caption extensions.

- **Values:**
  - `VTT`: WebVTT format
  - `SRT`: SubRip format
  - `JSON3`: JSON3 format
  - `TTML`: TTML format
  - `SRV1`: SRV1 format
  - `SRV2`: SRV2 format
  - `SRV3`: SRV3 format
  - `M3U8`: HLS manifest format

### Exceptions

#### `YouTubeVideoUnavailable`

Raised when a YouTube video is not available.

#### `YTOAuthTokenExpired`

Raised when the OAuth token has expired.

## Examples

See the `examples` directory for more detailed examples:

- `youtube_caption_demo.py`: Demonstrates the improved caption handling in YoutubeHelper.
- `youtube_video_info.py`: Shows how to extract and use video information.

## Testing

The helper includes comprehensive tests for all functionality, including:

- URL validation tests
- Video information extraction tests
- Caption handling tests
- Error handling tests

Run the tests with pytest:

```bash
pytest tests/youtube_helper/
```