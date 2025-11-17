# Update to Portrait Mode - Instructions

This guide shows you how to update your Raspberry Pi to the new portrait mode version.

## What Changed

✅ **Default orientation**: Now portrait (480x800)  
✅ **Smaller title**: More compact header  
✅ **More tasks visible**: ~18-20 tasks instead of 8-10  
✅ **Easy to switch**: Change one line to go back to landscape  

## Update Steps

### Step 1: Update Your Local Repository (On Your Computer)

Navigate to your project folder:

**Windows:**
```bash
cd C:\Users\Support\Downloads\eink-todo
```

**Mac/Linux:**
```bash
cd ~/Downloads/eink-todo
```

### Step 2: Pull Latest Changes from This Chat

Download the updated file:
- [Download updated todo_display.py](computer:///mnt/user-data/outputs/eink-todo/todo_display.py)

Replace your current `todo_display.py` with this new version.

### Step 3: Commit and Push to GitHub

```bash
git add todo_display.py
git commit -m "Add portrait mode support with smaller title"
git push
```

### Step 4: Update Your Raspberry Pi

SSH into your Pi:
```bash
ssh pi@raspberrypi.local
```

Navigate to your project and pull the changes:
```bash
cd ~/eink-todo-display
git pull origin main
```

### Step 5: Test It

Run the display script:
```bash
python3 todo_display.py
```

You should see:
- `Display mode: Portrait (480x800)` in the output
- A portrait-oriented display with smaller title
- More tasks visible (~18-20 tasks)

## How to Switch Back to Landscape

If you want to switch back to landscape mode:

### On Your Raspberry Pi:

1. Edit the file:
```bash
nano todo_display.py
```

2. Find this line near the top (around line 16):
```python
ORIENTATION = 'portrait'  # Options: 'portrait' or 'landscape'
```

3. Change it to:
```python
ORIENTATION = 'landscape'  # Options: 'portrait' or 'landscape'
```

4. Save and exit (Ctrl+X, then Y, then Enter)

5. Run again:
```bash
python3 todo_display.py
```

## Preview Before Displaying

The script saves a preview image called `todo_preview.png` in the project folder. You can check this on your Pi:

```bash
# View the preview (if you have a desktop environment)
xdg-open todo_preview.png

# Or copy it to your computer to view
# On your computer:
scp pi@raspberrypi.local:~/eink-todo-display/todo_preview.png .
```

## Troubleshooting

**Display looks wrong or rotated incorrectly:**
- Make sure you're using the latest version of the script
- Check that `ORIENTATION = 'portrait'` is set at the top of the file
- Try rebooting the Pi if the display doesn't update correctly

**Text is too small/large:**
- The font sizes are automatically adjusted for portrait mode
- Portrait: Title=28, Tasks=20, Small=14
- Landscape: Title=36, Tasks=24, Small=16

**Want to fine-tune the layout:**
- Edit the font sizes around line 71-78
- Adjust line_height around line 79-84
- All layout parameters automatically adjust based on orientation

## What's Different in Portrait Mode

| Feature | Landscape | Portrait |
|---------|-----------|----------|
| Dimensions | 800x480 | 480x800 |
| Title Size | 36pt | 28pt |
| Task Font | 24pt | 20pt |
| Line Height | 40px | 35px |
| Tasks Visible | ~8-10 | ~18-20 |
| Checkbox Size | 20px | 18px |

## Next Steps

Once you've updated and tested:
- Your hourly cron job will automatically use the new portrait mode
- You can switch between portrait and landscape anytime by editing one line
- The preview image helps you see what it will look like before displaying

Enjoy your portrait to-do list! 📱
