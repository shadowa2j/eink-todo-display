# E-Ink To-Do List Display

Display your Google Sheets to-do list on a Waveshare 7.5" e-ink display connected to a Raspberry Pi. Supports dual lists for two people!

![E-Ink Display](https://img.shields.io/badge/Display-Waveshare%207.5%22-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-red)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- ✅ **Dual Lists** - Display two people's to-do lists (Bryan & Stacy) with equal space
- ✅ **Sync with Google Sheets** - Edit your to-do list from any device
- ✅ **Auto-update** - Refreshes every hour automatically
- ✅ **Portrait Mode** - Optimized vertical layout showing more tasks
- ✅ **Visual feedback** - Checkboxes and strikethrough for completed tasks
- ✅ **Low power** - E-ink display uses power only during updates
- ✅ **Easy setup** - Automated installation script included
- ✅ **Hardware compatible** - Works with V1 and V2 Waveshare displays

## What You'll Need

### Hardware
- Raspberry Pi 4 (or 3B+)
- Waveshare 7.5" e-Paper HAT (any version)
- MicroSD card with Raspberry Pi OS
- Internet connection

### Software
- Google account
- Google Cloud project (free)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/shadowa2j/eink-todo-display.git
cd eink-todo-display
```

### 2. Follow Setup Guide

Read **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** for complete step-by-step instructions.

**Quick overview:**
1. Set up Google Sheets API credentials (~15 min)
2. Run installation script on Raspberry Pi (~10 min)
3. Test and configure (~5 min)

### 3. Run

```bash
# Test Google Sheets connection first
python3 test_connection.py

# Display on e-ink
python3 todo_display.py
```

## Google Sheet Format

Create a Google Sheet with three columns:

| Task              | Status | Person |
|-------------------|--------|--------|
| Buy groceries     |        | Bryan  |
| Call dentist      | done   | Stacy  |
| Fix bike tire     |        | Bryan  |
| Schedule meeting  |        | Stacy  |

- **Task**: Your task description
- **Status**: Leave empty for active tasks, type `done` for completed
- **Person**: Name of person (must match exactly: `Bryan` or `Stacy`)

## Display Preview

```
┌──────────────────────────────┐
│ TO-DO LISTS        Nov 17    │
│──────────────────────────────│
│ Bryan's List                 │
│ ────────────────────────     │
│ ☐ Buy groceries              │
│ ☑ Fix bike tire              │
│ ☐ Call mechanic              │
│ ...                          │
│──────────────────────────────│
│ Stacy's List                 │
│ ────────────────────────     │
│ ☐ Schedule meeting           │
│ ☑ Call dentist               │
│ ☐ Pick up dry cleaning       │
│ ...                          │
│──────────────────────────────│
│ Total: 6 (Bryan: 3, Stacy: 3)│
└──────────────────────────────┘
```

## Installation

### Automated Setup

```bash
chmod +x setup.sh
./setup.sh
sudo reboot
```

The setup script will:
- Install required system packages
- Enable SPI interface
- Install Python dependencies
- Download Waveshare e-Paper library

### Manual Setup

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed manual installation steps.

## Configuration

Edit `todo_display.py` to customize:

```python
# Orientation: 'portrait' or 'landscape'
ORIENTATION = 'portrait'

# Names for the two lists (case-sensitive!)
PERSON_1 = 'Bryan'  # Top half of display
PERSON_2 = 'Stacy'  # Bottom half of display

# Google Sheet name
SHEET_NAME = 'My To-Do List'
```

## Automatic Updates

Set up hourly updates with cron:

```bash
crontab -e
```

Add this line:
```
0 * * * * cd /home/pi/eink-todo-display && /usr/bin/python3 todo_display.py >> /home/pi/eink-todo-display/log.txt 2>&1
```

## File Structure

```
eink-todo-display/
├── README.md                    # This file
├── SETUP_INSTRUCTIONS.md        # Detailed setup guide
├── START_HERE.md               # Quick orientation guide
├── CHECKLIST.md                # Pre-flight checklist
├── LICENSE                     # MIT License
├── todo_display.py             # Main display script
├── test_connection.py          # Test Google Sheets connection
├── setup.sh                    # Installation script
├── requirements.txt            # Python dependencies
├── GOOGLE_SHEET_TEMPLATE.md    # Sheet format guide
└── CHANGELOG.md                # Version history
```

## Troubleshooting

### Common Issues

**Display not working**
- Ensure SPI is enabled: `sudo raspi-config` → Interface Options → SPI
- Check HAT is properly connected to GPIO pins
- Reboot after enabling SPI

**"credentials.json not found"**
- Make sure credentials file is in the project folder
- Follow Google Sheets API setup in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

**"Permission denied" when accessing sheet**
- Share Google Sheet with service account email
- Email is found in `credentials.json` under `client_email`

**Tasks not showing up**
- Make sure Person column matches exactly (`Bryan` not `bryan`)
- Names are case-sensitive

**Module import errors**
- Run `./setup.sh` to install dependencies
- Use `--break-system-packages` flag on newer Raspberry Pi OS

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for more troubleshooting help.

## Testing

Test your Google Sheets connection before running the display:

```bash
python3 test_connection.py
```

This will verify:
- ✓ Credentials file exists
- ✓ Authentication works
- ✓ Sheet can be accessed
- ✓ Data can be read

## Version History

- **v1.2.0** - Dual list support (Bryan & Stacy)
- **v1.1.0** - Portrait mode, configurable orientation
- **v1.0.0** - Initial release

See [CHANGELOG.md](CHANGELOG.md) for full details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Waveshare e-Paper library](https://github.com/waveshare/e-Paper) for display drivers
- [gspread](https://github.com/burnash/gspread) for Google Sheets integration

## Support

- 📖 Full documentation: [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- 🐛 Issues: [GitHub Issues](https://github.com/shadowa2j/eink-todo-display/issues)
- 💬 Questions: Open a discussion or issue

## Author

Created for Raspberry Pi enthusiasts who want a simple, low-power to-do list display.

---

**Star ⭐ this repo if you find it useful!**
