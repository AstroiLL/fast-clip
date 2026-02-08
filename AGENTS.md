<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# AGENTS.md

This file provides guidelines and commands for agentic coding agents working in this repository.

## Build, Lint, and Test Commands

```bash
# Install dependencies
uv sync

# Run the main application
uv run python main.py

# Run tests (pytest recommended)
uv run pytest                    # Run all tests
uv run pytest tests/test_file.py  # Run single test file
uv run pytest tests/test_file.py::test_function  # Run specific test

# Type checking
uv run mypy .                    # Check all files
uv run mypy path/to/file.py     # Check specific file

# Linting (ruff recommended)
uv run ruff check .              # Lint all files
uv run ruff check path/to/file.py  # Lint specific file
uv run ruff check --fix .        # Auto-fix linting issues

# Formatting (ruff format recommended)
uv run ruff format .             # Format all files
uv run ruff format path/to/file.py  # Format specific file
```

## Project Overview

This is a Python console utility that uses moviepy to assemble video projects from fragments (video clips, images, audio files). A JSON script file in the input directory defines the sequence and timing of fragments.

## Code Style Guidelines

### Imports
- Group imports in order: standard library, third-party, local
- Use `from x import y` for specific imports
- Avoid `from x import *`
- Keep imports at the top of files

Example:
```python
import os
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips

from fast_clip.video_assembler import VideoAssembler
```

### Formatting
- Use ruff formatter (PEP 8 compliant)
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Use f-strings for string interpolation
- Add trailing commas in multi-line collections

Example:
```python
def process_video(
    input_path: Path,
    output_path: Path,
    duration: float,
) -> VideoFileClip:
    """Process a video clip with the given duration."""
    clip = VideoFileClip(str(input_path))
    return clip.subclip(0, duration)
```

### Type Hints
- Use type hints for all function parameters and return values
- Import types from `typing` module as needed
- Use `Path` from `pathlib` for file paths
- Use `Final` for constants

Example:
```python
from pathlib import Path
from typing import Optional, List, Dict, Final

DEFAULT_DURATION: Final[float] = 2.0

def assemble_clips(
    clips: List[VideoFileClip],
    output_path: Path,
    audio_track: Optional[AudioFileClip] = None,
) -> None:
    """Assemble video clips into a final output."""
    pass
```

### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Dunder methods**: `__dunder__`

Example:
```python
MAX_FRAMES_PER_SECOND = 30

class VideoFragment:
    def __init__(self, name: str, start_time: float):
        self.name = name
        self._start_time = start_time

    def _validate_timing(self) -> bool:
        return self._start_time >= 0

    def __repr__(self) -> str:
        return f"VideoFragment({self.name})"
```

### Error Handling
- Use specific exception types
- Include descriptive error messages
- Handle expected failures gracefully
- Use context managers for resource cleanup

Example:
```python
def load_clip(file_path: Path) -> VideoFileClip:
    """Load a video clip from the given path."""
    if not file_path.exists():
        raise FileNotFoundError(f"Video file not found: {file_path}")

    try:
        clip = VideoFileClip(str(file_path))
    except Exception as e:
        raise ValueError(f"Failed to load video clip: {file_path}") from e

    return clip
```

### Documentation
- Use Google-style docstrings for functions and classes
- Include parameter types and return types
- Add brief descriptions for public methods
- Keep docstrings up-to-date with code

Example:
```python
def assemble_video(
    input_dir: Path,
    script_path: Path,
    output_path: Path,
) -> None:
    """Assemble a video from fragments according to a JSON script.

    Args:
        input_dir: Directory containing video fragments and resources.
        script_path: Path to JSON file describing assembly sequence.
        output_path: Path where the final video will be saved.

    Raises:
        FileNotFoundError: If input directory or script doesn't exist.
        ValueError: If script format is invalid.
    """
    pass
```

### Project Structure
- Keep main.py minimal (CLI entry point only)
- Create separate modules for core functionality
- Use type-safe data classes for configuration
- Organize tests in a `tests/` directory

Recommended structure:
```
fast_clip/
├── __init__.py
├── cli.py              # Command-line interface
├── video_assembler.py  # Core assembly logic
├── script_parser.py    # JSON script parsing
└── models.py           # Data models

tests/
├── test_video_assembler.py
├── test_script_parser.py
└── fixtures/           # Test data
```

### moviepy Specific Guidelines
- Always close clips with `.close()` to free resources
- Use context managers when possible
- Be aware of memory usage with large video files
- Cache expensive operations like clip loading
- Use appropriate codecs and bitrates for output

Example:
```python
def process_clip(clip: VideoFileClip) -> VideoFileClip:
    """Process a clip with resource cleanup."""
    try:
        processed = clip.resize(height=1080)
        return processed
    finally:
        clip.close()
```

### Testing
- Write tests for all public functions
- Use pytest fixtures for common setup
- Mock expensive operations (file I/O, video processing)
- Include both positive and negative test cases
- Keep tests fast and isolated

Example:
```python
import pytest
from pathlib import Path

def test_assemble_clips(tmp_path: Path):
    """Test assembling clips into a final video."""
    script = create_test_script(tmp_path)
    output = tmp_path / "output.mp4"

    assemble_video(tmp_path, script, output)

    assert output.exists()
    assert output.stat().st_size > 0
```

### Performance Considerations
- Process large videos in chunks when possible
- Use `without_audio()` for audio-less video operations
- Preload resources when processing multiple clips
- Consider parallel processing for independent operations
- Profile code when working with performance issues

## Notes
- This project uses Python 3.13+
- moviepy is the primary dependency for video operations
- JSON scripts define the video assembly sequence
- All file paths should use `pathlib.Path` for cross-platform compatibility
