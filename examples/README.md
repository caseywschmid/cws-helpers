# CWS Helpers Examples

This directory contains example scripts demonstrating how to use the various helpers in the `cws-helpers` package.

## Available Examples

### YouTube Helper

- **[youtube_caption_demo.py](youtube_caption_demo.py)**: Demonstrates the improved caption handling in the YouTube helper, including:
  - Basic caption extraction from YouTube videos
  - Using custom download options for better caption retrieval
  - Processing captions for different use cases
  - Inspecting raw video information for debugging

## Running the Examples

To run the examples, you'll need to have the `cws-helpers` package installed. You can install it directly from GitHub:

```bash
pip install git+https://github.com/caseywschmid/cws-helpers.git
```

Alternatively, if you're working with a local copy of the repository, you can install it in development mode:

```bash
# From the root directory of the repository
pip install -e .
```

Then, you can run any example script:

```bash
python examples/youtube_caption_demo.py
```

## Environment Variables

Some examples may require environment variables to be set. You can create a `.env` file in the root directory of the repository with the necessary variables. See the individual example scripts for details on what environment variables they require. 