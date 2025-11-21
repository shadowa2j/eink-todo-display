# Google Sheet Template

Copy this format to your Google Sheet:

## Sheet Name: "My To-Do List"

### Row 1 (Headers):
| Task | Status | Person |

### Sample Data:
| Task                          | Status | Person |
|-------------------------------|--------|--------|
| Review quarterly reports      |        | Bryan  |
| Update server documentation   | done   | Bryan  |
| Order new keyboard            |        | Bryan  |
| Schedule dentist appointment  |        | Stacy  |
| Backup important files        | done   | Stacy  |
| Call insurance company        |        | Stacy  |
| Submit expense report         | done   | Bryan  |
| Plan birthday party           |        | Stacy  |
| Test new feature              |        | Bryan  |
| Pick up dry cleaning          |        | Stacy  |

## Instructions:

1. Column A (Task): 
   - Enter your task descriptions
   - Can be any length, but keep under 40 characters for best display

2. Column B (Status):
   - Leave EMPTY for active/incomplete tasks
   - Type "done" (lowercase) for completed tasks
   - Completed tasks will show with strikethrough on display

3. Column C (Person):
   - Enter the person's name exactly as configured in the script
   - Default names are "Bryan" and "Stacy" (case-sensitive!)
   - Tasks without a Person will not appear on display

## Tips:

- Add new tasks at the bottom
- Delete old completed tasks periodically
- Each person gets half the display (~9 tasks each in portrait mode)
- Edit from your phone, computer, or tablet - changes sync automatically
- Updates appear on the e-ink display every hour
- Names are case-sensitive: "Bryan" works, "bryan" does not

## Changing Names:

If you want different names, edit these lines in `todo_display.py`:
```python
PERSON_1 = 'Bryan'  # Top half of display
PERSON_2 = 'Stacy'  # Bottom half of display
```

## Share Settings:

Make sure to share this sheet with your service account email:
- Email looks like: your-service-account@your-project.iam.gserviceaccount.com
- Give "Viewer" permission (read-only is sufficient)
- Find this email in your credentials.json file
