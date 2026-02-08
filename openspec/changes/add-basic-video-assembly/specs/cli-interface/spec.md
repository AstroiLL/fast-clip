## ADDED Requirements

### Requirement: CLI Command Interface
The system SHALL provide a command-line interface for assembling videos from fragments.

#### Scenario: Successful video assembly
- **GIVEN** an input directory containing media files and a valid JSON script
- **WHEN** user runs `fast-clip assemble INPUT_DIR SCRIPT.json`
- **THEN** the system SHALL assemble the video according to the script
- **AND** create an output file with automatic numbering (output_001.mp4, output_002.mp4)

#### Scenario: Display help information
- **WHEN** user runs `fast-clip --help` or `fast-clip assemble --help`
- **THEN** the system SHALL display usage information including command syntax and options

#### Scenario: Display version information
- **WHEN** user runs `fast-clip --version`
- **THEN** the system SHALL display the current version of Fast-Clip

### Requirement: Automatic Output File Numbering
The system SHALL automatically number output video files to prevent overwriting.

#### Scenario: First output file creation
- **GIVEN** no existing output_*.mp4 files in the directory
- **WHEN** the system creates a new output
- **THEN** it SHALL be named output_001.mp4

#### Scenario: Sequential output numbering
- **GIVEN** existing output files output_001.mp4 and output_002.mp4
- **WHEN** the system creates a new output
- **THEN** it SHALL be named output_003.mp4
- **AND** existing files SHALL remain unchanged

#### Scenario: Numbering with gaps
- **GIVEN** existing output files output_001.mp4 and output_005.mp4
- **WHEN** the system creates a new output
- **THEN** it SHALL be named output_006.mp4
- **AND** SHALL use the maximum existing number + 1

### Requirement: Simple Error Messages
The system SHALL provide clear, simple error messages for diagnostics.

#### Scenario: File not found error
- **WHEN** the specified JSON script file does not exist
- **THEN** the system SHALL display `❌ File not found: SCRIPT.json`
- **AND** exit with non-zero status

#### Scenario: Invalid JSON format
- **WHEN** the JSON script file contains invalid JSON syntax
- **THEN** the system SHALL display `❌ Invalid JSON format: [specific error message]`
- **AND** exit with non-zero status

#### Scenario: Missing media file
- **WHEN** a media file referenced in the script does not exist
- **THEN** the system SHALL display `❌ File not found: filename.mp4`
- **AND** exit with non-zero status

### Requirement: Progress Indication
The system SHALL provide basic progress indication during video assembly.

#### Scenario: Progress display during assembly
- **WHEN** the system is assembling a video
- **THEN** it SHALL display a progress bar or status indicator
- **AND** update the progress as each clip is processed

#### Scenario: Completion message
- **WHEN** video assembly completes successfully
- **THEN** the system SHALL display `✅ Created: output_NNN.mp4`
- **AND** include the final output filename

### Requirement: Argument Validation
The system SHALL validate CLI arguments before processing.

#### Scenario: Missing input directory
- **WHEN** user runs `fast-clip assemble SCRIPT.json` (missing INPUT_DIR)
- **THEN** the system SHALL display `❌ Missing argument: INPUT_DIR`
- **AND** display usage information
- **AND** exit with non-zero status

#### Scenario: Missing script file
- **WHEN** user runs `fast-clip assemble INPUT_DIR` (missing SCRIPT.json)
- **THEN** the system SHALL display `❌ Missing argument: SCRIPT.json`
- **AND** display usage information
- **AND** exit with non-zero status

#### Scenario: Invalid input directory
- **WHEN** the specified INPUT_DIR does not exist or is not a directory
- **THEN** the system SHALL display `❌ Invalid directory: INPUT_DIR`
- **AND** exit with non-zero status
