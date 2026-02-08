## ADDED Requirements

### Requirement: Clip Concatenation Logic
The system SHALL concatenate media clips according to the timeline.

#### Scenario: Sequential clip assembly
- **GIVEN** a timeline with multiple clips in sequence
- **WHEN** the system assembles the video
- **THEN** it SHALL concatenate clips in timeline order
- **AND** preserve each clip's specified start time and duration

#### Scenario: Single clip assembly
- **GIVEN** a timeline with only one clip
- **WHEN** the system assembles the video
- **THEN** it SHALL create a video containing just that clip
- **AND** use the clip's specified duration

#### Scenario: Mixed video and image clips
- **GIVEN** a timeline with alternating video and image clips
- **WHEN** the system assembles the video
- **THEN** it SHALL correctly concatenate different clip types
- **AND** maintain proper transitions

### Requirement: Timeline-Based Clip Positioning
The system SHALL position clips according to timeline start times.

#### Scenario: Clip positioning at start time
- **GIVEN** a timeline clip with start time 5.0
- **WHEN** the system positions the clip
- **THEN** it SHALL place the clip starting at 5.0 seconds
- **AND** fill the timeline from 5.0 to (start + duration)

#### Scenario: Gaps between clips
- **GIVEN** timeline clips with gaps (e.g., 0-5s, 8-10s)
- **WHEN** the system assembles the video
- **THEN** it SHALL preserve gaps between clips
- **AND** fill gaps with black frames or silence

#### Scenario: Continuous timeline
- **GIVEN** timeline clips with no gaps (e.g., 0-5s, 5-8s, 8-12s)
- **WHEN** the system assembles the video
- **THEN** it SHALL create a seamless video
- **AND** remove black frames between clips

### Requirement: Automatic Output File Naming
The system SHALL automatically name output video files with sequential numbering.

#### Scenario: First output file creation
- **GIVEN** no existing output_*.mp4 files
- **WHEN** the system creates a new output
- **THEN** it SHALL name the file output_001.mp4

#### Scenario: Sequential file naming
- **GIVEN** existing files output_001.mp4 through output_005.mp4
- **WHEN** the system creates a new output
- **THEN** it SHALL name the file output_006.mp4
- **AND** NOT overwrite existing files

#### Scenario: Numbering with gaps
- **GIVEN** existing files output_001.mp4 and output_010.mp4
- **WHEN** the system creates a new output
- **THEN** it SHALL name the file output_011.mp4
- **AND** use the maximum existing number + 1

#### Scenario: Three-digit padding
- **GIVEN** any existing output number
- **WHEN** the system creates a new output
- **THEN** it SHALL format the number with three digits (001, 010, 100)
- **AND** include leading zeros for numbers < 100

### Requirement: Memory Cleanup
The system SHALL properly manage memory by cleaning up clip resources.

#### Scenario: Clip cleanup after processing
- **GIVEN** a VideoFileClip or ImageClip being processed
- **WHEN** the clip is no longer needed
- **THEN** the system SHALL call clip.close() to free resources
- **AND** prevent memory leaks

#### Scenario: All clips cleanup after assembly
- **GIVEN** multiple clips processed during assembly
- **WHEN** assembly is complete
- **THEN** the system SHALL close all clips
- **AND** release all associated memory

#### Scenario: Context manager usage
- **GIVEN** clips being loaded and processed
- **WHEN** using context managers for resource management
- **THEN** clips SHALL be automatically closed when exiting context
- **AND** ensure proper cleanup even on errors

### Requirement: MP4 Export
The system SHALL export assembled videos in MP4 format.

#### Scenario: Standard MP4 export
- **GIVEN** a successfully assembled video
- **WHEN** the system exports to MP4
- **THEN** it SHALL create an MP4 file at the specified output path
- **AND** use default codec settings
- **AND** maintain video quality

#### Scenario: Export with audio preservation
- **GIVEN** an assembled video containing audio tracks from source clips
- **WHEN** the system exports to MP4
- **THEN** it SHALL preserve the audio in the output
- **AND** mix audio from all clips appropriately

#### Scenario: Export without audio
- **GIVEN** an assembled video with no audio tracks
- **WHEN** the system exports to MP4
- **THEN** it SHALL create a video-only MP4 file
- **AND** NOT fail due to missing audio

### Requirement: Maximum Clips Limit
The system SHALL limit timeline to maximum 10 clips for MVP.

#### Scenario: Valid timeline with 10 clips
- **GIVEN** a timeline with exactly 10 clips
- **WHEN** the system processes the timeline
- **THEN** it SHALL accept and process all 10 clips
- **AND** successfully assemble the video

#### Scenario: Timeline exceeding 10 clips
- **GIVEN** a timeline with 11 or more clips
- **WHEN** the system validates the timeline
- **THEN** it SHALL reject the timeline
- **AND** display error `❌ Timeline exceeds maximum of 10 clips`
- **AND** exit with non-zero status

#### Scenario: Performance with 10 clips
- **GIVEN** a timeline with 10 clips of moderate duration
- **WHEN** the system processes the timeline
- **THEN** it SHALL complete processing in reasonable time (< 30 seconds)
- **AND** manage memory efficiently

### Requirement: Timeline Duration Calculation
The system SHALL calculate total timeline duration from clip specifications.

#### Scenario: Sequential timeline duration
- **GIVEN** timeline clips: 0-5s, 5-8s, 8-12s
- **WHEN** the system calculates total duration
- **THEN** it SHALL return 12.0 seconds (end of last clip)

#### Scenario: Timeline with gaps duration
- **GIVEN** timeline clips: 0-5s, 8-10s, 15-20s
- **WHEN** the system calculates total duration
- **THEN** it SHALL return 20.0 seconds (including gaps)

#### Scenario: Single clip duration
- **GIVEN** a timeline with one clip: 0-7.5s
- **WHEN** the system calculates total duration
- **THEN** it SHALL return 7.5 seconds

### Requirement: Audio Mixing
The system SHALL handle audio from multiple clips during assembly.

#### Scenario: Audio from single video clip
- **GIVEN** a timeline with one video clip containing audio
- **WHEN** the system assembles the video
- **THEN** the output SHALL include the audio from that clip
- **AND** play at original volume

#### Scenario: Audio from multiple video clips
- **GIVEN** a timeline with multiple video clips each with audio
- **WHEN** the system assembles the video
- **THEN** the output SHALL include audio from all clips
- **AND** mix audio appropriately at clip boundaries

#### Scenario: No audio from images
- **GIVEN** a timeline containing only image clips
- **WHEN** the system assembles the video
- **THEN** the output SHALL have no audio track
- **AND** NOT fail due to missing audio

#### Scenario: Mixed audio and no-audio clips
- **GIVEN** a timeline with video clips (audio) and image clips (no audio)
- **WHEN** the system assembles the video
- **THEN** the output SHALL include audio from video clips
- **AND** remain silent during image clip durations

### Requirement: Error Handling During Assembly
The system SHALL handle errors gracefully during video assembly.

#### Scenario: Failed clip loading
- **WHEN** a clip fails to load during assembly
- **THEN** the system SHALL display error for that specific clip
- **AND** NOT attempt to continue assembly
- **AND** clean up any loaded resources

#### Scenario: Export failure
- **WHEN** the system fails to export the assembled video
- **THEN** it SHALL display error with export details
- **AND** NOT create partial output file
- **AND** clean up all loaded clips

#### Scenario: Memory constraints
- **WHEN** the system encounters memory issues during assembly
- **THEN** it SHALL display appropriate error message
- **AND** clean up resources gracefully
- **AND** exit with non-zero status
