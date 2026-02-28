import sys
import uuid
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QLabel, QPushButton, QSlider, QMenu
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QColor

from db import TodoDAO
from logger import logger
from themes import THEMES, generate_qss

class StrikeLabel(QLabel):
    # Just a marker if needed, but we will use QFrame inside TodoItemWidget instead
    pass

class TodoItemWidget(QWidget):
    def __init__(self, item: QListWidgetItem, todo, main_window):
        super().__init__(main_window.list_widget)
        self.item = item
        self.todo = todo
        self.main_window = main_window
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 10, 12, 10)
        self.layout.setSpacing(12)
        
        # Checkbox
        self.checkbox = QPushButton("✓" if todo['completed'] else "")
        self.checkbox.setFixedSize(24, 24)
        self.checkbox.setCheckable(True)
        self.checkbox.setChecked(todo['completed'])
        self.checkbox.setObjectName("ITEM_CHECKBOX")
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox.clicked.connect(self.on_checkbox_clicked)
        
        # Label
        self.label = QLabel(todo['text'])
        self.label.setWordWrap(True)
        self.label.setObjectName("ITEM_LABEL")
        self.label.setMinimumHeight(24)
        font = self.label.font()
        font.setPointSize(15)
        self.label.setFont(font)
        
        # Strike Line overlay
        from PySide6.QtWidgets import QFrame
        self.strike_line = QFrame(self.label)
        self.strike_line.setFixedHeight(2)
        self.strike_line.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.strike_line.hide()
        
        self.apply_text_style()
        
        # Edit Field (hidden)
        self.edit_field = QLineEdit()
        self.edit_field.setText(todo['text'])
        self.edit_field.setObjectName("ITEM_EDIT")
        font_edit = self.edit_field.font()
        font_edit.setPointSize(15)
        self.edit_field.setFont(font_edit)
        self.edit_field.setMinimumHeight(26)
        self.edit_field.hide()
        self.edit_field.returnPressed.connect(self.finish_edit)
        self.edit_field.editingFinished.connect(self.finish_edit)
        
        # Delete Button
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.setObjectName("ITEM_DELETE_BTN")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.edit_field, stretch=1)
        self.layout.addWidget(self.delete_btn)

    def mouseDoubleClickEvent(self, event):
        self.start_edit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_strike_geometry()

    def _update_strike_geometry(self):
        # We need the rect of the text inside the label, but drawing it simply across the middle works well.
        fm = self.label.fontMetrics()
        text_width = fm.horizontalAdvance(self.label.text())
        strike_w = min(text_width, self.label.width()) + 4
        self.strike_line.setFixedWidth(strike_w)
        y = self.label.height() // 2
        self.strike_line.move(0, y)

    def apply_text_style(self):
        theme_data = THEMES[self.main_window.current_theme]
        
        if self.todo['completed']:
            color = theme_data['text_done']
            self.strike_line.setStyleSheet(f"background-color: {theme_data['strike_color']}; border-radius: 1px;")
            self.strike_line.show()
            self._update_strike_geometry()
        else:
            color = theme_data['text_main']
            self.strike_line.hide()
            
        self.label.setStyleSheet(f"color: {color}; background: transparent; border: none;")

    def on_checkbox_clicked(self):
        self.main_window.toggle_task_by_id(self.todo['id'])

    def on_delete_clicked(self):
        self.main_window.delete_task_by_id(self.todo['id'])

    def start_edit(self, event=None):
        self.label.hide()
        self.edit_field.show()
        self.edit_field.setFocus()
        self.edit_field.selectAll()

    def finish_edit(self):
        if not self.edit_field.isVisible():
            return
        self.edit_field.hide()
        self.label.show()
        new_text = self.edit_field.text().strip()
        
        if not new_text:
            logger.info(f"Task {self.todo['id']} text was empty, deleting.")
            self.main_window.delete_task_by_id(self.todo['id'])
        elif new_text != self.todo['text']:
            logger.info(f"Task updated: [green]'{new_text}'[/green]")
            self.main_window.update_task_text(self.todo['id'], new_text)

class TitleBar(QWidget):
    def __init__(self, theme_callback, opacity_callback, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 8, 0)
        
        self.title_label = QLabel("Todos")
        self.title_label.setObjectName("TITLE")
        
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(40, 100)
        self.opacity_slider.setFixedWidth(60)
        self.opacity_slider.setToolTip("Background Opacity")
        self.opacity_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.opacity_slider.valueChanged.connect(opacity_callback)
        
        self.theme_btn = QPushButton("🎨")
        self.theme_btn.setObjectName("THEME_BTN")
        self.theme_btn.setFixedSize(28, 24)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add a rich dropdown menu for 10 themes
        menu = QMenu(self.theme_btn)
        menu.setStyleSheet("""
            QMenu { background-color: #222; border-radius: 4px; padding: 4px; border: 1px solid #444; }
            QMenu::item { color: #fff; padding: 4px 16px; border-radius: 4px; }
            QMenu::item:selected { background-color: #007aff; }
        """)
        for t_id, t_data in THEMES.items():
            action = menu.addAction(t_data["name"])
            action.triggered.connect(lambda checked=False, tid=t_id: theme_callback(tid))
        self.theme_btn.setMenu(menu)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("CLOSE_BTN")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.window().hide)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.opacity_slider)
        layout.addSpacing(5)
        layout.addWidget(self.theme_btn)
        layout.addWidget(self.close_btn)
        
        # Variables for dragging
        self._is_dragging = False
        self._drag_pos = QPoint()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._is_dragging = False
        event.accept()


class TodoWidget(QWidget):
    def __init__(self, dao: TodoDAO, settings_mgr):
        super().__init__()
        self.dao = dao
        self.settings = settings_mgr
        
        self.current_theme = self.settings.get("theme", "dark")
        self.current_opacity = self.settings.get("opacity", 95)
        
        # Configure the window
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(340, 480)
        self.setObjectName("TODO_MAIN")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget(self)
        self.container.setObjectName("TODO_MAIN")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 5, 10, 15)
        self.container_layout.setSpacing(12)
        
        self.main_layout.addWidget(self.container)
        
        # Title Bar
        self.title_bar = TitleBar(self.change_theme, self.change_opacity, self)
        self.title_bar.opacity_slider.blockSignals(True)
        self.title_bar.opacity_slider.setValue(self.current_opacity)
        self.title_bar.opacity_slider.blockSignals(False)
        self.container_layout.addWidget(self.title_bar)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setObjectName("INPUT")
        self.input_field.setPlaceholderText("What needs to be done? (Press Enter)")
        self.input_field.returnPressed.connect(self.add_task)
        self.container_layout.addWidget(self.input_field)
        
        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setWordWrap(True)
        self.list_widget.installEventFilter(self)
        self.container_layout.addWidget(self.list_widget)
        
        # Empty State Label
        self.empty_label = QLabel("No tasks yet.\\nPress Enter to add your first task.")
        self.empty_label.setObjectName("EMPTY_LABEL")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.empty_label)
        
        self.apply_theme()
        self.load_tasks()

    def change_theme(self, theme_id):
        self.current_theme = theme_id
        self.settings.set("theme", theme_id)
        logger.info(f"Theme switched to: [bold cyan]{self.current_theme}[/bold cyan]")
        self.apply_theme()
        self.load_tasks()

    def change_opacity(self, value):
        self.current_opacity = value
        self.settings.set("opacity", value)
        self.apply_theme()

    def apply_theme(self):
        theme_data = THEMES.get(self.current_theme, THEMES["dark"])
        qss = generate_qss(theme_data, self.current_opacity)
        self.container.setStyleSheet(qss)
        # Update dynamically injected styles in existing items
        self.load_tasks()

    def showEvent(self, event):
        super().showEvent(event)
        self.input_field.setFocus()

    def load_tasks(self):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        todos = self.dao.get_todos()
        
        if not todos:
            self.list_widget.hide()
            self.empty_label.show()
        else:
            self.empty_label.hide()
            self.list_widget.show()
            for todo in todos:
                self.add_item_to_list(todo)
        self.list_widget.blockSignals(False)

    def add_item_to_list(self, todo):
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, todo['id'])
        
        self.list_widget.addItem(item)
        
        custom_widget = TodoItemWidget(item, todo, self)
        # Ensure item knows its height so it doesn't crush the layout into a thin line
        item.setSizeHint(custom_widget.sizeHint())
        self.list_widget.setItemWidget(item, custom_widget)

    def _restore_selection(self, todo_id):
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).data(Qt.ItemDataRole.UserRole) == todo_id:
                self.list_widget.setCurrentRow(i)
                break

    def update_task_text(self, todo_id, new_text):
        self.dao.update_todo(todo_id, text=new_text)
        self.load_tasks()
        self._restore_selection(todo_id)

    def toggle_task_by_id(self, todo_id):
        todos = self.dao.get_todos()
        for t in todos:
            if t['id'] == todo_id:
                new_status = not t['completed']
                self.dao.update_todo(todo_id, completed=new_status)
                self.load_tasks()
                self._restore_selection(todo_id)
                break

    def delete_task_by_id(self, todo_id):
        row = self.list_widget.currentRow()
        logger.info(f"Deleting task {todo_id[:8]}...")
        self.dao.delete_todo(todo_id)
        self.load_tasks()
        
        if self.list_widget.count() > 0:
            new_row = min(row, self.list_widget.count() - 1)
            if new_row >= 0:
                self.list_widget.setCurrentRow(new_row)

    def add_task(self):
        text = self.input_field.text().strip()
        if not text:
            return
            
        todo_id = str(uuid.uuid4())
        created_at = int(time.time())
        logger.info(f"Adding new task: [blue]'{text}'[/blue]")
        self.dao.add_todo(todo_id, text, created_at)
        
        self.input_field.clear()
        self.load_tasks()
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)

    def eventFilter(self, obj, event):
        if obj == self.list_widget and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Space:
                current_item = self.list_widget.currentItem()
                if current_item:
                    todo_id = current_item.data(Qt.ItemDataRole.UserRole)
                    widget = self.list_widget.itemWidget(current_item)
                    if isinstance(widget, TodoItemWidget) and widget.edit_field.isVisible():
                        return False # let the text field handle space
                    self.toggle_task_by_id(todo_id)
                return True
            elif event.key() == Qt.Key.Key_F2:
                current_item = self.list_widget.currentItem()
                if current_item:
                    widget = self.list_widget.itemWidget(current_item)
                    if isinstance(widget, TodoItemWidget):
                        widget.start_edit()
                return True
            elif event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
                current_item = self.list_widget.currentItem()
                if current_item:
                    widget = self.list_widget.itemWidget(current_item)
                    if isinstance(widget, TodoItemWidget) and widget.edit_field.isVisible():
                        return False # logic for textbox
                    else:
                        todo_id = current_item.data(Qt.ItemDataRole.UserRole)
                        self.delete_task_by_id(todo_id)
                        return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            if self.list_widget.isVisible():
                self.list_widget.setFocus()
                if self.list_widget.currentRow() == -1 and self.list_widget.count() > 0:
                    if event.key() == Qt.Key.Key_Down:
                        self.list_widget.setCurrentRow(0)
                    else:
                        self.list_widget.setCurrentRow(self.list_widget.count() - 1)
                else:
                    super().keyPressEvent(event)
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)
