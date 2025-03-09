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

# Get available captions
captions = youtube.list_available_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Example output:
# {
#     'en': [CaptionExtension.VTT, CaptionExtension.SRV1],
#     'es': [CaptionExtension.VTT]
# }

# Check if a specific language and format is available
has_english_vtt = CaptionExtension.VTT in captions.get('en', [])
```

## API Reference

### `YoutubeHelper`

#### `__init__(options: Optional[Dict[str, Any]] = None)`

Initialize the YouTube helper with optional configuration options.

- **Parameters:**
  - `options`: Optional dictionary of options to pass to the yt-dlp extractor.

#### `is_valid_url(url: str) -> bool`

Check if a URL is a valid YouTube URL.

- **Parameters:**
  - `url`: The URL to check.
- **Returns:**
  - `bool`: True if the URL is a valid YouTube URL, False otherwise.

#### `get_video_info(url: str) -> YTDLPVideoDetails`

Get detailed information about a YouTube video.

- **Parameters:**
  - `url`: The URL of the YouTube video.
- **Returns:**
  - `YTDLPVideoDetails`: A Pydantic model containing detailed information about the video.
- **Raises:**
  - `YouTubeVideoUnavailable`: If the video is not available.
  - `YTOAuthTokenExpired`: If the YouTube OAuth token has expired.

#### `extract_video_id(url: str) -> Optional[str]`

Extract the video ID from a YouTube URL.

- **Parameters:**
  - `url`: The YouTube URL.
- **Returns:**
  - `Optional[str]`: The video ID if found, None otherwise.

#### `list_available_captions(url: str) -> Dict[str, List[CaptionExtension]]`

List available captions for a YouTube video.

- **Parameters:**
  - `url`: The URL of the YouTube video.
- **Returns:**
  - `Dict[str, List[CaptionExtension]]`: A dictionary mapping language codes to lists of available caption formats.

### Exceptions

#### `YouTubeVideoUnavailable`

Raised when a YouTube video is not available.

#### `YTOAuthTokenExpired`

Raised when the YouTube OAuth token has expired.

### Enums

#### `CaptionExtension`

Enumeration of supported YouTube caption extensions.

- `JSON3`: JSON format version 3
- `SRV1`: SubRip format version 1
- `SRV2`: SubRip format version 2
- `SRV3`: SubRip format version 3
- `TTML`: Timed Text Markup Language
- `VTT`: WebVTT (Web Video Text Tracks)
- `M3U8`: HLS manifest format 