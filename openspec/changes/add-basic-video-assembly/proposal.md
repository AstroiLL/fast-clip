# Change: Add Basic Video Assembly Infrastructure

## Why
Create a minimal working version of Fast-Clip that can assemble videos from video clips and images using JSON scripts, providing a foundation for future enhancements.

## What Changes
- Add CLI command `fast-clip assemble INPUT_DIR SCRIPT.json` for video assembly
- Implement JSON script parser with Pydantic validation
- Add media loader supporting .mp4, .jpg, .png formats
- Implement basic video assembler with concatenation logic
- Add automatic output file numbering (output_001.mp4, output_002.mp4)
- Create test media files for integration testing
- Support landscape format (1920x1080) for images by default
- Limit timeline to maximum 10 clips for MVP

## Impact
- Affected specs: cli-interface, script-parser, media-loader, video-assembler
- Affected code: pyproject.toml, new fast_clip module, tests/
- Breaking changes: None (new functionality)
