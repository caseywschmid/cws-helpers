"""
Tests for the YouTube Helper caption functionality.

This module contains tests specifically focused on the caption handling functionality
of the YoutubeHelper class, including:
1. Caption processing tests - Testing _process_captions_for_model functionality
2. Automatic caption prefix tests - Testing 'auto-' prefix handling
3. Caption format handling tests - Testing different caption formats
4. Custom download options for captions - Testing caption-specific download options
"""

import pytest
from unittest.mock import patch, MagicMock
import yt_dlp

from cws_helpers.youtube_helper import YoutubeHelper, YouTubeVideoUnavailable
from cws_helpers.youtube_helper.models.youtube_helper_models import (
    YTDLPVideoDetails, 
    YTDLPCaption, 
    YTDLPAutomaticCaption, 
    YTDLPSubtitle
)
from cws_helpers.youtube_helper.enums.youtube_helper_enums import CaptionExtension

# Test constants
SAMPLE_VIDEO_ID = "dQw4w9WgXcQ"
SAMPLE_VIDEO_URL = f"https://www.youtube.com/watch?v={SAMPLE_VIDEO_ID}"

@pytest.fixture
def youtube_helper():
    """Fixture to create a YoutubeHelper instance."""
    return YoutubeHelper()

@pytest.fixture
def mock_caption_data():
    """Fixture providing mock caption data for testing."""
    return {
        # Automatic captions in multiple languages
        'automatic_captions': {
            'en': [
                {
                    'ext': 'json3',
                    'url': 'https://example.com/auto_captions_en.json3',
                    'name': 'English'
                },
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/auto_captions_en.vtt',
                    'name': 'English'
                },
                {
                    'ext': 'srv1',
                    'url': 'https://example.com/auto_captions_en.srv1',
                    'name': 'English'
                }
            ],
            'es': [
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/auto_captions_es.vtt',
                    'name': 'Spanish'
                }
            ],
            'fr': [
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/auto_captions_fr.vtt',
                    'name': 'French'
                }
            ]
        },
        # Manual subtitles in multiple languages
        'subtitles': {
            'en': [
                {
                    'ext': 'json3',
                    'url': 'https://example.com/subtitles_en.json3',
                    'name': 'English'
                },
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/subtitles_en.vtt',
                    'name': 'English'
                }
            ],
            'de': [
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/subtitles_de.vtt',
                    'name': 'German'
                }
            ]
        }
    }

# ---------------------------- Caption Processing Tests ---------------------------- #

def test_process_captions_for_model(youtube_helper, mock_caption_data):
    """Test the _process_captions_for_model method with various caption formats."""
    # Process automatic captions
    auto_captions_result = youtube_helper._process_captions_for_model(mock_caption_data['automatic_captions'])
    
    # Verify the structure is correct
    assert 'root' in auto_captions_result
    assert isinstance(auto_captions_result['root'], dict)
    
    # Verify languages are preserved
    assert 'en' in auto_captions_result['root']
    assert 'es' in auto_captions_result['root']
    assert 'fr' in auto_captions_result['root']
    
    # Verify caption formats are processed correctly
    en_captions = auto_captions_result['root']['en']
    assert len(en_captions) == 3
    
    # Check that the first caption has the correct structure
    first_caption = en_captions[0]
    assert 'ext' in first_caption
    assert 'url' in first_caption
    assert 'name' in first_caption
    
    # Verify extension is converted to enum when possible
    assert first_caption['ext'] in [CaptionExtension.JSON3, CaptionExtension.VTT, CaptionExtension.SRV1]
    
    # Process subtitles
    subtitles_result = youtube_helper._process_captions_for_model(mock_caption_data['subtitles'])
    
    # Verify the structure is correct
    assert 'root' in subtitles_result
    assert isinstance(subtitles_result['root'], dict)
    
    # Verify languages are preserved
    assert 'en' in subtitles_result['root']
    assert 'de' in subtitles_result['root']

def test_process_captions_for_model_empty(youtube_helper):
    """Test the _process_captions_for_model method with empty input."""
    # Process empty captions
    result = youtube_helper._process_captions_for_model({})
    
    # Verify the structure is correct
    assert 'root' in result
    assert isinstance(result['root'], dict)
    assert len(result['root']) == 0

def test_process_captions_for_model_invalid_extension(youtube_helper):
    """Test the _process_captions_for_model method with invalid caption extensions."""
    # Create caption data with invalid extension
    invalid_caption_data = {
        'en': [
            {
                'ext': 'invalid_ext',
                'url': 'https://example.com/captions.invalid',
                'name': 'English'
            }
        ]
    }
    
    # Process captions with invalid extension
    result = youtube_helper._process_captions_for_model(invalid_caption_data)
    
    # Verify the structure is correct
    assert 'root' in result
    assert 'en' in result['root']
    
    # Verify the extension is preserved as a string
    first_caption = result['root']['en'][0]
    assert first_caption['ext'] == 'invalid_ext'

def test_process_captions_for_model_missing_fields(youtube_helper):
    """Test the _process_captions_for_model method with missing fields."""
    # Create caption data with missing fields
    incomplete_caption_data = {
        'en': [
            {
                # Missing 'ext'
                'url': 'https://example.com/captions.vtt'
                # Missing 'name'
            }
        ]
    }
    
    # Process captions with missing fields
    result = youtube_helper._process_captions_for_model(incomplete_caption_data)
    
    # Verify the structure is correct
    assert 'root' in result
    assert 'en' in result['root']
    
    # Verify default values are used for missing fields
    first_caption = result['root']['en'][0]
    assert 'ext' in first_caption
    assert first_caption['ext'] is None  # Default value for missing ext
    assert 'url' in first_caption
    assert first_caption['url'] == 'https://example.com/captions.vtt'
    assert 'name' in first_caption
    assert first_caption['name'] == 'Caption for en'  # Default name with language code

# ---------------------------- Automatic Caption Prefix Tests ---------------------------- #

def test_list_available_captions_with_auto_prefix(youtube_helper, mock_caption_data):
    """Test that list_available_captions correctly prefixes automatic captions with 'auto-' when return_all_captions=True."""
    # Create a mock video info object
    mock_video_info = MagicMock()
    
    # Set up automatic captions
    auto_captions = MagicMock()
    auto_captions.root = {
        'en': [
            MagicMock(ext=CaptionExtension.VTT, name='English'),
            MagicMock(ext=CaptionExtension.JSON3, name='English')
        ],
        'es': [
            MagicMock(ext=CaptionExtension.VTT, name='Spanish')
        ]
    }
    
    # Set up subtitles
    subtitles = MagicMock()
    subtitles.root = {
        'fr': [
            MagicMock(ext=CaptionExtension.VTT, name='French')
        ],
        'de': [
            MagicMock(ext=CaptionExtension.VTT, name='German')
        ]
    }
    
    # Attach captions to mock video info
    mock_video_info.automatic_captions = auto_captions
    mock_video_info.subtitles = subtitles
    
    # Mock the extract_info method to return our mock data
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=mock_caption_data):
        # Call list_available_captions with return_all_captions=True
        captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL, return_all_captions=True)
        
        # Verify automatic captions are prefixed with 'auto-'
        assert 'auto-en' in captions
        assert 'auto-es' in captions
        
        # Verify regular subtitles are not prefixed
        assert 'fr' in captions or 'de' in captions
        
        # Verify caption formats are preserved
        if 'auto-en' in captions:
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['auto-en'])
            assert any(caption.ext == CaptionExtension.JSON3 for caption in captions['auto-en'])
        if 'auto-es' in captions:
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['auto-es'])
        if 'fr' in captions:
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['fr'])

def test_list_available_captions_preferred_only(youtube_helper, mock_caption_data):
    """Test that list_available_captions returns only preferred captions by default."""
    # Mock the extract_info method to return our mock data
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=mock_caption_data):
        # Mock the _extract_captions method to return a known set of preferred captions
        preferred_captions = {
            'en': [
                YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/en.vtt", name='English')
            ]
        }
        with patch.object(youtube_helper, '_extract_captions', return_value=preferred_captions):
            # Call list_available_captions with default parameters (return_all_captions=False)
            captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL)
            
            # Verify only preferred captions are returned
            assert 'en' in captions
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['en'])
            
            # Verify non-preferred captions are not included
            assert 'auto-en' not in captions
            assert 'auto-es' not in captions
            assert 'fr' not in captions
            assert 'de' not in captions
            
            # Verify the total number of languages matches our preferred set
            assert len(captions) == len(preferred_captions)

def test_list_available_captions_parameter_behavior(youtube_helper, mock_caption_data):
    """Test that the return_all_captions parameter correctly controls the behavior."""
    # Mock the extract_info method to return our mock data
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=mock_caption_data):
        # Create a side effect function that returns different values based on the context
        def extract_captions_side_effect(result):
            # For the first call (preferred captions)
            if not hasattr(extract_captions_side_effect, 'called'):
                extract_captions_side_effect.called = True
                return {
                    'en': [
                        YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/en.vtt", name='English')
                    ]
                }
            # For the second call (all captions)
            else:
                return {
                    'en': [
                        YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/en.vtt", name='English'),
                        YTDLPCaption(ext=CaptionExtension.JSON3, url="https://example.com/en.json3", name='English')
                    ],
                    'auto-en': [
                        YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/auto-en.vtt", name='Auto English')
                    ],
                    'es': [
                        YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/es.vtt", name='Spanish')
                    ]
                }
        
        # Mock _extract_captions with our side effect function
        with patch.object(youtube_helper, '_extract_captions', side_effect=extract_captions_side_effect):
            # Call with return_all_captions=False (default)
            preferred_only = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL)
            
            # Call with return_all_captions=True
            all_captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL, return_all_captions=True)
            
            # Verify preferred_only has fewer languages than all_captions
            assert len(preferred_only) <= len(all_captions)
            
            # Verify preferred captions are in both results
            assert 'en' in preferred_only
            assert 'en' in all_captions
            
            # Verify all_captions has more languages or caption formats
            assert len(all_captions) > len(preferred_only) or sum(len(formats) for formats in all_captions.values()) > sum(len(formats) for formats in preferred_only.values())

def test_list_available_captions_no_auto_captions(youtube_helper):
    """Test list_available_captions when no automatic captions are available."""
    # Create a mock video info object with no automatic captions
    mock_data = {
        'id': SAMPLE_VIDEO_ID,
        'title': 'Test Video',
        'automatic_captions': {},
        'subtitles': {
            'en': [
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/subtitles_en.vtt',
                    'name': 'English'
                }
            ]
        }
    }
    
    # Mock the extract_info method to return our mock data
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=mock_data):
        # Mock the _extract_captions method to return only English subtitles
        preferred_captions = {
            'en': [
                YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/en.vtt", name='English')
            ]
        }
        with patch.object(youtube_helper, '_extract_captions', return_value=preferred_captions):
            # Call list_available_captions with default parameters
            captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL)
            
            # Verify no automatic captions are present
            assert not any(lang.startswith('auto-') for lang in captions.keys())
            
            # Verify regular subtitles are present
            assert 'en' in captions
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['en'])
            
            # Call with return_all_captions=True
            all_captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL, return_all_captions=True)
            
            # Verify no automatic captions are present in all captions
            assert not any(lang.startswith('auto-') for lang in all_captions.keys())
            
            # Verify regular subtitles are present in all captions
            assert 'en' in all_captions
            assert any(caption.ext == CaptionExtension.VTT for caption in all_captions['en'])

def test_list_available_captions_no_subtitles(youtube_helper):
    """Test list_available_captions when no subtitles are available."""
    # Create a mock video info with only automatic captions
    mock_data = {
        'id': SAMPLE_VIDEO_ID,
        'title': 'Test Video',
        'automatic_captions': {
            'en': [
                {
                    'ext': 'vtt',
                    'url': 'https://example.com/auto_captions_en.vtt',
                    'name': 'English'
                }
            ]
        },
        'subtitles': {}
    }
    
    # Mock the extract_info method to return our mock data
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=mock_data):
        # Mock the _extract_captions method to return preferred captions
        # In this case, we'll return auto-en captions as preferred
        preferred_captions = {
            'auto-en': [
                YTDLPCaption(ext=CaptionExtension.VTT, url="https://example.com/auto-en.vtt", name='English')
            ]
        }
        with patch.object(youtube_helper, '_extract_captions', return_value=preferred_captions):
            # Call list_available_captions with default parameters
            captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL)
            
            # Verify automatic captions are present and prefixed
            assert 'auto-en' in captions
            assert any(caption.ext == CaptionExtension.VTT for caption in captions['auto-en'])
            
            # Verify no regular subtitles are present
            assert not any(not lang.startswith('auto-') for lang in captions.keys())
            
            # Call with return_all_captions=True
            all_captions = youtube_helper.list_available_captions(SAMPLE_VIDEO_URL, return_all_captions=True)
            
            # Verify automatic captions are present in all captions
            assert 'auto-en' in all_captions
            assert any(caption.ext == CaptionExtension.VTT for caption in all_captions['auto-en'])

# ---------------------------- Caption Format Handling Tests ---------------------------- #

def test_caption_format_handling(youtube_helper):
    """Test handling of different caption formats."""
    # Create caption data with various formats
    caption_data = {
        'en': [
            {'ext': 'json3', 'url': 'https://example.com/captions.json3', 'name': 'English'},
            {'ext': 'vtt', 'url': 'https://example.com/captions.vtt', 'name': 'English'},
            {'ext': 'srv1', 'url': 'https://example.com/captions.srv1', 'name': 'English'},
            {'ext': 'srv2', 'url': 'https://example.com/captions.srv2', 'name': 'English'},
            {'ext': 'srv3', 'url': 'https://example.com/captions.srv3', 'name': 'English'},
            {'ext': 'ttml', 'url': 'https://example.com/captions.ttml', 'name': 'English'},
            {'ext': 'm3u8_native', 'url': 'https://example.com/captions.m3u8', 'name': 'English'}
        ]
    }
    
    # Process captions
    result = youtube_helper._process_captions_for_model(caption_data)
    
    # Verify all formats are processed correctly
    en_captions = result['root']['en']
    assert len(en_captions) == 7
    
    # Check that each format is converted to the correct enum
    extensions = [caption['ext'] for caption in en_captions]
    assert CaptionExtension.JSON3 in extensions
    assert CaptionExtension.VTT in extensions
    assert CaptionExtension.SRV1 in extensions
    assert CaptionExtension.SRV2 in extensions
    assert CaptionExtension.SRV3 in extensions
    assert CaptionExtension.TTML in extensions
    assert CaptionExtension.M3U8 in extensions

# ---------------------------- Custom Download Options Tests ---------------------------- #

def test_get_video_info_with_caption_download_options(youtube_helper):
    """Test get_video_info with custom download options for captions."""
    # Create custom download options focused on captions
    download_options = {
        'writesubtitles': True,
        'write_auto_subs': True,
        'subtitleslangs': ['en', 'es', 'fr'],
        'subtitlesformat': 'vtt'
    }
    
    # Create a minimal mock result
    mock_result = {
        'id': SAMPLE_VIDEO_ID,
        'title': 'Test Video',
        'formats': [],
        'thumbnails': [],
        'automatic_captions': {
            'en': [{'ext': 'vtt', 'url': 'https://example.com/auto_en.vtt', 'name': 'English'}]
        },
        'subtitles': {
            'en': [{'ext': 'vtt', 'url': 'https://example.com/sub_en.vtt', 'name': 'English'}]
        }
    }
    
    # Mock YoutubeDL to return our mock result
    with patch('yt_dlp.YoutubeDL') as mock_ytdl:
        mock_instance = MagicMock()
        mock_ytdl.return_value = mock_instance
        mock_instance.__enter__.return_value.extract_info.return_value = mock_result
        
        # Call get_video_info with custom download options
        youtube_helper.get_video_info(SAMPLE_VIDEO_URL, download_options=download_options)
        
        # Verify YoutubeDL was called
        mock_ytdl.assert_called_once_with()

def test_integration_with_custom_options():
    """Test integration of custom options with caption handling."""
    # Create a helper with custom options
    helper = YoutubeHelper({
        'writesubtitles': True,
        'write_auto_subs': True,
        'subtitleslangs': ['en']
    })
    
    # Create a minimal mock result
    mock_result = {
        'id': SAMPLE_VIDEO_ID,
        'title': 'Test Video',
        'formats': [],
        'thumbnails': [],
        'automatic_captions': {
            'en': [{'ext': 'vtt', 'url': 'https://example.com/auto_en.vtt', 'name': 'English'}]
        },
        'subtitles': {
            'en': [{'ext': 'vtt', 'url': 'https://example.com/sub_en.vtt', 'name': 'English'}]
        }
    }
    
    # Mock YoutubeDL to return our mock result
    with patch('yt_dlp.YoutubeDL') as mock_ytdl:
        mock_instance = MagicMock()
        mock_ytdl.return_value = mock_instance
        mock_instance.__enter__.return_value.extract_info.return_value = mock_result
        
        # Override options for a specific request
        override_options = {
            'writesubtitles': True,
            'write_auto_subs': True,
            'subtitleslangs': ['en', 'es', 'fr']  # Add more languages
        }
        
        # Call get_video_info with override options
        helper.get_video_info(SAMPLE_VIDEO_URL, download_options=override_options)
        
        # Verify YoutubeDL was called
        mock_ytdl.assert_called_once_with() 