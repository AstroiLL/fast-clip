# Design: Basic Video Assembly

## Context
Fast-Clip is a Python console utility for assembling video projects from fragments (video clips, images, audio files) using JSON scripts. This initial implementation focuses on basic functionality with MP4 video and JPG/PNG image support, automatic output numbering, and simple error messages.

Constraints:
- Support maximum 10 clips in timeline for MVP
- Use landscape format (1920x1080) for images by default
- Simple error diagnostics only
- Automatic output file numbering

## Goals / Non-Goals

**Goals:**
- Minimal working version of video assembly
- Simple CLI interface with smart defaults
- Robust JSON validation with Pydantic
- Reliable media loading with clear error messages
- Memory-efficient processing with proper cleanup

**Non-Goals:**
- Complex layering or overlay effects
- Audio processing beyond simple mixing
- Video transformations (crop, rotate, filters)
- Preview functionality
- Performance optimization beyond 10 clips
- Advanced error reporting

## Decisions

### 1. CLI Framework: Typer
**Decision**: Use Typer for CLI implementation
**Rationale**:
- Modern, type-safe framework with Python 3.13 support
- Automatic help generation and argument validation
- Simple and intuitive API
- Excellent documentation and community support

**Alternatives considered**:
- argparse: Too verbose, less type-safe
- click: Older, less Pythonic syntax
- No CLI framework: Too much boilerplate code

### 2. JSON Validation: Pydantic
**Decision**: Use Pydantic models for JSON script validation
**Rationale**:
- Type-safe data models with automatic validation
- Clear error messages for invalid JSON
- Supports default values and constraints
- Python 3.13 compatible

**Alternatives considered**:
- jsonschema: More complex API, less Pythonic
- Manual validation: Error-prone, time-consuming

### 3. Video Processing: moviepy
**Decision**: Use moviepy for video assembly
**Rationale**:
- Directly matches project requirements
- Simple API for clip concatenation
- Built-in support for video, audio, and images
- Established library with good documentation

**Alternatives considered**:
- ffmpeg-python: Lower-level, more complex
- opencv: Overkill for simple concatenation

### 4. Module Structure: Simple Modular Design
**Decision**: Separate modules for CLI, parser, loader, assembler
**Rationale**:
- Clear separation of concerns
- Easy to test individual components
- Scalable for future enhancements
- Follows Python best practices

**Module layout**:
```
fast_clip/
├── cli.py              # Typer CLI with auto-numbering
├── script_parser.py    # Pydantic JSON models
├── media_loader.py     # MP4/JPG/PNG loading
├── video_assembler.py   # Assembly logic + export
├── models.py           # Shared data classes
└── utils.py            # Helper functions
```

### 5. Image Handling: Landscape Default
**Decision**: Default images to landscape format (1920x1080)
**Rationale**:
- Common video format
- Simple user expectation
- Avoids portrait-to-landscape distortion
- Easy to override in future

**Implementation**: Use ImageClip resize on load

### 6. Output Naming: Auto-Numbering
**Decision**: Automatic sequential numbering (output_001.mp4, output_002.mp4)
**Rationale**:
- Prevents accidental overwrites
- Simple file organization
- No manual naming required
- Easy to track output history

**Algorithm**: Scan for output_*.mp4, extract max number, increment by 1, pad to 3 digits

### 7. Memory Management: Immediate Cleanup
**Decision**: Call clip.close() immediately after processing
**Rationale**:
- Prevents memory leaks with large video files
- Essential for moviepy resource management
- Supports 10-clip limit without issues

### 8. Error Strategy: Fail-Fast with Simple Messages
**Decision**: Immediate error exit with clear message
**Rationale**:
- Easy to understand for users
- No confusing partial outputs
- Simple to implement and maintain

**Message format**: `❌ Error: description`

## Architecture Patterns

### Error Handling
```python
try:
    result = operation()
except FileNotFoundError as e:
    raise typer.Exit(f"❌ File not found: {e.filename}", code=1)
except pydantic.ValidationError as e:
    raise typer.Exit(f"❌ Invalid JSON format: {e}", code=1)
except Exception as e:
    raise typer.Exit(f"❌ Failed to load file: {e}", code=1)
```

### Resource Management (from Context7 docs)
```python
from moviepy.editor import VideoFileClip

# Automatic cleanup using context manager (recommended)
with VideoFileClip(path) as clip:
    processed = process_clip(clip)
    processed.write_videofile("output.mp4")
# clip.close() is automatically called here

# Manual cleanup for multiple clips
clips = []
for file_path in file_paths:
    clip = VideoFileClip(file_path)
    clips.append(clip)

try:
    final = concatenate_videoclips(clips)
    final.write_videofile("output.mp4")
finally:
    # Always close all clips to release resources
    for clip in clips:
        clip.close()
```

### Auto-Numbering
```python
def get_next_output_number(output_dir: Path) -> int:
    existing = output_dir.glob("output_*.mp4")
    numbers = [int(f.stem.split("_")[1]) for f in existing if f.stem.split("_")[1].isdigit()]
    return max(numbers, default=0) + 1

# Format with 3-digit padding
output_name = f"output_{next_number:03d}.mp4"
```

### Image Processing with Pillow
```python
from PIL import Image

def resize_to_landscape(image_path: Path, target_size: tuple[int, int] = (1920, 1080)) -> Path:
    """Resize image to landscape format maintaining aspect ratio."""
    with Image.open(image_path) as img:
        # Use BICUBIC resampling for better quality (from Context7)
        resized = img.resize(target_size, Image.BICUBIC)
        # Save to temporary location for moviepy processing
        output_path = image_path.parent / f"resized_{image_path.name}"
        resized.save(output_path)
        return output_path
```

## Risks / Trade-offs

### Risk 1: MoviePy Memory Usage
**Risk**: Large video files may consume significant memory
**Mitigation**:
- Limit to 10 clips maximum
- Immediate clip cleanup
- Clear memory management documentation

### Risk 2: Test Media File Size
**Risk**: Test media files in git repository could be large
**Mitigation**:
- Keep test files minimal (2-3 seconds)
- Use solid colors instead of complex scenes
- Add to .gitignore if they grow too large

### Risk 3: JSON Complexity
**Risk**: Users might create complex JSON scripts that fail validation
**Mitigation**:
- Clear Pydantic error messages
- Provide example JSON scripts in documentation
- Limit complexity in MVP (no nested structures)

### Trade-off: Simplicity vs. Features
**Trade-off**: Choosing minimal features over rich functionality
**Rationale**:
- Faster implementation
- Lower complexity
- Better testing coverage
- Easier to extend later

## Migration Plan

### No migration needed (new feature)

## Open Questions

1. **Test media generation**: Should we use actual moviepy to generate test files or mock the entire media loading?
   - **Decision**: Use real moviepy to generate small test media files in tests/fixtures/ for realistic integration testing

2. **Performance with 10 clips**: Should we add timing metrics to ensure acceptable performance?
   - **Decision**: Add performance test but no strict timing requirements for MVP

3. **Output quality**: Should we specify video codec/bitrate settings?
   - **Decision**: Use moviepy defaults for MVP, add configuration options in future

## Dependencies

### Core Dependencies
```toml
moviepy>=2.0.0    # Video processing - concatenate_videoclips, VideoFileClip, ImageClip
typer>=0.9.0      # CLI framework - app.command(), typer.echo()
pydantic>=2.0.0   # JSON validation - BaseModel, model_validate_json
pillow>=10.0.0    # Image processing - resize((width, height)), Image.BICUBIC
```

### Key API Patterns from Context7 Documentation:

**MoviePy:**
```python
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

# Load video with automatic resource cleanup
with VideoFileClip("video.mp4") as clip:
    processed = clip.subclipped(0, 5)
    processed.write_videofile("output.mp4")

# Create image clip with duration
image_clip = ImageClip("image.jpg").with_duration(3)

# Concatenate clips
final = concatenate_videoclips([clip1, clip2, clip3])
final.write_videofile("output.mp4")
```

**Typer:**
```python
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def assemble(
    input_dir: Path = typer.Argument(..., help="Directory with media files"),
    script_path: Path = typer.Argument(..., help="JSON script file")
):
    """Assemble video from script."""
    typer.echo(f"Processing {script_path.name}")

if __name__ == "__main__":
    app()
```

**Pydantic:**
```python
from pydantic import BaseModel, Field

class TimelineEntry(BaseModel):
    file: str
    start: float
    duration: float = Field(gt=0, default=3.0)

class Script(BaseModel):
    timeline: list[TimelineEntry] = Field(max_length=10)

# Validate JSON from file
with open("script.json") as f:
    script = Script.model_validate_json(f.read())
```

**Pillow:**
```python
from PIL import Image

# Resize to landscape format
with Image.open("image.jpg") as img:
    resized = img.resize((1920, 1080), Image.BICUBIC)
    resized.save("resized.jpg")
```

### Dev Dependencies
```toml
pytest>=7.0.0         # Testing framework
pytest-mock>=3.10.0   # Mocking utilities
```

## Performance Considerations

### Memory
- Expected usage: 10 clips, max 10 seconds each
- Memory optimization: Immediate clip cleanup
- No caching required for MVP

### Processing Time
- Expected: <30 seconds for 10-clip timeline
- No parallelization needed for MVP
- Simple concatenation is fast enough

## Testing Strategy

### Unit Tests
- Each module tested in isolation
- Mock external dependencies (moviepy)
- 80%+ code coverage target

### Integration Tests
- End-to-end workflow with test media files
- Real moviepy operations
- Auto-numbering logic validation

### Error Handling Tests
- Missing files
- Invalid formats
- Timeline overlaps
- Invalid JSON structure

### Performance Tests
- 10-clip timeline processing
- Memory usage verification
- Output file generation

## Future Enhancements (Out of Scope)

- Audio track processing
- Image overlays and layers
- Video transformations (crop, rotate, scale)
- Preview generation
- Configuration files for default settings
- Format options (codec, bitrate, resolution)
- Custom output naming patterns
