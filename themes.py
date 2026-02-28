def generate_qss(theme: dict, opacity_percent: int) -> str:
    alpha = int(255 * (opacity_percent / 100.0))
    bg_rgba = f"rgba({theme['bg_rgb']}, {alpha})"
    
    return f"""
QWidget#TODO_MAIN {{
    background-color: {bg_rgba};
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 40);
}}
QLabel#TITLE {{
    color: {theme['text_main']};
    font-size: 15px;
    font-weight: 600;
    font-family: Arial, sans-serif;
    padding-left: 5px;
}}
QPushButton#THEME_BTN, QPushButton#CLOSE_BTN {{
    background-color: transparent;
    color: {theme['text_dim']};
    border: none;
    font-size: 14px;
    font-weight: bold;
    border-radius: 12px;
}}
QPushButton#THEME_BTN::menu-indicator {{
    image: none;
}}
QPushButton#THEME_BTN:hover {{
    color: {theme['text_main']};
    background-color: rgba(128, 128, 128, 40);
}}
QPushButton#CLOSE_BTN:hover {{
    color: #ffffff;
    background-color: #ff5f56;
}}
QLineEdit#INPUT {{
    background-color: {theme['input_bg']};
    border: 1px solid rgba(128, 128, 128, 30);
    border-radius: 8px;
    padding: 10px;
    color: {theme['text_main']};
    font-size: 14px;
    font-family: Arial, sans-serif;
}}
QLineEdit#INPUT:focus {{
    border: 1px solid {theme['accent']};
    background-color: {theme['input_focus']};
}}
QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
    font-family: Arial, sans-serif;
    font-size: 15px;
}}
QListWidget::item {{
    background-color: transparent;
    border-radius: 8px;
    margin-bottom: 2px;
    padding: 0px;
}}
QListWidget::item:hover {{
    background-color: {theme['item_hover']};
}}
QListWidget::item:selected {{
    background-color: {theme['item_selected']};
    border: 1px solid {theme['accent']};
}}
QLabel#EMPTY_LABEL {{
    color: {theme['text_dim']};
    font-size: 15px;
    font-family: Arial, sans-serif;
    font-style: italic;
}}
QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 6px;
    margin: 0px 0px 0px 0px;
}}
QScrollBar::handle:vertical {{
    background: {theme['scrollbar']};
    min-height: 20px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical:hover {{
    background: {theme['text_dim']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}
QPushButton#ITEM_CHECKBOX {{
    background-color: transparent;
    border: 2px solid {theme['text_dim']};
    border-radius: 6px;
    color: {theme['accent']};
    font-weight: bold;
    font-size: 14px;
}}
QPushButton#ITEM_CHECKBOX:checked {{
    border: 2px solid {theme['accent']};
    background-color: {theme['item_selected']};
}}
QPushButton#ITEM_DELETE_BTN {{
    background-color: transparent;
    border: none;
    color: #ff3b30;
    font-weight: bold;
    font-size: 16px;
    opacity: 0.5;
}}
QPushButton#ITEM_DELETE_BTN:hover {{
    background-color: rgba(255, 59, 48, 40);
    border-radius: 6px;
}}
QLineEdit#ITEM_EDIT {{
    background-color: {theme['input_focus']};
    border: 1px solid {theme['accent']};
    border-radius: 4px;
    color: {theme['text_main']};
    padding: 5px;
    font-size: 14px;
}}
QSlider::groove:horizontal {{
    border: 1px solid rgba(128, 128, 128, 50);
    height: 4px;
    background: {theme['input_bg']};
    margin: 2px 0;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {theme['accent']};
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px;
}}
"""

THEMES = {
    "dark": {
        "name": "Dark",
        "bg_rgb": "30, 30, 30",
        "text_main": "#ffffff",
        "text_dim": "#aaaaaa",
        "text_done": "#777777",
        "accent": "#0a84ff",
        "input_bg": "rgba(0, 0, 0, 80)",
        "input_focus": "rgba(0, 0, 0, 150)",
        "item_hover": "rgba(255, 255, 255, 10)",
        "item_selected": "rgba(10, 132, 255, 40)",
        "scrollbar": "rgba(255, 255, 255, 30)",
        "strike_color": "#ff3b30", # vibrant red
    },
    "light": {
        "name": "Light",
        "bg_rgb": "250, 250, 250",
        "text_main": "#111111",
        "text_dim": "#777777",
        "text_done": "#aaaaaa",
        "accent": "#007aff",
        "input_bg": "rgba(0, 0, 0, 10)",
        "input_focus": "rgba(255, 255, 255, 255)",
        "item_hover": "rgba(0, 0, 0, 10)",
        "item_selected": "rgba(0, 122, 255, 30)",
        "scrollbar": "rgba(0, 0, 0, 20)",
        "strike_color": "#ff2d55", # vibrant pink/red
    },
    "dracula": {
        "name": "Dracula",
        "bg_rgb": "40, 42, 54",
        "text_main": "#f8f8f2",
        "text_dim": "#6272a4",
        "text_done": "#44475a",
        "accent": "#bd93f9",
        "input_bg": "rgba(0, 0, 0, 40)",
        "input_focus": "rgba(0, 0, 0, 80)",
        "item_hover": "rgba(255, 255, 255, 15)",
        "item_selected": "rgba(189, 147, 249, 40)",
        "scrollbar": "rgba(255, 255, 255, 20)",
        "strike_color": "#ff79c6", # vibrant pink
    },
    "nord": {
        "name": "Nord",
        "bg_rgb": "46, 52, 64",
        "text_main": "#eceff4",
        "text_dim": "#d8dee9",
        "text_done": "#4c566a",
        "accent": "#88c0d0",
        "input_bg": "rgba(59, 66, 82, 180)",
        "input_focus": "rgba(67, 76, 94, 255)",
        "item_hover": "rgba(255, 255, 255, 10)",
        "item_selected": "rgba(136, 192, 208, 40)",
        "scrollbar": "rgba(255, 255, 255, 25)",
        "strike_color": "#bf616a", # nord red
    },
    "gruvbox": {
        "name": "Gruvbox",
        "bg_rgb": "40, 40, 40",
        "text_main": "#ebdbb2",
        "text_dim": "#a89984",
        "text_done": "#7c6f64",
        "accent": "#fabd2f",
        "input_bg": "rgba(29, 32, 33, 100)",
        "input_focus": "rgba(50, 48, 47, 200)",
        "item_hover": "rgba(255, 255, 255, 12)",
        "item_selected": "rgba(250, 189, 47, 40)",
        "scrollbar": "rgba(255, 255, 255, 25)",
        "strike_color": "#fb4934", # red
    },
    "monokai": {
        "name": "Monokai",
        "bg_rgb": "39, 40, 34",
        "text_main": "#f8f8f2",
        "text_dim": "#75715e",
        "text_done": "#49483e",
        "accent": "#a6e22e",
        "input_bg": "rgba(0, 0, 0, 60)",
        "input_focus": "rgba(0, 0, 0, 120)",
        "item_hover": "rgba(255, 255, 255, 15)",
        "item_selected": "rgba(166, 226, 46, 40)",
        "scrollbar": "rgba(255, 255, 255, 20)",
        "strike_color": "#f92672", # pink
    },
    "synthwave": {
        "name": "Synthwave",
        "bg_rgb": "38, 35, 53",
        "text_main": "#ffffff",
        "text_dim": "#848bbd",
        "text_done": "#495495",
        "accent": "#ff7edb",
        "input_bg": "rgba(20, 15, 30, 120)",
        "input_focus": "rgba(20, 15, 30, 200)",
        "item_hover": "rgba(255, 255, 255, 15)",
        "item_selected": "rgba(255, 126, 219, 40)",
        "scrollbar": "rgba(255, 255, 255, 20)",
        "strike_color": "#fe4450", # bright red
    },
    "catppuccin": {
        "name": "Catppuccin",
        "bg_rgb": "30, 30, 46",
        "text_main": "#cdd6f4",
        "text_dim": "#bac2de",
        "text_done": "#585b70",
        "accent": "#cba6f7",
        "input_bg": "rgba(24, 24, 37, 180)",
        "input_focus": "rgba(17, 17, 27, 255)",
        "item_hover": "rgba(255, 255, 255, 12)",
        "item_selected": "rgba(203, 166, 247, 40)",
        "scrollbar": "rgba(255, 255, 255, 20)",
        "strike_color": "#f38ba8", # peach/red
    },
    "solarized_dark": {
        "name": "Solarized Dark",
        "bg_rgb": "0, 43, 54",
        "text_main": "#839496",
        "text_dim": "#586e75",
        "text_done": "#073642",
        "accent": "#2aa198",
        "input_bg": "rgba(0, 0, 0, 50)",
        "input_focus": "rgba(0, 0, 0, 100)",
        "item_hover": "rgba(255, 255, 255, 10)",
        "item_selected": "rgba(42, 161, 152, 40)",
        "scrollbar": "rgba(255, 255, 255, 20)",
        "strike_color": "#cb4b16", # orange
    },
    "hacker": {
        "name": "Hacker",
        "bg_rgb": "10, 10, 10",
        "text_main": "#00ff00",
        "text_dim": "#008800",
        "text_done": "#003300",
        "accent": "#00ff00",
        "input_bg": "rgba(0, 20, 0, 150)",
        "input_focus": "rgba(0, 40, 0, 255)",
        "item_hover": "rgba(0, 255, 0, 15)",
        "item_selected": "rgba(0, 255, 0, 30)",
        "scrollbar": "rgba(0, 255, 0, 40)",
        "strike_color": "#ff0000", # intense red
    }
}
