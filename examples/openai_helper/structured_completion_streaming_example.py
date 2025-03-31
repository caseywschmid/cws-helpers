"""
Example of streaming structured completions with the OpenAI API.

This example demonstrates how to use the streaming functionality
to get real-time updates as the model generates a response.
"""

import os
from dotenv import load_dotenv
from cws_helpers.openai_helper import OpenAIHelper
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# Get required environment variables
api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORG_ID")

if not api_key or not organization:
    raise ValueError("OPENAI_API_KEY and OPENAI_ORG_ID must be set in environment variables")

# Define the response format using Pydantic
class EntityExtraction(BaseModel):
    """Response format for entity extraction."""
    attributes: List[str]
    colors: List[str]
    animals: List[str]


def main():
    client = OpenAIHelper(api_key=api_key, organization=organization)
    print("Initialized OpenAI client")
    print(client)

    system_message = "Extract entities from the input text"
    prompt = "The quick brown fox jumps over the lazy dog with piercing blue eyes"
    messages = client.create_messages(prompt=prompt, system_message=system_message)
    print("Created messages")
    print(messages)

    # Stream the structured completion
    print("\nStreaming response:")
    for parsed_data, is_final in client.stream_structured_completion(
        messages=messages,
        model="gpt-4o-mini",
        response_format=EntityExtraction,
        temperature=0.7,
    ):
        if is_final:
            print("\nFinal completion:")
            print(parsed_data)
        else:
            print(parsed_data)


if __name__ == "__main__":
    main()
