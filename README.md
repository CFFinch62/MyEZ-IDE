# EZ IDE

A modern, themeable IDE for the EZ programming language, built with Python and PyQt6.

![EZ IDE Screenshot](../images/EZ_LOGO.jpeg)

## Features

### 📁 File Browser
- Full-featured file/folder navigation
- Create, rename, and delete files and folders
- Folder bookmarks for quick access
- Show/hide hidden files
- Navigation history (back/forward buttons)
- Toggle visibility with `Ctrl+B` or via toolbar

### 📝 Code Editor
- Tabbed interface for multiple open files
- Syntax highlighting for EZ language
- Line numbers with current line highlighting
- Auto-indent and bracket matching
- Word wrap (optional)
- Zoom with `Ctrl+Mouse Wheel` or `Ctrl++`/`Ctrl+-`

### 💻 Integrated Terminal
- Execute commands directly in the IDE
- Command history (up/down arrows)
- Quick EZ file execution with `F5`
- Position the terminal below or to the right of the editor
- Toggle visibility with `` Ctrl+` `` or via toolbar

### 🎨 Theming
- 4 built-in themes: Dark, Light, Monokai, Nord
- Full syntax highlighting colors per theme
- Custom themes via JSON files
- All settings saved to local JSON

## Installation

### Prerequisites
- Python 3.8 or higher
- EZ language installed (for running EZ files)

### Setup

```bash
cd ez_ide

# Make scripts executable
chmod +x setup.sh run.sh

# Run setup (creates venv and installs PyQt6)
./setup.sh
```

## Usage

```bash
# Start the IDE
./run.sh

# Or manually:
source venv/bin/activate
python main.py
```

## Keyboard Shortcuts

### File Operations
| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save All |
| `Ctrl+W` | Close Tab |

### Edit Operations
| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+F` | Find |
| `Ctrl+G` | Go to Line |
| `Ctrl+,` | Settings |

### View & Run
| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Toggle File Browser |
| `` Ctrl+` `` | Toggle Terminal |
| `F5` | Run Current File |
| `Ctrl++` | Zoom In |
| `Ctrl+-` | Zoom Out |
| `Ctrl+0` | Reset Zoom |

## Configuration

Settings are stored in:
- Linux: `~/.config/ez-ide/settings.json`
- macOS: `~/.config/ez-ide/settings.json`  
- Windows: `%APPDATA%\EZ-IDE\settings.json`

### Custom Themes

Create custom themes by placing JSON files in the themes directory:
- Linux/macOS: `~/.config/ez-ide/themes/`
- Windows: `%APPDATA%\EZ-IDE\themes\`

Example theme file structure:
```json
{
  "name": "My Theme",
  "is_dark": true,
  "background": "#1a1a1a",
  "foreground": "#ffffff",
  "accent": "#007acc",
  ...
  "syntax": {
    "keyword": "#c586c0",
    "string": "#ce9178",
    ...
  }
}
```

## Project Structure

```
ez_ide/
├── main.py           # Application entry point
├── setup.sh          # Setup script
├── run.sh            # Run script
├── README.md         # This file
└── app/
    ├── __init__.py
    ├── main_window.py    # Main IDE window
    ├── settings.py       # Settings management
    ├── themes.py         # Theme manager
    ├── syntax.py         # EZ syntax highlighter
    ├── editor.py         # Code editor widgets
    ├── file_browser.py   # File browser widget
    └── terminal.py       # Terminal widget
```

## License

Part of the EZ Language project.  
MIT License - Copyright (c) 2025 Marshall A Burns
