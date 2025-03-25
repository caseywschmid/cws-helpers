"""CWS Helpers - Collection of utility helpers for personal projects."""

__version__ = "0.10.0"

# For convenient imports
from .logger import configure_logging
from .openai_helper import OpenAIHelper, AIModel, AIProvider
from .aws_helper import S3Helper
from .youtube_helper import YoutubeHelper, CaptionExtension
from .google_helper import GoogleHelper
from .powerpath_helper import PowerPathClient
from .anthropic_helper import AnthropicHelper