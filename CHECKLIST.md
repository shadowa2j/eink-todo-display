# Pre-Flight Checklist

Use this checklist before starting to make sure you have everything ready.

## Hardware ✓

- [ ] Raspberry Pi 4 with Raspberry Pi OS installed
- [ ] Waveshare 7.5" e-Paper HAT (any version)
- [ ] Internet connection working on Pi
- [ ] SSH access OR keyboard/monitor connected

## Accounts & Access ✓

- [ ] Google account (for Google Sheets)
- [ ] Can access Google Cloud Console
- [ ] Comfortable using terminal/command line (or can follow instructions)

## Files You'll Create ✓

- [ ] Google Cloud project (you'll create this)
- [ ] credentials.json (downloaded from Google Cloud)
- [ ] Google Sheet with your to-do list
- [ ] Files from this package on your Raspberry Pi

## Steps Overview

### Phase 1: Google Setup (~15 minutes)
1. Create Google Cloud project
2. Enable APIs
3. Create service account
4. Download credentials.json
5. Create Google Sheet
6. Share sheet with service account

### Phase 2: Raspberry Pi Setup (~10 minutes)
1. Copy files to Pi
2. Run setup.sh
3. Reboot
4. Connect display

### Phase 3: Testing (~5 minutes)
1. Run test_connection.py
2. Fix any issues
3. Run todo_display.py
4. Set up hourly updates

## Common Gotchas (Read This!)

🚨 **You MUST reboot after running setup.sh** - SPI won't work without it!

🚨 **Sheet name must match exactly** - "My To-Do List" is case-sensitive

🚨 **Must share sheet with service account** - It's an email like xxx@xxx.iam.gserviceaccount.com

🚨 **Column headers must be exact** - "Task" and "Status" (capital T and S)

🚨 **Display must be firmly seated** - Push the HAT all the way onto GPIO pins

🚨 **"done" must be lowercase** - Type exactly "done" in Status column

## Quick Test Before You Start

Can you answer YES to all of these?

- [ ] I can SSH into my Raspberry Pi OR connect a keyboard/monitor
- [ ] My Pi has internet access
- [ ] I have a Google account
- [ ] I can create projects in Google Cloud Console
- [ ] I'm ready to spend ~30 minutes on setup

If you answered YES to all, you're ready to start!

## Start Here

1. Open **SETUP_INSTRUCTIONS.md**
2. Follow it step by step
3. Use **test_connection.py** to verify Google Sheets works
4. Run **todo_display.py** when ready

## If You Get Stuck

Common issues and solutions:

**"credentials.json not found"**
→ Make sure it's in the eink-todo folder with the scripts

**"Permission denied" when reading sheet**
→ Share the sheet with your service account email (it's in credentials.json)

**"Module 'waveshare_epd' not found"**
→ Run ./setup.sh and reboot

**Display doesn't update**
→ Check that SPI is enabled: sudo raspi-config → Interface Options → SPI

**"pip install" fails**
→ Make sure you're using the --break-system-packages flag

Good luck! 🎉
