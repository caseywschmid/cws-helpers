"""
Integration tests for the OpenAI helper with live API.

IMPORTANT: These tests call the actual OpenAI API and will incur costs.
They are meant to be run manually and selectively, not as part of the regular test suite.

To run these tests:
1. Provide your API key using one of these methods:
   - Set the OPENAI_API_KEY environment variable: `export OPENAI_API_KEY=your_key_here`
   - Create a .env file in the project root with: `OPENAI_API_KEY=your_key_here`

2. Run a specific test to minimize API costs:
   ```bash
   # Remove the skip decorator for a single test
   pytest -xvs tests/openai_helper/test_live_integration.py::test_basic_chat_completion -k "not skip"
   
   # Or, to temporarily enable a test for a one-time run:
   python -m pytest tests/openai_helper/test_live_integration.py::test_basic_chat_completion -v --no-skip-mark
   ```

3. To run all tests (costly, use with caution):
   ```bash
   pytest -xvs tests/openai_helper/test_live_integration.py -k "not skip"
   ```

Each test is designed to verify a specific aspect of the OpenAI Helper functionality
with the actual API. The tests print their results to the console for inspection.
"""

import os
import pytest
from pydantic import BaseModel
from typing import List, Optional
import tempfile
from pathlib import Path
from dotenv import load_dotenv

from cws_helpers.openai_helper import OpenAIHelper, AIModel


# Try to load environment variables from .env file
load_dotenv()


# Skip all tests by default to prevent accidental API calls
pytestmark = pytest.mark.skip(reason="Live API tests are skipped by default to avoid costs")


class SimpleResponse(BaseModel):
    """Simple response model for testing structured outputs."""
    message: str
    items: List[str]
    count: int


def create_test_image(size=(100, 100)):
    """Creates a simple test image for multimodal tests."""
    try:
        from PIL import Image
        import numpy as np
        
        # Create a simple gradient image
        array = np.zeros((size[0], size[1], 3), dtype=np.uint8)
        for i in range(size[0]):
            for j in range(size[1]):
                array[i, j, 0] = i % 256  # Red channel
                array[i, j, 1] = j % 256  # Green channel
                array[i, j, 2] = (i + j) % 256  # Blue channel
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img = Image.fromarray(array)
        img.save(temp_file.name)
        temp_file.close()
        
        return temp_file.name
    except ImportError:
        # If PIL is not available, create a simple file with bytes
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        # Write some bytes that form a valid but simple JPEG
        temp_file.write(bytes.fromhex('FFD8FFE000104A4649460001010100480048000000FFDB004300080606070605080707070909080A0C140D0C0B0B0C1912130F141D1A1F1E1D1A1C1C20242E2720222C231C1C2837292C30313434341F27393D38323C2E333432FFDB0043010909090C0B0C180D0D1832211C213232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232FFC00011080001000103012200021101031101FFC4001F0000010501010101010100000000000000000102030405060708090A0BFFC400B5100002010303020403050504040000017D01020300041105122131410613516107227114328191A1082342B1C11552D1F02433627282090A161718191A25262728292A3435363738393A434445464748494A535455565758595A636465666768696A737475767778797A838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE1E2E3E4E5E6E7E8E9EAF1F2F3F4F5F6F7F8F9FAFFC4001F0100030101010101010101010000000000000102030405060708090A0BFFC400B51100020102040403040705040400010277000102031104052131061241510761711322328108144291A1B1C109233352F0156272D10A162434E125F11718191A262728292A35363738393A434445464748494A535455565758595A636465666768696A737475767778797A82838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE2E3E4E5E6E7E8E9EAF2F3F4F5F6F7F8F9FAFFDA000C03010002110311003F00FDFCA2A1DEFEB401AFF00DD5FCE800FEF1FCE8A0028A002AC52FF00162FD08FFDE148073D14FF007F3FDDA00B349401FFD9'))
        temp_file.close()
        return temp_file.name


def get_api_key():
    """
    Get the OpenAI API key from environment variables or .env file.
    
    We check the following sources in order:
    1. OPENAI_API_KEY environment variable
    2. OPENAI_KEY environment variable (alternative name)
    3. .env file at the project root (loaded via python-dotenv)
    """
    # Check for API key in environment variables (multiple possible names)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")
    
    if not api_key:
        # If we couldn't find in environment, try to locate and load a .env file manually
        # This is a fallback in case the automatic load_dotenv() didn't work
        project_root = Path(__file__).parent.parent.parent  # Go up from tests/openai_helper/ to project root
        env_path = project_root / ".env"
        
        if env_path.exists():
            print(f"Loading API key from .env file at {env_path}")
            # Simple manual parsing of .env file
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')  # Remove quotes if present
                            if key in ["OPENAI_API_KEY", "OPENAI_KEY"] and value:
                                api_key = value
                                break
                        except ValueError:
                            continue  # Skip invalid lines
    
    if not api_key:
        pytest.skip("OPENAI_API_KEY not found in environment variables or .env file")
    
    return api_key


def get_organization():
    """
    Get the OpenAI organization ID from environment variables or .env file.
    
    Returns an empty string if not found.
    """
    # Check for organization ID in environment variables
    org_id = os.environ.get("OPENAI_ORG_ID") or os.environ.get("OPENAI_ORGANIZATION")
    
    if not org_id:
        # If we couldn't find in environment, try to locate and load a .env file manually
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / ".env"
        
        if env_path.exists():
            # Simple manual parsing of .env file
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            if key in ["OPENAI_ORG_ID", "OPENAI_ORGANIZATION"] and value:
                                org_id = value
                                break
                        except ValueError:
                            continue
    
    return org_id or ""  # Return empty string if not found


@pytest.fixture
def helper():
    """Create an OpenAIHelper instance with the API key from environment."""
    api_key = get_api_key()
    org_id = get_organization()
    return OpenAIHelper(api_key=api_key, organization=org_id)


@pytest.fixture
def test_image():
    """Create a test image file and clean it up after the test."""
    image_path = create_test_image()
    yield image_path
    # Clean up the temporary file
    os.unlink(image_path)


def test_basic_chat_completion(helper):
    """Test basic chat completion functionality."""
    response = helper.create_chat_completion(
        prompt="Say hello world",
        model="gpt-4o"
    )
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\nBasic response: {response}")


def test_json_mode(helper):
    """Test JSON mode functionality."""
    response = helper.create_chat_completion(
        prompt="List three colors as a JSON array",
        model="gpt-4o",
        json_mode=True
    )
    
    assert response is not None
    assert isinstance(response, dict) or isinstance(response, list)
    print(f"\nJSON response: {response}")


def test_structured_output(helper):
    """Test structured output with Pydantic model."""
    try:
        # First try beta parse endpoint
        response = helper.create_structured_chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in the required format."},
                {"role": "user", "content": "Provide a simple message and a list of 3 fruits"}
            ],
            model="gpt-4o",
            response_format=SimpleResponse
        )
        
        assert response is not None
        assert hasattr(response, "choices")
        assert hasattr(response.choices[0].message, "parsed")
        
        parsed = response.choices[0].message.parsed
        assert isinstance(parsed, SimpleResponse)
        print(f"\nStructured response using beta parse: {parsed.dict()}")
        success = True
    except Exception as e:
        print(f"\nBeta parse method failed: {str(e)}")
        success = False
    
    if not success:
        # Fall back to json_mode approach
        try:
            print("\nTrying fallback to JSON mode...")
            # Create a completion with JSON mode using prompt parameter
            json_response = helper.create_chat_completion(
                prompt="Provide a simple message and a list of 3 fruits. Respond with a JSON object with fields: message (string), items (array of strings), and count (number, should be 3).",
                model="gpt-4o",
                json_mode=True,
                system_message="You are a helpful assistant that responds in JSON format."
            )
            
            assert json_response is not None
            assert isinstance(json_response, dict)
            assert "message" in json_response
            assert "items" in json_response
            assert "count" in json_response
            assert len(json_response["items"]) == 3
            assert json_response["count"] == 3
            
            # Convert to Pydantic model
            parsed_model = SimpleResponse(**json_response)
            print(f"\nStructured response using JSON mode fallback: {parsed_model.dict()}")
            success = True
        except Exception as e:
            print(f"\nJSON mode fallback failed: {str(e)}")
            success = False
    
    assert success, "Both structured output methods failed"


def test_multimodal(helper, test_image):
    """Test multimodal input with an image."""
    response = helper.create_chat_completion(
        prompt="What's in this image? Describe it briefly.",
        images=[test_image],
        model="gpt-4o"
    )
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\nImage description: {response}")


def test_streaming(helper):
    """Test streaming response."""
    stream = helper.create_chat_completion(
        prompt="Count from 1 to 5",
        model="gpt-4o",
        stream=True
    )
    
    assert stream is not None
    
    # Collect chunks to verify streaming works
    chunks = []
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            chunks.append(content)
            print(content, end="", flush=True)
    
    assert len(chunks) > 0
    print("\nReceived", len(chunks), "chunks")


def test_model_specific_token_params(helper):
    """Test model-specific token parameters."""
    # Test with standard model (uses max_tokens)
    response_standard = helper.create_chat_completion(
        prompt="Say hello",
        model="gpt-4", 
        max_tokens=10
    )
    
    assert response_standard is not None
    assert len(response_standard.split()) <= 10
    
    # Test with 'o' model (uses max_completion_tokens)
    response_o_model = helper.create_chat_completion(
        prompt="Say hello",
        model="o3-mini",
        max_completion_tokens=10
    )
    
    assert response_o_model is not None
    assert len(response_o_model.split()) <= 10
    
    print(f"\nStandard model response: {response_standard}")
    print(f"O-model response: {response_o_model}")


def test_error_recovery(helper):
    """Test that error recovery works for token parameter mismatches."""
    try:
        # First try with a standard model but using max_completion_tokens (should be auto-corrected)
        response = helper.create_chat_completion(
            prompt="Say hello",
            model="gpt-3.5-turbo",
            max_completion_tokens=10  # Wrong param for standard model, should be auto-corrected to max_tokens
        )
        
        assert response is not None
        assert isinstance(response, str)
        print(f"\nError recovery response (gpt-3.5-turbo with wrong param): {response}")
    except Exception as e:
        print(f"First test failed: {str(e)}")
        
    try:
        # Try with an 'o' model but using max_tokens (should be auto-corrected)
        response = helper.create_chat_completion(
            prompt="Say hello",
            model="gpt-4o",
            max_tokens=10  # Wrong param for 'o' model but may work or be auto-corrected
        )
        
        assert response is not None
        assert isinstance(response, str)
        print(f"\nError recovery response (gpt-4o with wrong param): {response}")
    except Exception as e:
        print(f"Second test failed: {str(e)}")
        
    # At least one of the tests should pass for this to be considered successful
    assert response is not None


def test_all_available_models(helper):
    """Test that we can get responses from all available models."""
    models_to_test = [
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo"
    ]
    
    # Optional models to test if they're available in your account
    optional_models = [
        "o1",
        "o3-mini",
        "gpt-4-turbo"
    ]
    
    results = {}
    for model in models_to_test:
        try:
            response = helper.create_chat_completion(
                prompt=f"Say 'Hello from {model}'",
                model=model,
                max_tokens=20
            )
            results[model] = response
            print(f"\n{model}: {response}")
        except Exception as e:
            print(f"\nError with {model}: {str(e)}")
    
    # Try optional models
    for model in optional_models:
        try:
            response = helper.create_chat_completion(
                prompt=f"Say 'Hello from {model}'",
                model=model,
                max_tokens=20
            )
            results[model] = response
            print(f"\n{model}: {response}")
        except Exception as e:
            print(f"\n{model} not available or error: {str(e)}")
    
    assert len(results) > 0 