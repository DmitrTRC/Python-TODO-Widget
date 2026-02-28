<div align="center">

# 📝 TodoWidget

**A minimalistic, frameless, keyboard-driven desktop todo widget built with Python and PySide6.**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg?style=for-the-badge&logo=qt)](https://pypi.org/project/PySide6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/dmitrymorozov/TodoWidget/ci.yml?style=for-the-badge&logo=github)](https://github.com/dmitrymorozov/TodoWidget/actions)

<img src="https://via.placeholder.com/800x400/1E1E1E/FFFFFF?text=TodoWidget+Screenshot+Here" alt="TodoWidget Showcase" width="600" style="border-radius: 12px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);"/>

</div>

## ✨ Features

- **Frameless & Floating:** Acts like a native widget on your desktop, stripped of all unnecessary window borders.
- **Always on Top:** Never lose track of your tasks behind other windows.
- **Global Hotkey:** Summon or hide your tasks instantly with `Cmd+Shift+Space` (macOS) or `Ctrl+Shift+Space` (Windows/Linux) from anywhere.
- **Keyboard-Driven:** 
  - `Enter` to add tasks.
  - `Space` to mark as completed.
  - `↑` / `↓` to navigate.
  - `F2` to edit.
  - `Delete` to remove.
  - `Esc` to hide.
- **10 Beautiful Themes:** From pure Dark/Light to Dracula, Nord, Synthwave, Catppuccin and more.
- **Adjustable Opacity:** Slide the opacity from 40% to 100% to create the perfect glass effect for your wallpaper.
- **Local SQLite Storage:** Fast, private, offline storage.

## 🚀 Quick Start

### 1. Requirements

Ensure you have Python 3.11+ installed. It is recommended to use `uv` for fast dependency management.

```bash
git clone https://github.com/dmitrymorozov/TodoWidget.git
cd TodoWidget
```

### 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv 
uv pip install -r requirements.txt
```

*(Note for macOS users: Accessibility permissions must be granted to the terminal or app running the script in order for the global hotkey to intercept keystrokes!)*

### 3. Run

```bash
uv run python app.py
```

The widget will appear, and an icon will be placed in your system tray!

## 🛠 Shortcuts

| Action | Shortcut |
|---|---|
| Toggle Widget Visibility | `Cmd+Shift+Space` (mac) / `Ctrl+Shift+Space` (win) |
| Add new task | Type in input -> `Enter` |
| Navigate List | `Up Arrow`, `Down Arrow` |
| Toggle Completed | `Space` |
| Delete Task | `Backspace` or `Delete` |
| Edit Task | `Double Click` or `F2` |
| Hide Widget | `Esc` |

## 🎨 Themes Available

- **Dark** (Default)
- **Light**
- **Dracula**
- **Nord**
- **Gruvbox**
- **Monokai**
- **Synthwave**
- **Catppuccin**
- **Solarized Dark**
- **Hacker**

Click the 🎨 icon in the widget to select your theme and use the slider next to it to adjust background transparency!

## ⚙️ How it Works

- **PySide6**: The official Python binding for the Qt toolkit provides the robust desktop UI backend.
- **pynput**: Listens for system-wide shortcut strokes asynchronously.
- **SQLite3**: Python's built-in blazing fast SQL database persists tasks.
- **Rich**: Provides beautiful terminal logging out of the box.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
