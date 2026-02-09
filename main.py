#!/usr/bin/env python3
"""Fast-Clip: Video assembly tool from JSON scripts."""

import json
import sys
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips, vfx, ColorClip, CompositeVideoClip
from moviepy.video.VideoClip import VideoClip
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Tuple, Union


# Supported formats and resolutions
SUPPORTED_FORMATS = {"mp4", "avi", "mov", "mkv"}
FORMAT_CODECS = {
    "mp4": "libx264",
    "avi": "mpeg4",
    "mov": "libx264",
    "mkv": "libx264"
}

# Resolution definitions (height in pixels)
RESOLUTIONS = {
    "2160p": 2160,  # 4K
    "1440p": 1440,  # 2K
    "1080p": 1080,  # Full HD
    "720p": 720,    # HD
    "480p": 480     # SD
}

# Orientation aspect ratios (width/height)
ORIENTATION_RATIOS = {
    "landscape": 16/9,
    "portrait": 9/16,
    "square": 1/1
}


class TimelineItem(BaseModel):
    """Single timeline item configuration."""
    id: int = Field(..., ge=1, description="Sequence number")
    resource: str = Field(..., description="Video filename")
    time_start: str = Field(..., description="Start time MM:SS or HH:MM:SS")
    time_end: str = Field(..., description="End time MM:SS or HH:MM:SS")
    start_effect: Optional[str] = Field(None, description="Effect at start: fade_in")
    start_duration: Optional[str] = Field(None, description="Effect duration: Xs")
    effect_during: Optional[str] = Field(None, description="Effect during playback")
    end_effect: Optional[str] = Field(None, description="Effect at end: fade_out")
    end_duration: Optional[str] = Field(None, description="Effect duration: Xs")
    description: Optional[str] = Field(None, description="Optional description")


class ScriptConfig(BaseModel):
    """Video assembly script configuration."""
    name: str = Field(..., description="Project name")
    resources_dir: str = Field(..., description="Resources directory name")
    timeline: List[TimelineItem] = Field(..., description="Video sequence")
    result_file: str = Field(..., description="Output filename")
    output_format: Optional[str] = Field(None, description="Output format: mp4, avi, mov, mkv")
    resolution: Optional[str] = Field("1080p", description="Resolution: 2160p, 1440p, 1080p, 720p, 480p")
    orientation: Optional[str] = Field("landscape", description="Video orientation: landscape, portrait, square")

    @model_validator(mode='after')
    def validate_timeline(self):
        if len(self.timeline) > 10:
            raise ValueError("Timeline cannot have more than 10 clips (MVP limit)")
        return self

    def get_output_format(self) -> Optional[str]:
        """Validate and return output format, or None if invalid."""
        if not self.output_format:
            return None
        fmt = self.output_format.lower().lstrip('.')
        if fmt not in SUPPORTED_FORMATS:
            print(f"Warning: Unsupported output format '{self.output_format}'. Using source format.")
            return None
        return fmt

    def get_resolution(self) -> Optional[int]:
        """Validate and return resolution height, or None if invalid."""
        if not self.resolution:
            return None
        res = self.resolution.lower()
        if res not in RESOLUTIONS:
            print(f"Warning: Unsupported resolution '{self.resolution}'. Valid values: {', '.join(RESOLUTIONS.keys())}. Using source resolution.")
            return None
        return RESOLUTIONS[res]

    def get_orientation(self) -> Optional[str]:
        """Validate and return orientation, or None if not specified/invalid."""
        if not self.orientation:
            return None
        orient = self.orientation.lower()
        if orient not in ORIENTATION_RATIOS:
            print(f"Warning: Unsupported orientation '{self.orientation}'. Will detect from first clip.")
            return None
        return orient


def parse_time(time_str: str) -> float:
    """Convert time string to seconds."""
    parts = time_str.split(':')
    if len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def parse_duration(duration_str: Optional[str]) -> float:
    """Convert duration string to seconds."""
    if not duration_str:
        return 0.0
    if duration_str.endswith('s'):
        return float(duration_str[:-1])
    return float(duration_str)


def detect_orientation_from_size(width: int, height: int) -> str:
    """Detect orientation from video dimensions."""
    aspect_ratio = width / height
    if aspect_ratio > 1.1:
        return "landscape"
    elif aspect_ratio < 0.9:
        return "portrait"
    else:
        return "square"


def calculate_target_size(resolution_height: Optional[int], orientation: Optional[str]) -> Optional[Tuple[int, int]]:
    """Calculate target container size based on resolution and orientation."""
    if resolution_height is None or orientation is None:
        return None
    
    aspect_ratio = ORIENTATION_RATIOS[orientation]
    
    if orientation == "landscape":
        width = int(resolution_height * aspect_ratio)
        height = resolution_height
    elif orientation == "portrait":
        width = resolution_height
        height = int(resolution_height / aspect_ratio)
    else:  # square
        width = resolution_height
        height = resolution_height
    
    # Ensure even dimensions (required by most codecs)
    width = width if width % 2 == 0 else width - 1
    height = height if height % 2 == 0 else height - 1
    
    return (width, height)


def fit_video_to_container(clip: VideoFileClip, container_size: Tuple[int, int]) -> VideoClip:
    """Fit video into container preserving aspect ratio, with black bars."""
    container_width, container_height = container_size
    clip_width, clip_height = clip.size
    
    # Calculate scaling factor to fit within container
    scale_w = container_width / clip_width
    scale_h = container_height / clip_height
    scale = min(scale_w, scale_h)
    
    # Calculate new size
    new_width = int(clip_width * scale)
    new_height = int(clip_height * scale)
    
    # Ensure even dimensions
    new_width = new_width if new_width % 2 == 0 else new_width - 1
    new_height = new_height if new_height % 2 == 0 else new_height - 1
    
    # Resize video
    resized_clip = clip.resized((new_width, new_height))
    
    # Create black background
    bg_clip = ColorClip(size=container_size, color=(0, 0, 0), duration=resized_clip.duration)
    
    # Center the resized video on black background
    x_center = (container_width - new_width) // 2
    y_center = (container_height - new_height) // 2
    
    final_clip = CompositeVideoClip([bg_clip, resized_clip.with_position((x_center, y_center))])
    
    return final_clip


def load_and_process_clip(
    resources_dir: Path,
    item: TimelineItem,
    target_size: Optional[Tuple[int, int]]
) -> Union[VideoFileClip, VideoClip]:
    """Load video clip and apply effects."""
    video_path = resources_dir / item.resource
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    # Load video and extract subclip
    start_sec = parse_time(item.time_start)
    end_sec = parse_time(item.time_end)
    
    clip = VideoFileClip(str(video_path)).subclipped(start_sec, end_sec)
    
    # Apply target size if specified (fit with black bars)
    if target_size:
        try:
            clip = fit_video_to_container(clip, target_size)
        except Exception as e:
            print(f"Warning: Cannot fit video to container: {e}. Using original size.")
    
    # Apply start effect (fade in)
    if item.start_effect == "fade_in" and item.start_duration:
        duration = parse_duration(item.start_duration)
        clip = clip.with_effects([vfx.FadeIn(duration)])
    
    # Apply end effect (fade out)
    if item.end_effect == "fade_out" and item.end_duration:
        duration = parse_duration(item.end_duration)
        clip = clip.with_effects([vfx.FadeOut(duration)])
    
    return clip


def assemble_video(config: ScriptConfig, script_dir: Path) -> Path:
    """Assemble video from script configuration."""
    resources_dir = script_dir / config.resources_dir
    
    # Get resolution
    resolution_height = config.get_resolution()
    
    # Get orientation from config or detect from first clip
    orientation = config.get_orientation()
    
    if orientation is None:
        # Load first clip to detect orientation
        first_item = config.timeline[0]
        first_video_path = resources_dir / first_item.resource
        if first_video_path.exists():
            temp_clip = VideoFileClip(str(first_video_path))
            width, height = temp_clip.size
            orientation = detect_orientation_from_size(width, height)
            temp_clip.close()
            print(f"Detected orientation from first clip: {orientation} ({width}x{height})")
        else:
            orientation = "landscape"
            print(f"Warning: Cannot detect orientation, first clip not found. Using landscape.")
    
    target_size = calculate_target_size(resolution_height, orientation)
    
    if target_size:
        print(f"Target size: {target_size[0]}x{target_size[1]} ({orientation})")
    else:
        print(f"Using original video sizes (orientation: {orientation})")
    
    # Get output format
    output_format = config.get_output_format()
    
    print(f"Loading {len(config.timeline)} clips from {resources_dir}...")
    
    clips: List[Union[VideoFileClip, VideoClip]] = []
    for item in config.timeline:
        print(f"  Processing clip {item.id}: {item.resource}")
        clip = load_and_process_clip(resources_dir, item, target_size)
        clips.append(clip)
    
    print(f"Concatenating clips...")
    final_video = concatenate_videoclips(clips)
    
    # Determine output path
    output_path = script_dir / config.result_file
    
    # Change extension if output format specified
    if output_format:
        output_path = output_path.with_suffix(f".{output_format}")
    
    # Auto-numbering if file exists
    counter = 1
    base_name = output_path.stem
    extension = output_path.suffix
    while output_path.exists():
        output_path = script_dir / f"{base_name}_{counter:03d}{extension}"
        counter += 1
    
    # Determine codec based on format
    fmt = output_format or output_path.suffix.lstrip('.').lower()
    codec = FORMAT_CODECS.get(fmt, 'libx264')
    
    print(f"Writing video to {output_path} (codec: {codec})...")
    final_video.write_videofile(str(output_path), codec=codec)
    
    # Cleanup
    for clip in clips:
        clip.close()
    final_video.close()
    
    return output_path


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <script.json>")
        print("Example: python main.py script_video_01.json")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        sys.exit(1)
    
    print(f"Loading script: {script_path}")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    config = ScriptConfig(**data)
    print(f"Project: {config.name}")
    print(f"Resources: {config.resources_dir}")
    print(f"Output: {config.result_file}")
    if config.output_format:
        print(f"Format: {config.output_format}")
    if config.resolution:
        print(f"Resolution: {config.resolution}")
    if config.orientation:
        print(f"Orientation: {config.orientation}")
    print()
    
    script_dir = script_path.parent
    output_path = assemble_video(config, script_dir)
    
    print(f"\nVideo assembled successfully: {output_path}")


if __name__ == "__main__":
    main()
