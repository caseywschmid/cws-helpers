#!/usr/bin/env python
"""
Test script for the YouTube helper.
This script tests the YouTube helper with specific URLs to verify caption retrieval functionality.
It limits caption output to avoid overwhelming the chat.
"""

from src.cws_helpers.youtube_helper.youtube_helper import YoutubeHelper, yt_dlp
from src.cws_helpers.youtube_helper.enums.youtube_helper_enums import CaptionExtension
import json
import pprint

def test_youtube_helper():
    """Test the YouTube helper with specific URLs."""
    # Create a YouTube helper instance
    helper = YoutubeHelper()
    
    # Test URLs - including videos known to have captions
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
        "https://www.youtube.com/watch?v=aqz-KE-bpKQ",  # Big Buck Bunny (known to have captions)
    ]
    
    for url in urls:
        print(f"\n\n{'='*50}")
        print(f"=== Testing URL: {url} ===")
        print(f"{'='*50}\n")
        
        # Test if the URL is valid
        print(f"URL valid: {helper.is_valid_url(url)}")
        
        # Get raw video info directly from yt-dlp with write_auto_subs and writesubtitles enabled
        print("\nGetting raw video info from yt-dlp with captions enabled...")
        
        # Create a copy of options with subtitles enabled
        options_with_subs = helper.options.copy()
        options_with_subs.update({
            'writesubtitles': True,
            'write_auto_subs': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
        })
        
        with yt_dlp.YoutubeDL(options_with_subs) as ydl:
            try:
                raw_info = ydl.extract_info(url, download=False)
                
                # Check for captions in raw info
                print("\nChecking for captions in raw info:")
                
                # Debug the entire raw_info structure
                print("\nRaw info keys available:")
                print(list(raw_info.keys()))
                
                # Function to limit and format caption output
                def print_limited_captions(caption_dict, caption_type="captions"):
                    """
                    Print a limited sample of captions to avoid overwhelming output.
                    
                    Args:
                        caption_dict: Dictionary containing caption data
                        caption_type: String describing the type of captions
                    """
                    if not caption_dict:
                        print(f"No {caption_type} available")
                        return
                        
                    print(f"\nRaw {caption_type}:")
                    print(f"Type: {type(caption_dict)}")
                    
                    if isinstance(caption_dict, dict):
                        langs = list(caption_dict.keys())
                        print(f"Available languages: {langs}")
                        
                        # Show details for at most 2 languages
                        sample_langs = langs[:2]
                        for lang in sample_langs:
                            print(f"\nSample for language '{lang}':")
                            formats = caption_dict[lang]
                            
                            # Show at most 3 caption formats per language
                            if isinstance(formats, list) and formats:
                                sample_formats = formats[:3]
                                print(f"Showing {len(sample_formats)} of {len(formats)} formats:")
                                for i, fmt in enumerate(sample_formats):
                                    print(f"  Format {i+1}:")
                                    # For each format, show only key information
                                    if isinstance(fmt, dict):
                                        keys_to_show = ['ext', 'url', 'name'] 
                                        for key in keys_to_show:
                                            if key in fmt:
                                                print(f"    {key}: {fmt[key]}")
                                    else:
                                        print(f"    {fmt}")
                            else:
                                print(f"  Formats: {formats}")
                    else:
                        print(f"  Content: {str(caption_dict)[:200]}...")
                
                # Print limited caption information
                if 'automatic_captions' in raw_info:
                    print_limited_captions(raw_info['automatic_captions'], "automatic_captions")
                else:
                    print("No automatic_captions field in raw info")
                    
                if 'subtitles' in raw_info:
                    print_limited_captions(raw_info['subtitles'], "subtitles")
                else:
                    print("No subtitles field in raw info")
            except Exception as e:
                print(f"Error extracting raw info: {str(e)}")
        
        # Test getting video information
        print("\nTesting get_video_info...")
        try:
            video_info = helper.get_video_info(url)
            print(f"Success! Video title: {video_info.title}")
            
            # Examine the captions in the processed video info (limited output)
            print("\nExamining captions in processed video info:")
            
            # Helper function to print limited processed caption info
            def print_limited_processed_captions(caption_obj, caption_type="captions"):
                """Print limited information about processed captions."""
                if not caption_obj:
                    print(f"No {caption_type} in processed info")
                    return
                    
                print(f"Processed {caption_type}:")
                if hasattr(caption_obj, 'root') and caption_obj.root:
                    root = caption_obj.root
                    print(f"Root type: {type(root)}")
                    
                    if isinstance(root, dict):
                        langs = list(root.keys())
                        print(f"Available languages: {langs}")
                        
                        # Show at most 2 languages
                        sample_langs = langs[:2]
                        for lang in sample_langs:
                            print(f"\nSample for language '{lang}':")
                            # Show limited information about this language's captions
                            if isinstance(root[lang], list):
                                formats = root[lang][:2]  # Show at most 2 formats
                                print(f"Showing {len(formats)} format(s)")
                                for i, fmt in enumerate(formats):
                                    print(f"  Format {i+1}: {str(fmt)[:100]}...")
                            else:
                                print(f"  Content: {str(root[lang])[:100]}...")
                    else:
                        print(f"  Root content: {str(root)[:200]}...")
                else:
                    print(f"No 'root' attribute in {caption_type}")
            
            # Print limited processed caption information
            if hasattr(video_info, 'automatic_captions') and video_info.automatic_captions:
                print_limited_processed_captions(video_info.automatic_captions, "automatic_captions")
            else:
                print("No automatic_captions in processed info")
                
            if hasattr(video_info, 'subtitles') and video_info.subtitles:
                print_limited_processed_captions(video_info.subtitles, "subtitles")
            else:
                print("No subtitles in processed info")
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
        
        # Test listing available captions
        print("\nTesting list_available_captions...")
        try:
            captions = helper.list_available_captions(url)
            if captions:
                print("Available captions:")
                # Limit to showing only 3 languages
                lang_count = 0
                for lang, formats in captions.items():
                    format_names = [f.name if hasattr(f, 'name') else str(f) for f in formats]
                    print(f"  {lang}: {', '.join(format_names[:3])}{'...' if len(format_names) > 3 else ''}")
                    lang_count += 1
                    if lang_count >= 3:
                        remaining = len(captions) - 3
                        if remaining > 0:
                            print(f"  ... and {remaining} more language(s)")
                        break
            else:
                print("No captions available for this video.")
        except Exception as e:
            print(f"Error listing captions: {str(e)}")

if __name__ == "__main__":
    test_youtube_helper() 