#!/usr/bin/env python3
"""Fast-Clip: Video assembly tool from JSON scripts."""

import json
import sys
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips, vfx
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


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

    @model_validator(mode='after')
    def validate_timeline(self):
        if len(self.timeline) > 10:
            raise ValueError("Timeline cannot have more than 10 clips (MVP limit)")
        return self


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


def load_and_process_clip(
    resources_dir: Path,
    item: TimelineItem
) -> VideoFileClip:
    """Load video clip and apply effects."""
    video_path = resources_dir / item.resource
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    # Load video and extract subclip
    start_sec = parse_time(item.time_start)
    end_sec = parse_time(item.time_end)
    
    clip = VideoFileClip(str(video_path)).subclipped(start_sec, end_sec)
    
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
    
    print(f"Loading {len(config.timeline)} clips from {resources_dir}...")
    
    clips = []
    for item in config.timeline:
        print(f"  Processing clip {item.id}: {item.resource}")
        clip = load_and_process_clip(resources_dir, item)
        clips.append(clip)
    
    print(f"Concatenating clips...")
    final_video = concatenate_videoclips(clips)
    
    # Determine output path
    output_path = script_dir / config.result_file
    
    # Auto-numbering if file exists
    counter = 1
    base_name = output_path.stem
    extension = output_path.suffix
    while output_path.exists():
        output_path = script_dir / f"{base_name}_{counter:03d}{extension}"
        counter += 1
    
    print(f"Writing video to {output_path}...")
    final_video.write_videofile(str(output_path), codec='libx264')
    
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
    print()
    
    script_dir = script_path.parent
    output_path = assemble_video(config, script_dir)
    
    print(f"\nVideo assembled successfully: {output_path}")


if __name__ == "__main__":
    main()
