from PySide6.QtCore import QObject, Signal
from pynput import keyboard
import platform
from logger import logger

class HotkeyManager(QObject):
    toggle_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = None
        self._setup_hotkey()

    def _setup_hotkey(self):
        # Define the hotkey based on OS
        system = platform.system()
        if system == 'Darwin':
            # Cmd+Shift+Space on macOS
            self.hotkey_str = '<cmd>+<shift>+<space>'
        else:
            # Ctrl+Shift+Space on Windows/Linux
            self.hotkey_str = '<ctrl>+<shift>+<space>'
            
        logger.info(f"Setting up global hotkey: [bold magenta]{self.hotkey_str}[/bold magenta]")
        if system == 'Darwin':
            logger.warning("[yellow]Note: macOS requires Accessibility permissions for global hotkeys to work![/yellow]")

        def on_activate():
            # Emit the signal to notify the main thread
            logger.info("Global hotkey triggered!")
            self.toggle_requested.emit()

        # GlobalHotkey using pynput
        self.hotkey = keyboard.GlobalHotKeys({
            self.hotkey_str: on_activate
        })
        self.hotkey.start()

    def stop(self):
        if hasattr(self, 'hotkey'):
            self.hotkey.stop()
