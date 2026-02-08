## ADDED Requirements

### Requirement: JSON Script Format
The system SHALL use a JSON script format to define video assembly sequence.

#### Scenario: Basic timeline format
- **GIVEN** a JSON script with timeline array
- **WHEN** the system parses the script
- **THEN** it SHALL accept the format:
```json
{
  "timeline": [
    {
      "file": "video_001.mp4",
      "start": 0.0,
      "duration": 5.0
    },
    {
      "file": "image_001.jpg",
      "start": 5.0,
      "duration": 3.0
    }
  ]
}
```

#### Scenario: Required fields validation
- **GIVEN** a JSON script entry
- **WHEN** the system validates the entry
- **THEN** it SHALL require fields: file, start, duration
- **AND** reject entries missing any required field

#### Scenario: Optional fields handling
- **GIVEN** a JSON script entry
- **WHEN** the system parses optional fields
- **THEN** it SHALL apply defaults if not specified

### Requirement: Timeline Field Validation
The system SHALL validate timeline fields according to type and value constraints.

#### Scenario: File field validation
- **GIVEN** a timeline entry with file field
- **WHEN** the system validates the file field
- **THEN** it SHALL accept string values
- **AND** reject non-string values
- **AND** reject empty strings

#### Scenario: Start time validation
- **GIVEN** a timeline entry with start field
- **WHEN** the system validates the start time
- **THEN** it SHALL accept non-negative float values (0.0, 5.5, etc.)
- **AND** reject negative values
- **AND** reject non-numeric values

#### Scenario: Duration validation
- **GIVEN** a timeline entry with duration field
- **WHEN** the system validates the duration
- **THEN** it SHALL accept positive float values (0.5, 5.0, etc.)
- **AND** reject zero or negative values
- **AND** reject non-numeric values

### Requirement: Default Values for Images
The system SHALL apply default values for image files when not specified.

#### Scenario: Default duration for images
- **GIVEN** a timeline entry for an image file (.jpg, .png)
- **WHEN** duration is not specified
- **THEN** the system SHALL use default duration of 3.0 seconds

#### Scenario: Default resolution for images
- **GIVEN** a timeline entry for an image file (.jpg, .png)
- **WHEN** resolution is not specified
- **THEN** the system SHALL use default resolution of [1920, 1080] (landscape format)

#### Scenario: Explicit values override defaults
- **GIVEN** a timeline entry for an image file with explicit duration
- **WHEN** duration is specified as 5.0
- **THEN** the system SHALL use the specified duration 5.0
- **AND** NOT apply the default 3.0 seconds

### Requirement: Timeline Validation
The system SHALL validate timeline structure and logic constraints.

#### Scenario: Maximum clips validation
- **GIVEN** a JSON script with timeline entries
- **WHEN** the system validates the timeline
- **THEN** it SHALL accept up to 10 clips
- **AND** reject timelines with more than 10 clips with error `❌ Timeline exceeds maximum of 10 clips`

#### Scenario: Non-overlapping times validation
- **GIVEN** a timeline with multiple entries
- **WHEN** the system validates time overlaps
- **THEN** it SHALL reject overlapping time ranges
- **AND** display error `❌ Timeline error: overlapping times (start-end and start-end)`
- **EXAMPLE**: Entry 1 (0.0-5.0) and Entry 2 (4.0-8.0) SHALL be rejected

#### Scenario: Sequential times validation
- **GIVEN** a timeline with sequential entries
- **WHEN** times do not overlap
- **THEN** the system SHALL accept the timeline
- **EXAMPLE**: Entry 1 (0.0-5.0) and Entry 2 (5.0-8.0) SHALL be accepted

### Requirement: JSON File Loading
The system SHALL load and parse JSON script files from the filesystem.

#### Scenario: Successful JSON loading
- **GIVEN** a valid JSON script file at the specified path
- **WHEN** the system loads the file
- **THEN** it SHALL successfully parse the JSON content
- **AND** return a validated data structure

#### Scenario: Invalid JSON syntax handling
- **GIVEN** a file with invalid JSON syntax
- **WHEN** the system attempts to parse it
- **THEN** it SHALL raise a validation error
- **AND** include specific error details (e.g., "Expected ',' delimiter at line 3")

#### Scenario: Empty file handling
- **GIVEN** an empty JSON file
- **WHEN** the system attempts to parse it
- **THEN** it SHALL raise a validation error
- **AND** indicate the file is empty

### Requirement: Pydantic Model Validation
The system SHALL use Pydantic models for type-safe JSON validation.

#### Scenario: Type enforcement
- **GIVEN** a Pydantic model with field types
- **WHEN** JSON data violates type constraints
- **THEN** Pydantic SHALL raise a ValidationError
- **AND** include field name, expected type, and actual value

#### Scenario: Nested validation
- **GIVEN** a Pydantic model with nested models (timeline items)
- **WHEN** nested data is invalid
- **THEN** Pydantic SHALL raise a ValidationError
- **AND** include path to invalid field

#### Scenario: Clear error messages
- **GIVEN** a Pydantic validation error
- **WHEN** the error is displayed to user
- **THEN** it SHALL provide clear, actionable error messages
- **EXAMPLE**: "field 'duration' must be greater than 0"
