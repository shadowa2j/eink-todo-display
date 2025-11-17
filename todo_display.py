#!/usr/bin/env python3
"""
E-Ink To-Do List Display
Reads tasks from Google Sheets and displays them on Waveshare 7.5" e-ink display
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
ORIENTATION = 'portrait'  # Options: 'portrait' or 'landscape'

# Add the Waveshare library path
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

def get_tasks_from_sheet(credentials_file, sheet_name):
    """
    Read tasks from Google Sheets
    Expected format:
    Column A: Task description
    Column B: Status (empty or 'done')
    """
    try:
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        # Authenticate
        creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open(sheet_name).sheet1
        
        # Get all records
        records = sheet.get_all_records()
        
        tasks = []
        for record in records:
            task = record.get('Task', '')
            status = record.get('Status', '').lower()
            if task:  # Only add non-empty tasks
                tasks.append({
                    'text': task,
                    'completed': status == 'done'
                })
        
        return tasks
    except Exception as e:
        print(f"Error reading from Google Sheets: {e}")
        return []

def create_todo_image(tasks, width=800, height=480, orientation='landscape'):
    """
    Create an image with the to-do list
    Supports both portrait and landscape orientations
    """
    # Create a new image with white background
    image = Image.new('1', (width, height), 255)  # '1' for 1-bit pixels, white
    draw = ImageDraw.Draw(image)
    
    # Adjust font sizes based on orientation
    if orientation == 'portrait':
        title_size = 28
        task_size = 20
        small_size = 14
        line_height = 35
    else:  # landscape
        title_size = 36
        task_size = 24
        small_size = 16
        line_height = 40
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', title_size)
        task_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', task_size)
        small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', small_size)
    except:
        title_font = ImageFont.load_default()
        task_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw title
    title = "TO-DO LIST"
    draw.text((20, 15), title, font=title_font, fill=0)
    
    # Draw line under title
    title_line_y = 55 if orientation == 'portrait' else 70
    draw.line((20, title_line_y, width-20, title_line_y), fill=0, width=2)
    
    # Draw timestamp
    timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
    timestamp_y = title_line_y + 10
    draw.text((20, timestamp_y), f"Updated: {timestamp}", font=small_font, fill=0)
    
    # Draw tasks
    y_position = timestamp_y + 35
    max_tasks = (height - y_position - 30) // line_height
    
    if not tasks:
        draw.text((20, y_position), "No tasks found", font=task_font, fill=0)
    else:
        for i, task in enumerate(tasks[:max_tasks]):
            task_text = task['text']
            x_pos = 20
            
            # Draw checkbox
            box_size = 18 if orientation == 'portrait' else 20
            draw.rectangle([x_pos, y_position, x_pos + box_size, y_position + box_size], 
                          outline=0, width=2)
            
            # Draw X if completed
            if task['completed']:
                draw.line([x_pos+4, y_position+4, x_pos+box_size-4, y_position+box_size-4], 
                         fill=0, width=2)
                draw.line([x_pos+4, y_position+box_size-4, x_pos+box_size-4, y_position+4], 
                         fill=0, width=2)
            
            # Draw task text
            text_x = x_pos + box_size + 12
            draw.text((text_x, y_position), task_text, font=task_font, fill=0)
            
            # Draw strikethrough if completed
            if task['completed']:
                # Get text width for strikethrough line
                bbox = draw.textbbox((text_x, y_position), task_text, font=task_font)
                text_width = bbox[2] - bbox[0]
                strike_y = y_position + (10 if orientation == 'portrait' else 12)
                draw.line([text_x, strike_y, text_x + text_width, strike_y], 
                         fill=0, width=2)
            
            y_position += line_height
    
    # Draw footer
    footer_text = f"Total tasks: {len(tasks)}"
    draw.text((20, height - 25), footer_text, font=small_font, fill=0)
    
    return image

def display_image_on_epd(image):
    """
    Display the image on the e-ink display
    Supports both V1 and V2 versions of Waveshare 7.5" displays
    """
    try:
        # Try to import the epd module
        try:
            from waveshare_epd import epd7in5_V2
            epd_module = epd7in5_V2
            print("Using 7.5inch V2 display driver")
        except ImportError:
            try:
                from waveshare_epd import epd7in5
                epd_module = epd7in5
                print("Using 7.5inch V1 display driver")
            except ImportError:
                print("ERROR: Could not import Waveshare e-Paper library!")
                print("Please run ./setup.sh first to download the library.")
                raise
        
        print("Initializing e-ink display...")
        epd = epd_module.EPD()
        epd.init()
        epd.Clear()
        
        print("Displaying image...")
        epd.display(epd.getbuffer(image))
        
        print("Putting display to sleep...")
        epd.sleep()
        print("Done!")
        
    except Exception as e:
        print(f"Error displaying on e-ink: {e}")
        raise

def main():
    # Configuration
    CREDENTIALS_FILE = 'credentials.json'
    SHEET_NAME = 'My To-Do List'  # Change this to your Google Sheet name
    
    # Display dimensions based on orientation
    if ORIENTATION == 'portrait':
        WIDTH = 480
        HEIGHT = 800
        print(f"Display mode: Portrait ({WIDTH}x{HEIGHT})")
    else:  # landscape
        WIDTH = 800
        HEIGHT = 480
        print(f"Display mode: Landscape ({WIDTH}x{HEIGHT})")
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: {CREDENTIALS_FILE} not found!")
        print("Please follow the setup instructions to create your credentials file.")
        sys.exit(1)
    
    print("Fetching tasks from Google Sheets...")
    tasks = get_tasks_from_sheet(CREDENTIALS_FILE, SHEET_NAME)
    
    print(f"Found {len(tasks)} tasks")
    
    print("Creating image...")
    image = create_todo_image(tasks, WIDTH, HEIGHT, ORIENTATION)
    
    # Rotate image if needed for display orientation
    if ORIENTATION == 'portrait':
        image = image.rotate(90, expand=True)  # Rotate 90 degrees for portrait
    
    # Save image for debugging
    image.save('todo_preview.png')
    print("Preview saved as todo_preview.png")
    
    # Display on e-ink
    display_image_on_epd(image)
    image.save('todo_preview.png')
    print("Preview saved as todo_preview.png")
    
    # Display on e-ink
    display_image_on_epd(image)

if __name__ == "__main__":
    main()
