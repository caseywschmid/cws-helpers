"""
An example showcasing how structured completions can be generated using the OpenAI API.
"""

import os
from typing import List
from cws_helpers.openai_helper import OpenAIHelper
from cws_helpers.logger import configure_logging
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


log = configure_logging(__name__)
api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORG_ID")

# Initialize the OpenAI helper
client = OpenAIHelper(api_key=api_key, organization=organization)
log.info("Initialized OpenAI client")
log.info(client)

class Step(BaseModel):
    explanation: str
    output: str


class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str


class MathResponseWithExplanation(MathResponse):
    explanation: str


system_message = "You are a helpful math tutor."
prompt = "solve 8x + 31 = 2"

messages = client.create_messages(prompt=prompt, system_message=system_message)
log.info("Created messages")
log.info(messages)


completion = client.create_structured_chat_completion(
    model="gpt-4o-2024-08-06",
    messages=messages,
    response_format=MathResponseWithExplanation,
)

log.info(completion)

message = completion.choices[0].message
if message.parsed:
    log.warning(f"Structured response detected: {type(message.parsed)}")
    log.info(message.parsed.steps)
    log.info(f"answer: {message.parsed.final_answer}")
    