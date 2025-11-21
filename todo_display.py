#!/usr/bin/env python3
"""
E-Ink To-Do List Display
Reads tasks from Google Sheets and displays them on Waveshare 7.5" e-ink display
Supports dual lists (Bryan and Stacy) with equal space
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

# Dual list configuration
PERSON_1 = 'Bryan'  # Top half of display
PERSON_2 = 'Stacy'  # Bottom half of display

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
    Column C: Person (name of person)
    
    Returns dict with tasks grouped by person
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
        
        # Group tasks by person
        tasks_by_person = {}
        
        for record in records:
            task = record.get('Task', '')
            status = record.get('Status', '').lower()
            person = record.get('Person', '').strip()
            
            if task:  # Only add non-empty tasks
                if person not in tasks_by_person:
                    tasks_by_person[person] = []
                
                tasks_by_person[person].append({
                    'text': task,
                    'completed': status == 'done'
                })
        
        return tasks_by_person
    except Exception as e:
        print(f"Error reading from Google Sheets: {e}")
        return {}

def draw_task_list(draw, tasks, start_y, end_y, person_name, width, fonts, orientation):
    """
    Draw a single person's task list in the given vertical space
    """
    title_font, task_font, small_font = fonts
    
    # Layout settings based on orientation
    if orientation == 'portrait':
        name_size = 22
        line_height = 32
        box_size = 16
    else:
        name_size = 28
        line_height = 36
        box_size = 18
    
    # Load name font
    try:
        name_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', name_size)
    except:
        name_font = ImageFont.load_default()
    
    x_pos = 20
    y_position = start_y
    
    # Draw person's name
    draw.text((x_pos, y_position), f"{person_name}'s List", font=name_font, fill=0)
    y_position += name_size + 8
    
    # Draw separator line
    draw.line((x_pos, y_position, width - 20, y_position), fill=0, width=1)
    y_position += 10
    
    # Calculate max tasks that fit in this section
    available_height = end_y - y_position - 10
    max_tasks = available_height // line_height
    
    if not tasks:
        draw.text((x_pos + 10, y_position), "No tasks", font=task_font, fill=0)
    else:
        for i, task in enumerate(tasks[:max_tasks]):
            task_text = task['text']
            
            # Draw checkbox
            draw.rectangle([x_pos, y_position, x_pos + box_size, y_position + box_size], 
                          outline=0, width=2)
            
            # Draw X if completed
            if task['completed']:
                draw.line([x_pos+3, y_position+3, x_pos+box_size-3, y_position+box_size-3], 
                         fill=0, width=2)
                draw.line([x_pos+3, y_position+box_size-3, x_pos+box_size-3, y_position+3], 
                         fill=0, width=2)
            
            # Draw task text
            text_x = x_pos + box_size + 10
            draw.text((text_x, y_position), task_text, font=task_font, fill=0)
            
            # Draw strikethrough if completed
            if task['completed']:
                bbox = draw.textbbox((text_x, y_position), task_text, font=task_font)
                text_width = bbox[2] - bbox[0]
                strike_y = y_position + (box_size // 2)
                draw.line([text_x, strike_y, text_x + text_width, strike_y], 
                         fill=0, width=2)
            
            y_position += line_height
    
    return len(tasks) if tasks else 0

def create_dual_todo_image(tasks_by_person, width, height, orientation, person1, person2):
    """
    Create an image with two to-do lists (one per person)
    Each person gets equal vertical space
    """
    # Create a new image with white background
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    
    # Font sizes based on orientation
    if orientation == 'portrait':
        title_size = 24
        task_size = 18
        small_size = 12
    else:
        title_size = 30
        task_size = 22
        small_size = 14
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', title_size)
        task_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', task_size)
        small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', small_size)
    except:
        title_font = ImageFont.load_default()
        task_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    fonts = (title_font, task_font, small_font)
    
    # Draw main title
    title = "TO-DO LISTS"
    draw.text((20, 10), title, font=title_font, fill=0)
    
    # Draw timestamp on the right
    timestamp = datetime.now().strftime("%b %d, %I:%M %p")
    ts_bbox = draw.textbbox((0, 0), timestamp, font=small_font)
    ts_width = ts_bbox[2] - ts_bbox[0]
    draw.text((width - ts_width - 20, 15), timestamp, font=small_font, fill=0)
    
    # Draw main title line
    title_line_y = 45
    draw.line((20, title_line_y, width - 20, title_line_y), fill=0, width=2)
    
    # Calculate sections - equal space for each person
    content_start = title_line_y + 10
    content_end = height - 25
    total_content_height = content_end - content_start
    
    # Split into two equal halves
    half_height = total_content_height // 2
    
    person1_start = content_start
    person1_end = content_start + half_height - 5
    
    person2_start = content_start + half_height + 5
    person2_end = content_end
    
    # Draw divider line between the two lists
    divider_y = content_start + half_height
    draw.line((20, divider_y, width - 20, divider_y), fill=0, width=2)
    
    # Get tasks for each person
    person1_tasks = tasks_by_person.get(person1, [])
    person2_tasks = tasks_by_person.get(person2, [])
    
    # Draw each person's list
    count1 = draw_task_list(draw, person1_tasks, person1_start, person1_end, 
                            person1, width, fonts, orientation)
    count2 = draw_task_list(draw, person2_tasks, person2_start, person2_end, 
                            person2, width, fonts, orientation)
    
    # Draw footer
    total_tasks = count1 + count2
    footer_text = f"Total: {total_tasks} tasks ({person1}: {count1}, {person2}: {count2})"
    draw.text((20, height - 20), footer_text, font=small_font, fill=0)
    
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
    
    print(f"Dual list mode: {PERSON_1} (top) and {PERSON_2} (bottom)")
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: {CREDENTIALS_FILE} not found!")
        print("Please follow the setup instructions to create your credentials file.")
        sys.exit(1)
    
    print("Fetching tasks from Google Sheets...")
    tasks_by_person = get_tasks_from_sheet(CREDENTIALS_FILE, SHEET_NAME)
    
    # Count tasks
    person1_count = len(tasks_by_person.get(PERSON_1, []))
    person2_count = len(tasks_by_person.get(PERSON_2, []))
    print(f"Found {person1_count} tasks for {PERSON_1}")
    print(f"Found {person2_count} tasks for {PERSON_2}")
    
    print("Creating image...")
    image = create_dual_todo_image(tasks_by_person, WIDTH, HEIGHT, ORIENTATION, PERSON_1, PERSON_2)
    
    # Rotate image if needed for display orientation
    if ORIENTATION == 'portrait':
        image = image.rotate(90, expand=True)
    
    # Save image for debugging
    image.save('todo_preview.png')
    print("Preview saved as todo_preview.png")
    
    # Display on e-ink
    display_image_on_epd(image)

if __name__ == "__main__":
    main()
