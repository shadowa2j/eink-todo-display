# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-17

### Added
- Dual list support - display two people's to-do lists on one screen
- Equal vertical space for each person's list
- Per-person task counts in footer
- "No tasks" message when a person has no tasks
- Person column support in Google Sheet (Task | Status | Person)

### Changed
- Google Sheet now requires three columns: Task, Status, Person
- Title changed from "TO-DO LIST" to "TO-DO LISTS"
- Each person gets their own section header (e.g., "Bryan's List")
- Footer now shows breakdown by person

### Configuration
- Set `PERSON_1 = 'Bryan'` and `PERSON_2 = 'Stacy'` at top of todo_display.py
- Names are case-sensitive and must match Google Sheet exactly

## [1.1.0] - 2025-11-17

### Added
- Portrait orientation support (now default)
- Configuration option to easily switch between portrait and landscape
- Automatic font size adjustment based on orientation
- Smaller, more compact title in portrait mode
- More tasks visible in portrait mode (~18-20 vs 8-10)

### Changed
- Default orientation changed from landscape to portrait
- Title font size reduced to 28pt in portrait mode (was 36pt)
- Task font size adjusted to 20pt in portrait mode (was 24pt)
- Line height optimized for each orientation
- Display now rotates 90° automatically for portrait mode

### Configuration
- Set `ORIENTATION = 'portrait'` or `'landscape'` at top of todo_display.py
- All layout parameters auto-adjust based on orientation

## [1.0.0] - 2025-11-16

### Added
- Initial release
- Google Sheets integration for to-do list management
- Support for Waveshare 7.5" e-ink displays (V1 and V2)
- Auto-refresh every hour via cron
- Visual checkboxes and strikethrough for completed tasks
- Automated setup script (`setup.sh`)
- Connection test script (`test_connection.py`)
- Comprehensive documentation
- MIT License

### Features
- Display up to 8-10 tasks on screen
- Automatic display rotation support
- Low power consumption (e-ink only uses power during updates)
- Edit tasks from any device via Google Sheets
- Timestamp showing last update
- Task counter in footer

### Documentation
- Complete setup instructions
- Pre-flight checklist
- Google Sheet template guide
- Troubleshooting section
- Contributing guidelines

## [Unreleased]

### Planned Features
- Support for additional display sizes
- Task priority levels
- Multiple to-do lists
- Customizable themes
- Weather integration
- Calendar integration

---

## Version History

- **1.2.0** (2025-11-17): Dual list support (Bryan & Stacy)
- **1.1.0** (2025-11-17): Portrait mode support, configurable orientation
- **1.0.0** (2025-11-16): Initial public release
