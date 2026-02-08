## ADDED Requirements

### Requirement: Supported Media Formats
The system SHALL support loading of specific media file formats.

#### Scenario: MP4 video format support
- **GIVEN** a file with .mp4 extension
- **WHEN** the system loads the file
- **THEN** it SHALL successfully load as VideoFileClip
- **AND** support standard video features (playback, audio)

#### Scenario: JPG image format support
- **GIVEN** a file with .jpg extension
- **WHEN** the system loads the file
- **THEN** it SHALL successfully load as ImageClip
- **AND** convert to video-compatible format

#### Scenario: PNG image format support
- **GIVEN** a file with .png extension
- **WHEN** the system loads the file
- **THEN** it SHALL successfully load as ImageClip
- **AND** convert to video-compatible format

#### Scenario: Unsupported format rejection
- **GIVEN** a file with .avi, .mov, or other unsupported extension
- **WHEN** the system attempts to load it
- **THEN** it SHALL reject the file
- **AND** display error `❌ Invalid format: filename.ext (supported: .mp4, .jpg, .png)`

### Requirement: Video File Loading
The system SHALL load video files using moviepy VideoFileClip.

#### Scenario: Successful MP4 loading
- **GIVEN** a valid MP4 file at specified path
- **WHEN** the system loads it as VideoFileClip
- **THEN** it SHALL create a VideoFileClip object
- **AND** return it for processing

#### Scenario: MP4 file with audio
- **GIVEN** an MP4 file containing audio
- **WHEN** the system loads it
- **THEN** it SHALL load both video and audio tracks
- **AND** preserve audio for final assembly

#### Scenario: Corrupted MP4 file handling
- **GIVEN** a corrupted or invalid MP4 file
- **WHEN** the system attempts to load it
- **THEN** it SHALL raise an error
- **AND** display appropriate error message

### Requirement: Image File Loading
The system SHALL load image files using moviepy ImageClip with default processing.

#### Scenario: Successful JPG loading
- **GIVEN** a valid JPG file at specified path
- **WHEN** the system loads it as ImageClip
- **THEN** it SHALL create an ImageClip object
- **AND** return it for processing

#### Scenario: Successful PNG loading
- **GIVEN** a valid PNG file at specified path
- **WHEN** the system loads it as ImageClip
- **THEN** it SHALL create an ImageClip object
- **AND** return it for processing

#### Scenario: Corrupted image file handling
- **GIVEN** a corrupted or invalid image file
- **WHEN** the system attempts to load it
- **THEN** it SHALL raise an error
- **AND** display appropriate error message

### Requirement: Image Format Processing
The system SHALL process image files with default landscape format.

#### Scenario: Default landscape resolution
- **GIVEN** an image file loaded by the system
- **WHEN** the system processes it
- **THEN** it SHALL resize to landscape format [1920, 1080]
- **AND** maintain aspect ratio
- **AND** add black bars if necessary

#### Scenario: Portrait image handling
- **GIVEN** a portrait orientation image file
- **WHEN** the system processes it
- **THEN** it SHALL resize to landscape [1920, 1080]
- **AND** center the image with black bars on sides

#### Scenario: Small image handling
- **GIVEN** a small image file (e.g., 320x240)
- **WHEN** the system processes it
- **THEN** it SHALL resize to landscape [1920, 1080]
- **AND** upscale maintaining quality as much as possible

### Requirement: File Existence Validation
The system SHALL validate that media files exist before loading.

#### Scenario: Existing file validation
- **GIVEN** a media file that exists at specified path
- **WHEN** the system validates the file
- **THEN** it SHALL confirm the file exists
- **AND** proceed with loading

#### Scenario: Non-existent file validation
- **GIVEN** a media file that does not exist
- **WHEN** the system validates the file
- **THEN** it SHALL detect the missing file
- **AND** display error `❌ File not found: filename.ext`
- **AND** exit with non-zero status

#### Scenario: Directory path validation
- **GIVEN** a path to a directory instead of a file
- **WHEN** the system validates the path
- **THEN** it SHALL detect it's not a file
- **AND** display error `❌ Not a file: directoryname/`
- **AND** exit with non-zero status

### Requirement: Format Validation
The system SHALL validate media file formats before processing.

#### Scenario: Extension-based format validation
- **GIVEN** a file with .mp4, .jpg, or .png extension
- **WHEN** the system validates the format
- **THEN** it SHALL accept the format

#### Scenario: Case-insensitive extension handling
- **GIVEN** a file with extension .MP4, .JPG, or .PNG (uppercase)
- **WHEN** the system validates the format
- **THEN** it SHALL accept the format
- **AND** treat it the same as lowercase extensions

#### Scenario: Invalid extension rejection
- **GIVEN** a file with extension .avi, .mov, .gif, etc.
- **WHEN** the system validates the format
- **THEN** it SHALL reject the format
- **AND** display error `❌ Invalid format: filename.ext (supported: .mp4, .jpg, .png)`

### Requirement: Simple Error Messages
The system SHALL provide simple, clear error messages for media loading failures.

#### Scenario: File not found error
- **WHEN** a media file is not found at the specified path
- **THEN** the system SHALL display `❌ File not found: filename.ext`
- **AND** indicate the exact filename

#### Scenario: Format error
- **WHEN** a media file has an unsupported format
- **THEN** the system SHALL display `❌ Invalid format: filename.ext (supported: .mp4, .jpg, .png)`
- **AND** list supported formats

#### Scenario: Loading error
- **WHEN** a media file fails to load due to corruption or other issues
- **THEN** the system SHALL display `❌ Failed to load file: filename.ext`
- **AND** include brief error context

### Requirement: Image Duration Setting
The system SHALL set duration for image clips during loading.

#### Scenario: Duration from script
- **GIVEN** an image file with duration specified in script as 5.0
- **WHEN** the system loads the image
- **THEN** it SHALL set the clip duration to 5.0 seconds

#### Scenario: Default duration for images
- **GIVEN** an image file without duration specified
- **WHEN** the system loads the image
- **THEN** it SHALL apply default duration of 3.0 seconds

#### Scenario: Duration enforcement
- **GIVEN** an image clip loaded with specific duration
- **WHEN** the system processes it
- **THEN** the clip SHALL play for exactly the specified duration
- **AND** not automatically loop
