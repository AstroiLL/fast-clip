# Implementation Tasks

## 1. Infrastructure Setup
- [ ] 1.1 Update pyproject.toml with dependencies (moviepy, typer, pydantic, pillow)
- [ ] 1.2 Add dev dependencies (pytest, pytest-mock)
- [ ] 1.3 Create fast_clip module directory structure
- [ ] 1.4 Update main.py to use new module

## 2. Test Media Files Creation
- [ ] 2.1 Create tests/fixtures/ directory
- [ ] 2.2 Create script to generate test video_001.mp4 (2s, red background)
- [ ] 2.3 Create script to generate test video_002.mp4 (3s, blue background)
- [ ] 2.4 Create script to generate test image_001.jpg (1920x1080, green background)
- [ ] 2.5 Create script to generate test image_002.png (1920x1080, yellow background)
- [ ] 2.6 Add test media files to .gitignore
- [ ] 2.7 Create fixture loading utilities

## 3. CLI Interface Implementation
- [ ] 3.1 Implement Typer CLI command `fast-clip assemble`
- [ ] 3.2 Add argument validation for INPUT_DIR and SCRIPT.json
- [ ] 3.3 Implement automatic output file numbering
- [ ] 3.4 Add progress indication
- [ ] 3.5 Add simple error messages
- [ ] 3.6 Add --version and --help flags

## 4. Script Parser Implementation
- [ ] 4.1 Create Pydantic models for JSON validation
- [ ] 4.2 Implement timeline model with start/duration
- [ ] 4.3 Add default values for images (duration=3.0, resolution=1920x1080)
- [ ] 4.4 Validate timeline structure and logic
- [ ] 4.5 Add maximum 10 clips validation
- [ ] 4.6 Implement JSON file loading and validation

## 5. Media Loader Implementation
- [ ] 5.1 Implement VideoFileClip loading for .mp4 files
- [ ] 5.2 Implement ImageClip loading for .jpg/.png files
- [ ] 5.3 Add landscape format resize (1920x1080) for images
- [ ] 5.4 Implement file existence validation
- [ ] 5.5 Add format validation (.mp4, .jpg, .png only)
- [ ] 5.6 Create simple error messages

## 6. Video Assembler Implementation
- [ ] 6.1 Implement clip concatenation logic
- [ ] 6.2 Add timeline-based clip positioning
- [ ] 6.3 Implement automatic output file naming (output_NNN.mp4)
- [ ] 6.4 Add memory cleanup (clip.close())
- [ ] 6.5 Optimize for 10 clips maximum
- [ ] 6.6 Implement MP4 export with default settings

## 7. Testing
- [ ] 7.1 Create unit tests for script parser
- [ ] 7.2 Create unit tests for media loader
- [ ] 7.3 Create unit tests for video assembler
- [ ] 7.4 Create integration test with test media files
- [ ] 7.5 Create error handling tests
- [ ] 7.6 Create performance test with 10 clips
- [ ] 7.7 Test auto-numbering logic

## 8. Documentation
- [ ] 8.1 Update README.md with usage examples
- [ ] 8.2 Add JSON script format documentation
- [ ] 8.3 Document CLI command usage
- [ ] 8.4 Add project description to pyproject.toml

## 9. Code Quality
- [ ] 9.1 Run ruff format on all files
- [ ] 9.2 Run ruff check and fix linting issues
- [ ] 9.3 Run mypy type checking
- [ ] 9.4 Ensure all tests pass
