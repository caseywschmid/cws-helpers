#!/usr/bin/env python3
"""
YouTube Caption Demo - Demonstrates the improved caption handling in YoutubeHelper.

This script shows how to:
1. Extract video information including automatic captions and subtitles
2. Process captions in different languages
3. Handle automatic captions vs. manual subtitles
4. Use custom download options for better caption retrieval

Usage:
    python youtube_caption_demo.py

Requirements:
    - cws-helpers package installed
    - .env file with necessary API keys (if applicable)
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any

# Add the src directory to the path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cws_helpers import YoutubeHelper, configure_logging
from cws_helpers.logger import FINE_LEVEL
from cws_helpers.youtube_helper.enums.youtube_helper_enums import CaptionExtension

# Configure logging
configure_logging(logger_name="youtube_caption_demo", log_level=FINE_LEVEL)

# Sample YouTube URLs known to have captions
SAMPLE_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
    "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
    "https://www.youtube.com/watch?v=EngW7tLk6R8",  # TED Talk (usually has multiple languages)
    "https://www.youtube.com/watch?v=8S0FDjFBj8o",  # Google I/O (usually has good captions)
]

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def demo_basic_caption_extraction():
    """Demonstrate basic caption extraction from a YouTube video."""
    print_separator("Basic Caption Extraction")
    
    helper = YoutubeHelper()
    
    for url in SAMPLE_URLS:
        print(f"Processing URL: {url}")
        
        try:
            # Get video info with default settings
            video_info = helper.get_video_info(url)
            
            print(f"Title: {video_info.title}")
            print(f"Duration: {video_info.duration} seconds")
            
            # Process both automatic captions and subtitles
            has_captions = False
            
            # Check for automatic captions
            if video_info.automatic_captions and hasattr(video_info.automatic_captions, 'root'):
                auto_captions = video_info.automatic_captions.root
                if auto_captions:
                    has_captions = True
                    print(f"Found automatic captions in {len(auto_captions)} languages:")
                    for lang_code, captions in auto_captions.items():
                        print(f"  Auto-{lang_code}: {len(captions)} format(s)")
                        for i, caption in enumerate(captions, 1):
                            print(f"    {i}. Format: {caption.ext}")
                            print(f"       Name: {caption.name}")
            
            # Check for subtitles
            if video_info.subtitles and hasattr(video_info.subtitles, 'root'):
                subtitles = video_info.subtitles.root
                if subtitles:
                    has_captions = True
                    print(f"Found subtitles in {len(subtitles)} languages:")
                    for lang_code, captions in subtitles.items():
                        print(f"  {lang_code}: {len(captions)} format(s)")
                        for i, caption in enumerate(captions, 1):
                            print(f"    {i}. Format: {caption.ext}")
                            print(f"       Name: {caption.name}")
            
            if not has_captions:
                print("No captions or subtitles found for this video.")
            
            print("\n" + "-" * 40 + "\n")
        
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

def demo_custom_download_options():
    """Demonstrate using custom download options for better caption retrieval."""
    print_separator("Custom Download Options")
    
    helper = YoutubeHelper()
    
    # Custom options to improve caption retrieval
    custom_options = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "es", "fr", "de"],  # English, Spanish, French, German
        "skip_download": True,  # Don't download the actual video
    }
    
    url = SAMPLE_URLS[2]  # Use the TED Talk which likely has multiple languages
    print(f"Processing URL with custom options: {url}")
    
    try:
        # Get video info with custom options
        video_info = helper.get_video_info(url, download_options=custom_options)
        
        print(f"Title: {video_info.title}")
        
        # Combine and process both automatic captions and subtitles
        captions_by_language = {}
        
        # Process automatic captions
        if video_info.automatic_captions and hasattr(video_info.automatic_captions, 'root'):
            for lang_code, captions in video_info.automatic_captions.root.items():
                auto_lang_code = f"auto-{lang_code}"
                if auto_lang_code not in captions_by_language:
                    captions_by_language[auto_lang_code] = []
                captions_by_language[auto_lang_code].extend(captions)
        
        # Process subtitles
        if video_info.subtitles and hasattr(video_info.subtitles, 'root'):
            for lang_code, captions in video_info.subtitles.root.items():
                if lang_code not in captions_by_language:
                    captions_by_language[lang_code] = []
                captions_by_language[lang_code].extend(captions)
        
        if captions_by_language:
            print(f"Found captions in {len(captions_by_language)} languages:")
            
            # Print summary by language
            for lang, captions in captions_by_language.items():
                print(f"  Language: {lang}")
                print(f"    Number of tracks: {len(captions)}")
                print(f"    Formats: {', '.join(str(c.ext) for c in captions if c.ext)}")
                print(f"    Auto-generated: {lang.startswith('auto-')}")
        else:
            print("No captions found for this video.")
    
    except Exception as e:
        print(f"Error processing with custom options: {str(e)}")

def demo_caption_processing():
    """Demonstrate processing captions for different use cases."""
    print_separator("Caption Processing")
    
    helper = YoutubeHelper()
    
    url = SAMPLE_URLS[0]  # Rick Astley video
    print(f"Processing captions for: {url}")
    
    try:
        # Get video info
        video_info = helper.get_video_info(url)
        
        # Look for English captions (first in subtitles, then in automatic captions)
        english_captions = []
        
        # Check subtitles first (manual captions are usually better quality)
        if video_info.subtitles and hasattr(video_info.subtitles, 'root'):
            if 'en' in video_info.subtitles.root:
                english_captions = video_info.subtitles.root['en']
                print("Found English subtitles (manual captions)")
        
        # If no English subtitles, check automatic captions
        if not english_captions and video_info.automatic_captions and hasattr(video_info.automatic_captions, 'root'):
            if 'en' in video_info.automatic_captions.root:
                english_captions = video_info.automatic_captions.root['en']
                print("Found English automatic captions")
        
        if not english_captions:
            print("No English captions found.")
            return
        
        # Get the first English caption
        caption = english_captions[0]
        
        # Print caption format and URL
        print(f"Caption format: {caption.ext}")
        print(f"Caption URL: {caption.url}")
        
        # Note: The actual text content would require downloading and parsing the caption file
        print("\nNote: To get the actual caption text, you would need to download and parse the caption file.")
        print("This is not implemented in the current version of the YoutubeHelper.")
    
    except Exception as e:
        print(f"Error processing captions: {str(e)}")

def demo_raw_info_inspection():
    """Demonstrate inspecting raw video information for debugging."""
    print_separator("Raw Info Inspection")
    
    helper = YoutubeHelper()
    
    url = SAMPLE_URLS[1]  # First YouTube video
    print(f"Inspecting raw info for: {url}")
    
    try:
        # Get video info with raw_info=True
        video_info = helper.get_video_info(url, raw_info=True)
        
        # Print basic info
        print(f"Title: {video_info.title}")
        print(f"Duration: {video_info.duration} seconds")
        
        # Print raw info about captions
        if hasattr(video_info, "raw_info") and video_info.raw_info:
            if "requested_subtitles" in video_info.raw_info:
                print("\nRequested subtitles:")
                print(json.dumps(video_info.raw_info["requested_subtitles"], indent=2))
            
            if "subtitles" in video_info.raw_info:
                print("\nAvailable subtitles:")
                print(json.dumps(video_info.raw_info["subtitles"], indent=2))
            
            if "automatic_captions" in video_info.raw_info:
                print("\nAutomatic captions:")
                print(json.dumps(video_info.raw_info["automatic_captions"], indent=2))
        else:
            print("No raw info available.")
    
    except Exception as e:
        print(f"Error inspecting raw info: {str(e)}")

def main():
    """Run the YouTube caption demo."""
    print_separator("YouTube Caption Demo")
    print("This script demonstrates the improved caption handling in YoutubeHelper.")
    
    # Run the demos
    demo_basic_caption_extraction()
    demo_custom_download_options()
    demo_caption_processing()
    demo_raw_info_inspection()
    
    print_separator("Demo Complete")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the demo
    main() 