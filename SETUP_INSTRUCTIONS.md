# E-Ink To-Do List Display - Setup Instructions

This guide will walk you through setting up your Raspberry Pi to display a to-do list from Google Sheets on your Waveshare 7.5" e-ink display.

## Hardware Requirements
- Raspberry Pi 4
- Waveshare 7.5" e-Paper HAT
- MicroSD card with Raspberry Pi OS
- Internet connection

## Part 1: Google Sheets API Setup

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Name it "EInk ToDo" → Click "Create"
4. Wait for the project to be created

### 1.2 Enable Google Sheets API

1. In the Google Cloud Console, make sure your new project is selected
2. Go to "APIs & Services" → "Library"
3. Search for "Google Sheets API"
4. Click on it and click "Enable"
5. Also search for "Google Drive API" and enable it

### 1.3 Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Enter a name like "eink-todo-reader"
4. Click "Create and Continue"
5. Skip the optional steps, click "Done"

### 1.4 Create and Download Key

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON" format
5. Click "Create" - a file will download
6. **Rename this file to `credentials.json`**

### 1.5 Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it **"My To-Do List"** (or change the name in the Python script)
4. In the first row, create headers:
   - Column A: `Task`
   - Column B: `Status`
5. Add your tasks:
   - Column A: Your task description (e.g., "Buy groceries")
   - Column B: Leave empty for active tasks, type "done" for completed tasks

Example:
```
| Task              | Status |
|-------------------|--------|
| Buy groceries     |        |
| Call dentist      | done   |
| Fix bike tire     |        |
| Pay electric bill | done   |
```

### 1.6 Share Sheet with Service Account

1. Open your `credentials.json` file with a text editor
2. Find the email address (looks like: `eink-todo-reader@...gserviceaccount.com`)
3. Copy this email address
4. In your Google Sheet, click "Share" button
5. Paste the service account email
6. Give it "Viewer" access
7. Click "Send" (uncheck "Notify people" if prompted)

## Part 2: Raspberry Pi Setup

### 2.1 Copy Files to Raspberry Pi

1. Copy all files from this folder to your Raspberry Pi:
   ```bash
   scp -r eink-todo pi@raspberrypi.local:~/
   ```
   Or use a USB drive, or download directly on the Pi

2. Also copy your `credentials.json` file to the same folder:
   ```bash
   scp credentials.json pi@raspberrypi.local:~/eink-todo/
   ```

### 2.2 Run Setup Script

1. SSH into your Raspberry Pi or open a terminal
2. Navigate to the project folder:
   ```bash
   cd ~/eink-todo
   ```

3. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. The script will:
   - Update your system
   - Install required packages
   - Download Waveshare libraries
   - Set up SPI interface

5. **Reboot your Raspberry Pi** after setup:
   ```bash
   sudo reboot
   ```

### 2.3 Connect the E-Ink Display

1. Power off your Raspberry Pi
2. Connect the Waveshare 7.5" e-Paper HAT to the 40-pin GPIO header
3. Make sure it's firmly seated
4. Power on the Raspberry Pi

## Part 3: Running the To-Do List Display

### 3.1 Test Your Connection First

Before testing the display, verify your Google Sheets connection works:

1. Navigate to the project folder:
   ```bash
   cd ~/eink-todo
   ```

2. Run the test script:
   ```bash
   python3 test_connection.py
   ```

3. This will check:
   - credentials.json file exists
   - Authentication works
   - Sheet can be opened
   - Data can be read

4. If all tests pass, you're ready for the display!
   If any fail, follow the error messages to fix the issue.

### 3.2 Test the Display

1. Navigate to the project folder:
   ```bash
   cd ~/eink-todo
   ```

2. Run the script:
   ```bash
   python3 todo_display.py
   ```

3. You should see:
   - "Fetching tasks from Google Sheets..."
   - "Found X tasks"
   - "Creating image..."
   - "Displaying image..."

4. Your to-do list should appear on the e-ink display!

### 3.3 Configure Auto-Update (Every Hour)

To make it update automatically every hour:

1. Open crontab editor:
   ```bash
   crontab -e
   ```
   (Choose nano editor if asked)

2. Add this line at the end:
   ```
   0 * * * * cd /home/pi/eink-todo && /usr/bin/python3 todo_display.py >> /home/pi/eink-todo/log.txt 2>&1
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

4. This will run the script at the start of every hour

## Part 4: Usage

### Updating Your To-Do List

1. Open your Google Sheet in any browser or on your phone
2. Add, edit, or delete tasks in column A
3. Mark tasks as done by typing "done" in column B
4. The display will update automatically every hour
5. Or manually run: `python3 todo_display.py`

### Troubleshooting

**"credentials.json not found"**
- Make sure `credentials.json` is in the same folder as `todo_display.py`

**"Permission denied" errors**
- Make sure you shared the Google Sheet with your service account email
- The email is in your `credentials.json` file

**Display not working**
- Make sure SPI is enabled: `sudo raspi-config` → Interface Options → SPI → Enable
- Check that the HAT is properly connected
- Try rebooting

**"Module not found" errors**
- Make sure you ran `./setup.sh`
- Try reinstalling: `pip3 install -r requirements.txt`

**Display shows old data**
- Check your internet connection
- Look at the log file: `cat ~/eink-todo/log.txt`

### Customization

You can edit `todo_display.py` to customize:
- Line 87: Change `SHEET_NAME` if your sheet has a different name
- Font sizes (lines 50-52)
- Display layout
- Update frequency in crontab

## Questions?

If something doesn't work, check:
1. Internet connection is working
2. SPI is enabled (`sudo raspi-config`)
3. Credentials file is in the right place
4. Google Sheet is shared with service account
5. Sheet name matches in the script

Good luck with your e-ink to-do list! 📝
