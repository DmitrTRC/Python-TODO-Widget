import sys
import os
import time
from PySide6.QtWidgets import QApplication
from main_window import TodoWidget
from settings import SettingsManager

class MockDAO:
    def get_todos(self):
        return [
            {"id": "1", "text": "Buy groceries", "completed": 1, "created_at": 1},
            {"id": "2", "text": "Finish TodoWidget UI", "completed": 0, "created_at": 2},
            {"id": "3", "text": "Take a coffee break", "completed": 0, "created_at": 3},
        ]
    def update_todo(self, *args, **kwargs): pass
    def add_todo(self, *args, **kwargs): pass
    def delete_todo(self, *args, **kwargs): pass

app = QApplication(sys.argv)
dao = MockDAO()
settings = SettingsManager()
widget = TodoWidget(dao, settings)

if not os.path.exists('docs'):
    os.makedirs('docs')

themes_to_grab = ['dark', 'light', 'synthwave']

widget.show()
# Wait for initial render
for _ in range(10):
    app.processEvents()
    time.sleep(0.05)

for theme in themes_to_grab:
    widget.change_theme(theme)
    # process events and sleep slightly to allow UI to update
    for _ in range(10):
        app.processEvents()
        time.sleep(0.05)
    
    pixmap = widget.grab()
    pixmap.save(f"docs/theme_{theme}.png")
    print(f"Captured docs/theme_{theme}.png")

widget.hide()
