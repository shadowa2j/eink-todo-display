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

def create_todo_image(tasks, width=800, height=480):
    """
    Create an image with the to-do list
    """
    # Create a new image with white background
    image = Image.new('1', (width, height), 255)  # '1' for 1-bit pixels, white
    draw = ImageDraw.Draw(image)
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        task_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    except:
        title_font = ImageFont.load_default()
        task_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw title
    title = "TO-DO LIST"
    draw.text((20, 20), title, font=title_font, fill=0)
    
    # Draw line under title
    draw.line((20, 70, width-20, 70), fill=0, width=2)
    
    # Draw timestamp
    timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
    draw.text((20, 80), f"Updated: {timestamp}", font=small_font, fill=0)
    
    # Draw tasks
    y_position = 120
    line_height = 40
    max_tasks = (height - y_position - 20) // line_height
    
    if not tasks:
        draw.text((20, y_position), "No tasks found", font=task_font, fill=0)
    else:
        for i, task in enumerate(tasks[:max_tasks]):
            task_text = task['text']
            x_pos = 20
            
            # Draw checkbox
            box_size = 20
            draw.rectangle([x_pos, y_position, x_pos + box_size, y_position + box_size], 
                          outline=0, width=2)
            
            # Draw X if completed
            if task['completed']:
                draw.line([x_pos+4, y_position+4, x_pos+box_size-4, y_position+box_size-4], 
                         fill=0, width=2)
                draw.line([x_pos+4, y_position+box_size-4, x_pos+box_size-4, y_position+4], 
                         fill=0, width=2)
            
            # Draw task text
            text_x = x_pos + box_size + 15
            draw.text((text_x, y_position), task_text, font=task_font, fill=0)
            
            # Draw strikethrough if completed
            if task['completed']:
                # Get text width for strikethrough line
                bbox = draw.textbbox((text_x, y_position), task_text, font=task_font)
                text_width = bbox[2] - bbox[0]
                strike_y = y_position + 12
                draw.line([text_x, strike_y, text_x + text_width, strike_y], 
                         fill=0, width=2)
            
            y_position += line_height
    
    # Draw footer
    footer_text = f"Total tasks: {len(tasks)}"
    draw.text((20, height - 30), footer_text, font=small_font, fill=0)
    
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
    
    # Display dimensions (default for 7.5" displays)
    WIDTH = 800
    HEIGHT = 480
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: {CREDENTIALS_FILE} not found!")
        print("Please follow the setup instructions to create your credentials file.")
        sys.exit(1)
    
    print("Fetching tasks from Google Sheets...")
    tasks = get_tasks_from_sheet(CREDENTIALS_FILE, SHEET_NAME)
    
    print(f"Found {len(tasks)} tasks")
    
    print("Creating image...")
    image = create_todo_image(tasks, WIDTH, HEIGHT)
    
    # Save image for debugging
    image.save('todo_preview.png')
    print("Preview saved as todo_preview.png")
    
    # Display on e-ink
    display_image_on_epd(image)

if __name__ == "__main__":
    main()
