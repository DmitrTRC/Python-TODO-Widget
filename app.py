import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
from PySide6.QtCore import Qt
from db import TodoDAO
from main_window import TodoWidget
from hotkey_manager import HotkeyManager
from logger import logger

def create_tray_icon():
    # Helper to generate a procedural icon for the tray
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    pen = QPen(Qt.GlobalColor.white)
    pen.setWidth(3)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.drawRect(5, 5, 22, 22)
    painter.drawLine(9, 16, 14, 21)
    painter.drawLine(14, 21, 23, 10)
    painter.end()
    return QIcon(pixmap)

def main():
    logger.info("Starting TodoWidget...")
    app = QApplication(sys.argv)
    app.setApplicationName("TodoWidget")
    
    # Do not quit the application when the main window is closed (hidden)
    app.setQuitOnLastWindowClosed(False)

    dao = TodoDAO()
    widget = TodoWidget(dao)
    hotkey_manager = HotkeyManager()
    
    def toggle_widget():
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()
            # On macOS, sometimes to steal focus back as a background tool, we need raise_ and activateWindow.
            widget.raise_()
            widget.activateWindow()
            # Also focus the input field as a convenience
            widget.input_field.setFocus()
            
    hotkey_manager.toggle_requested.connect(toggle_widget)
    
    # Setup Tray Icon
    # macOS Note: QSystemTrayIcon works well. No app icon will appear in the dock due to window flags
    # and LSUIElement (which should be set in Info.plist for Pyinstaller app bundle).
    tray_icon = QSystemTrayIcon(create_tray_icon(), app)
    tray_menu = QMenu()
    
    toggle_action = tray_menu.addAction("Toggle Widget (Cmd+Shift+Space)")
    toggle_action.triggered.connect(toggle_widget)
    
    quit_action = tray_menu.addAction("Quit")
    quit_action.triggered.connect(app.quit)
    
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Show it initially so the user knows it's started
    logger.info("Application started successfully. Tray icon created.")
    widget.show()
    widget.raise_()
    widget.activateWindow()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
