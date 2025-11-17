# GitHub Setup Guide

Quick guide for setting up this project from GitHub.

## 1. Clone the Repository

```bash
# Via HTTPS
git clone https://github.com/YOUR_USERNAME/eink-todo-display.git
cd eink-todo-display

# Or via SSH
git clone git@github.com:YOUR_USERNAME/eink-todo-display.git
cd eink-todo-display
```

## 2. Transfer to Raspberry Pi

### Option A: Direct Clone on Pi
```bash
# SSH into your Pi
ssh pi@raspberrypi.local

# Clone directly
git clone https://github.com/YOUR_USERNAME/eink-todo-display.git
cd eink-todo-display
```

### Option B: Clone Locally, Then Copy
```bash
# Clone on your computer
git clone https://github.com/YOUR_USERNAME/eink-todo-display.git

# Copy to Pi via SCP
scp -r eink-todo-display pi@raspberrypi.local:~/

# SSH into Pi
ssh pi@raspberrypi.local
cd eink-todo-display
```

### Option C: Download ZIP
1. Click "Code" → "Download ZIP" on GitHub
2. Extract the zip file
3. Copy to your Pi using your preferred method

## 3. Follow Main Setup

Once files are on your Pi, follow **SETUP_INSTRUCTIONS.md**:

1. Set up Google Sheets API (on your computer)
2. Copy `credentials.json` to the project folder
3. Run `./setup.sh` on the Pi
4. Reboot the Pi
5. Run `python3 test_connection.py`
6. Run `python3 todo_display.py`

## 4. Keep Updated

To get the latest updates:

```bash
cd ~/eink-todo-display
git pull origin main
```

## Need Help?

- 📖 Full documentation: [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- 🚀 Quick start: [START_HERE.md](START_HERE.md)
- ✅ Pre-flight: [CHECKLIST.md](CHECKLIST.md)
- 🐛 Issues: [Open an issue](https://github.com/YOUR_USERNAME/eink-todo-display/issues)
