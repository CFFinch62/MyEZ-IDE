"""
Theme Manager for EZ IDE
Handles loading and applying themes
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

from app.settings import SettingsManager, get_config_dir


@dataclass
class SyntaxColors:
    """Syntax highlighting colors for code editor"""
    keyword: str = "#c678dd"
    builtin: str = "#e5c07b"
    type: str = "#e5c07b"
    string: str = "#98c379"
    number: str = "#d19a66"
    comment: str = "#5c6370"
    operator: str = "#56b6c2"
    function: str = "#61afef"
    variable: str = "#e06c75"
    constant: str = "#d19a66"
    identifier: str = "#abb2bf"


@dataclass  
class Theme:
    """Complete theme definition"""
    name: str
    is_dark: bool
    
    # Main colors
    background: str
    foreground: str
    accent: str
    accent_hover: str
    
    # Panel colors
    panel_background: str
    panel_border: str
    
    # Editor colors
    editor_background: str
    editor_foreground: str
    editor_line_highlight: str
    editor_selection: str
    editor_gutter_bg: str
    editor_gutter_fg: str
    
    # Tab colors
    tab_background: str
    tab_active_background: str
    tab_hover_background: str
    tab_border: str
    
    # File browser colors
    browser_background: str
    browser_item_hover: str
    browser_item_selected: str
    
    # Terminal colors
    terminal_background: str
    terminal_foreground: str
    
    # Scrollbar
    scrollbar_background: str
    scrollbar_handle: str
    scrollbar_handle_hover: str
    
    # Button colors
    button_background: str
    button_foreground: str
    button_hover: str
    button_pressed: str
    
    # Input colors
    input_background: str
    input_border: str
    input_focus_border: str
    
    # Status colors
    success: str
    warning: str
    error: str
    info: str
    
    # Syntax highlighting
    syntax: SyntaxColors = None
    
    def __post_init__(self):
        if self.syntax is None:
            self.syntax = SyntaxColors()


# Built-in themes
DARK_THEME = Theme(
    name="Dark",
    is_dark=True,
    background="#1e1e2e",
    foreground="#cdd6f4",
    accent="#89b4fa",
    accent_hover="#74c7ec",
    panel_background="#181825",
    panel_border="#313244",
    editor_background="#1e1e2e",
    editor_foreground="#cdd6f4",
    editor_line_highlight="#2a2a3c",
    editor_selection="#44475a",
    editor_gutter_bg="#181825",
    editor_gutter_fg="#6c7086",
    tab_background="#181825",
    tab_active_background="#1e1e2e",
    tab_hover_background="#313244",
    tab_border="#313244",
    browser_background="#181825",
    browser_item_hover="#313244",
    browser_item_selected="#45475a",
    terminal_background="#11111b",
    terminal_foreground="#cdd6f4",
    scrollbar_background="#181825",
    scrollbar_handle="#45475a",
    scrollbar_handle_hover="#585b70",
    button_background="#45475a",
    button_foreground="#cdd6f4",
    button_hover="#585b70",
    button_pressed="#313244",
    input_background="#313244",
    input_border="#45475a",
    input_focus_border="#89b4fa",
    success="#a6e3a1",
    warning="#f9e2af",
    error="#f38ba8",
    info="#89b4fa",
    syntax=SyntaxColors(
        keyword="#cba6f7",
        builtin="#f9e2af",
        type="#f9e2af",
        string="#a6e3a1",
        number="#fab387",
        comment="#6c7086",
        operator="#94e2d5",
        function="#89b4fa",
        variable="#f38ba8",
        constant="#fab387",
        identifier="#cdd6f4"
    )
)

LIGHT_THEME = Theme(
    name="Light",
    is_dark=False,
    background="#eff1f5",
    foreground="#4c4f69",
    accent="#1e66f5",
    accent_hover="#2a7afd",
    panel_background="#e6e9ef",
    panel_border="#bcc0cc",
    editor_background="#eff1f5",
    editor_foreground="#4c4f69",
    editor_line_highlight="#dce0e8",
    editor_selection="#acb0be",
    editor_gutter_bg="#e6e9ef",
    editor_gutter_fg="#8c8fa1",
    tab_background="#e6e9ef",
    tab_active_background="#eff1f5",
    tab_hover_background="#ccd0da",
    tab_border="#bcc0cc",
    browser_background="#e6e9ef",
    browser_item_hover="#ccd0da",
    browser_item_selected="#bcc0cc",
    terminal_background="#dce0e8",
    terminal_foreground="#4c4f69",
    scrollbar_background="#e6e9ef",
    scrollbar_handle="#bcc0cc",
    scrollbar_handle_hover="#acb0be",
    button_background="#bcc0cc",
    button_foreground="#4c4f69",
    button_hover="#acb0be",
    button_pressed="#ccd0da",
    input_background="#ccd0da",
    input_border="#bcc0cc",
    input_focus_border="#1e66f5",
    success="#40a02b",
    warning="#df8e1d",
    error="#d20f39",
    info="#1e66f5",
    syntax=SyntaxColors(
        keyword="#8839ef",
        builtin="#df8e1d",
        type="#df8e1d",
        string="#40a02b",
        number="#fe640b",
        comment="#8c8fa1",
        operator="#179299",
        function="#1e66f5",
        variable="#d20f39",
        constant="#fe640b",
        identifier="#4c4f69"
    )
)

MONOKAI_THEME = Theme(
    name="Monokai",
    is_dark=True,
    background="#272822",
    foreground="#f8f8f2",
    accent="#a6e22e",
    accent_hover="#b8f340",
    panel_background="#1e1f1c",
    panel_border="#3e3d32",
    editor_background="#272822",
    editor_foreground="#f8f8f2",
    editor_line_highlight="#3e3d32",
    editor_selection="#49483e",
    editor_gutter_bg="#1e1f1c",
    editor_gutter_fg="#75715e",
    tab_background="#1e1f1c",
    tab_active_background="#272822",
    tab_hover_background="#3e3d32",
    tab_border="#3e3d32",
    browser_background="#1e1f1c",
    browser_item_hover="#3e3d32",
    browser_item_selected="#49483e",
    terminal_background="#1a1b17",
    terminal_foreground="#f8f8f2",
    scrollbar_background="#1e1f1c",
    scrollbar_handle="#49483e",
    scrollbar_handle_hover="#5c5b4f",
    button_background="#49483e",
    button_foreground="#f8f8f2",
    button_hover="#5c5b4f",
    button_pressed="#3e3d32",
    input_background="#3e3d32",
    input_border="#49483e",
    input_focus_border="#a6e22e",
    success="#a6e22e",
    warning="#e6db74",
    error="#f92672",
    info="#66d9ef",
    syntax=SyntaxColors(
        keyword="#f92672",
        builtin="#66d9ef",
        type="#66d9ef",
        string="#e6db74",
        number="#ae81ff",
        comment="#75715e",
        operator="#f92672",
        function="#a6e22e",
        variable="#fd971f",
        constant="#ae81ff",
        identifier="#f8f8f2"
    )
)

NORD_THEME = Theme(
    name="Nord",
    is_dark=True,
    background="#2e3440",
    foreground="#eceff4",
    accent="#88c0d0",
    accent_hover="#8fbcbb",
    panel_background="#2e3440",
    panel_border="#3b4252",
    editor_background="#2e3440",
    editor_foreground="#eceff4",
    editor_line_highlight="#3b4252",
    editor_selection="#434c5e",
    editor_gutter_bg="#2e3440",
    editor_gutter_fg="#616e88",
    tab_background="#2e3440",
    tab_active_background="#3b4252",
    tab_hover_background="#434c5e",
    tab_border="#3b4252",
    browser_background="#2e3440",
    browser_item_hover="#3b4252",
    browser_item_selected="#434c5e",
    terminal_background="#242933",
    terminal_foreground="#eceff4",
    scrollbar_background="#2e3440",
    scrollbar_handle="#434c5e",
    scrollbar_handle_hover="#4c566a",
    button_background="#434c5e",
    button_foreground="#eceff4",
    button_hover="#4c566a",
    button_pressed="#3b4252",
    input_background="#3b4252",
    input_border="#434c5e",
    input_focus_border="#88c0d0",
    success="#a3be8c",
    warning="#ebcb8b",
    error="#bf616a",
    info="#88c0d0",
    syntax=SyntaxColors(
        keyword="#81a1c1",
        builtin="#88c0d0",
        type="#8fbcbb",
        string="#a3be8c",
        number="#b48ead",
        comment="#616e88",
        operator="#81a1c1",
        function="#88c0d0",
        variable="#d08770",
        constant="#b48ead",
        identifier="#eceff4"
    )
)

# Dracula Theme
DRACULA_THEME = Theme(
    name="Dracula",
    is_dark=True,
    background="#282a36",
    foreground="#f8f8f2",
    accent="#bd93f9",
    accent_hover="#ff79c6",
    panel_background="#21222c",
    panel_border="#44475a",
    editor_background="#282a36",
    editor_foreground="#f8f8f2",
    editor_line_highlight="#44475a",
    editor_selection="#44475a",
    editor_gutter_bg="#21222c",
    editor_gutter_fg="#6272a4",
    tab_background="#21222c",
    tab_active_background="#282a36",
    tab_hover_background="#44475a",
    tab_border="#44475a",
    browser_background="#21222c",
    browser_item_hover="#44475a",
    browser_item_selected="#6272a4",
    terminal_background="#1e1f29",
    terminal_foreground="#f8f8f2",
    scrollbar_background="#21222c",
    scrollbar_handle="#44475a",
    scrollbar_handle_hover="#6272a4",
    button_background="#44475a",
    button_foreground="#f8f8f2",
    button_hover="#6272a4",
    button_pressed="#21222c",
    input_background="#44475a",
    input_border="#6272a4",
    input_focus_border="#bd93f9",
    success="#50fa7b",
    warning="#f1fa8c",
    error="#ff5555",
    info="#8be9fd",
    syntax=SyntaxColors(
        keyword="#ff79c6",
        builtin="#8be9fd",
        type="#8be9fd",
        string="#f1fa8c",
        number="#bd93f9",
        comment="#6272a4",
        operator="#ff79c6",
        function="#50fa7b",
        variable="#ffb86c",
        constant="#bd93f9",
        identifier="#f8f8f2"
    )
)

# One Dark Theme
ONE_DARK_THEME = Theme(
    name="One Dark",
    is_dark=True,
    background="#282c34",
    foreground="#abb2bf",
    accent="#61afef",
    accent_hover="#528bff",
    panel_background="#21252b",
    panel_border="#3e4451",
    editor_background="#282c34",
    editor_foreground="#abb2bf",
    editor_line_highlight="#2c313c",
    editor_selection="#3e4451",
    editor_gutter_bg="#21252b",
    editor_gutter_fg="#636d83",
    tab_background="#21252b",
    tab_active_background="#282c34",
    tab_hover_background="#2c313c",
    tab_border="#3e4451",
    browser_background="#21252b",
    browser_item_hover="#2c313c",
    browser_item_selected="#3e4451",
    terminal_background="#1e2127",
    terminal_foreground="#abb2bf",
    scrollbar_background="#21252b",
    scrollbar_handle="#3e4451",
    scrollbar_handle_hover="#4b5263",
    button_background="#3e4451",
    button_foreground="#abb2bf",
    button_hover="#4b5263",
    button_pressed="#2c313c",
    input_background="#2c313c",
    input_border="#3e4451",
    input_focus_border="#61afef",
    success="#98c379",
    warning="#e5c07b",
    error="#e06c75",
    info="#61afef",
    syntax=SyntaxColors(
        keyword="#c678dd",
        builtin="#e5c07b",
        type="#e5c07b",
        string="#98c379",
        number="#d19a66",
        comment="#5c6370",
        operator="#56b6c2",
        function="#61afef",
        variable="#e06c75",
        constant="#d19a66",
        identifier="#abb2bf"
    )
)

# Gruvbox Dark Theme
GRUVBOX_DARK_THEME = Theme(
    name="Gruvbox Dark",
    is_dark=True,
    background="#282828",
    foreground="#ebdbb2",
    accent="#83a598",
    accent_hover="#8ec07c",
    panel_background="#1d2021",
    panel_border="#3c3836",
    editor_background="#282828",
    editor_foreground="#ebdbb2",
    editor_line_highlight="#3c3836",
    editor_selection="#504945",
    editor_gutter_bg="#1d2021",
    editor_gutter_fg="#928374",
    tab_background="#1d2021",
    tab_active_background="#282828",
    tab_hover_background="#3c3836",
    tab_border="#3c3836",
    browser_background="#1d2021",
    browser_item_hover="#3c3836",
    browser_item_selected="#504945",
    terminal_background="#1d2021",
    terminal_foreground="#ebdbb2",
    scrollbar_background="#1d2021",
    scrollbar_handle="#504945",
    scrollbar_handle_hover="#665c54",
    button_background="#504945",
    button_foreground="#ebdbb2",
    button_hover="#665c54",
    button_pressed="#3c3836",
    input_background="#3c3836",
    input_border="#504945",
    input_focus_border="#83a598",
    success="#b8bb26",
    warning="#fabd2f",
    error="#fb4934",
    info="#83a598",
    syntax=SyntaxColors(
        keyword="#fb4934",
        builtin="#fabd2f",
        type="#fabd2f",
        string="#b8bb26",
        number="#d3869b",
        comment="#928374",
        operator="#8ec07c",
        function="#83a598",
        variable="#fe8019",
        constant="#d3869b",
        identifier="#ebdbb2"
    )
)

# Tokyo Night Theme
TOKYO_NIGHT_THEME = Theme(
    name="Tokyo Night",
    is_dark=True,
    background="#1a1b26",
    foreground="#a9b1d6",
    accent="#7aa2f7",
    accent_hover="#7dcfff",
    panel_background="#16161e",
    panel_border="#292e42",
    editor_background="#1a1b26",
    editor_foreground="#a9b1d6",
    editor_line_highlight="#292e42",
    editor_selection="#33467c",
    editor_gutter_bg="#16161e",
    editor_gutter_fg="#565f89",
    tab_background="#16161e",
    tab_active_background="#1a1b26",
    tab_hover_background="#292e42",
    tab_border="#292e42",
    browser_background="#16161e",
    browser_item_hover="#292e42",
    browser_item_selected="#33467c",
    terminal_background="#13131a",
    terminal_foreground="#a9b1d6",
    scrollbar_background="#16161e",
    scrollbar_handle="#292e42",
    scrollbar_handle_hover="#3b4261",
    button_background="#292e42",
    button_foreground="#a9b1d6",
    button_hover="#3b4261",
    button_pressed="#1f2335",
    input_background="#1f2335",
    input_border="#292e42",
    input_focus_border="#7aa2f7",
    success="#9ece6a",
    warning="#e0af68",
    error="#f7768e",
    info="#7aa2f7",
    syntax=SyntaxColors(
        keyword="#bb9af7",
        builtin="#7dcfff",
        type="#2ac3de",
        string="#9ece6a",
        number="#ff9e64",
        comment="#565f89",
        operator="#89ddff",
        function="#7aa2f7",
        variable="#f7768e",
        constant="#ff9e64",
        identifier="#a9b1d6"
    )
)

# Solarized Light Theme
SOLARIZED_LIGHT_THEME = Theme(
    name="Solarized Light",
    is_dark=False,
    background="#fdf6e3",
    foreground="#657b83",
    accent="#268bd2",
    accent_hover="#2aa198",
    panel_background="#eee8d5",
    panel_border="#93a1a1",
    editor_background="#fdf6e3",
    editor_foreground="#657b83",
    editor_line_highlight="#eee8d5",
    editor_selection="#93a1a1",
    editor_gutter_bg="#eee8d5",
    editor_gutter_fg="#93a1a1",
    tab_background="#eee8d5",
    tab_active_background="#fdf6e3",
    tab_hover_background="#ddd6c1",
    tab_border="#93a1a1",
    browser_background="#eee8d5",
    browser_item_hover="#ddd6c1",
    browser_item_selected="#93a1a1",
    terminal_background="#eee8d5",
    terminal_foreground="#657b83",
    scrollbar_background="#eee8d5",
    scrollbar_handle="#93a1a1",
    scrollbar_handle_hover="#839496",
    button_background="#93a1a1",
    button_foreground="#fdf6e3",
    button_hover="#839496",
    button_pressed="#eee8d5",
    input_background="#fdf6e3",
    input_border="#93a1a1",
    input_focus_border="#268bd2",
    success="#859900",
    warning="#b58900",
    error="#dc322f",
    info="#268bd2",
    syntax=SyntaxColors(
        keyword="#859900",
        builtin="#2aa198",
        type="#b58900",
        string="#2aa198",
        number="#d33682",
        comment="#93a1a1",
        operator="#657b83",
        function="#268bd2",
        variable="#cb4b16",
        constant="#d33682",
        identifier="#657b83"
    )
)

# GitHub Light Theme
GITHUB_LIGHT_THEME = Theme(
    name="GitHub Light",
    is_dark=False,
    background="#ffffff",
    foreground="#24292f",
    accent="#0969da",
    accent_hover="#0550ae",
    panel_background="#f6f8fa",
    panel_border="#d0d7de",
    editor_background="#ffffff",
    editor_foreground="#24292f",
    editor_line_highlight="#f6f8fa",
    editor_selection="#add6ff",
    editor_gutter_bg="#f6f8fa",
    editor_gutter_fg="#8c959f",
    tab_background="#f6f8fa",
    tab_active_background="#ffffff",
    tab_hover_background="#eaeef2",
    tab_border="#d0d7de",
    browser_background="#f6f8fa",
    browser_item_hover="#eaeef2",
    browser_item_selected="#ddf4ff",
    terminal_background="#f6f8fa",
    terminal_foreground="#24292f",
    scrollbar_background="#f6f8fa",
    scrollbar_handle="#d0d7de",
    scrollbar_handle_hover="#afb8c1",
    button_background="#f3f4f6",
    button_foreground="#24292f",
    button_hover="#eaeef2",
    button_pressed="#d0d7de",
    input_background="#ffffff",
    input_border="#d0d7de",
    input_focus_border="#0969da",
    success="#1a7f37",
    warning="#9a6700",
    error="#cf222e",
    info="#0969da",
    syntax=SyntaxColors(
        keyword="#cf222e",
        builtin="#8250df",
        type="#953800",
        string="#0a3069",
        number="#0550ae",
        comment="#6e7781",
        operator="#24292f",
        function="#8250df",
        variable="#953800",
        constant="#0550ae",
        identifier="#24292f"
    )
)

# Gruvbox Light Theme
GRUVBOX_LIGHT_THEME = Theme(
    name="Gruvbox Light",
    is_dark=False,
    background="#fbf1c7",
    foreground="#3c3836",
    accent="#458588",
    accent_hover="#689d6a",
    panel_background="#f2e5bc",
    panel_border="#d5c4a1",
    editor_background="#fbf1c7",
    editor_foreground="#3c3836",
    editor_line_highlight="#f2e5bc",
    editor_selection="#d5c4a1",
    editor_gutter_bg="#f2e5bc",
    editor_gutter_fg="#928374",
    tab_background="#f2e5bc",
    tab_active_background="#fbf1c7",
    tab_hover_background="#ebdbb2",
    tab_border="#d5c4a1",
    browser_background="#f2e5bc",
    browser_item_hover="#ebdbb2",
    browser_item_selected="#d5c4a1",
    terminal_background="#f2e5bc",
    terminal_foreground="#3c3836",
    scrollbar_background="#f2e5bc",
    scrollbar_handle="#d5c4a1",
    scrollbar_handle_hover="#bdae93",
    button_background="#d5c4a1",
    button_foreground="#3c3836",
    button_hover="#bdae93",
    button_pressed="#ebdbb2",
    input_background="#fbf1c7",
    input_border="#d5c4a1",
    input_focus_border="#458588",
    success="#79740e",
    warning="#b57614",
    error="#9d0006",
    info="#458588",
    syntax=SyntaxColors(
        keyword="#9d0006",
        builtin="#b57614",
        type="#b57614",
        string="#79740e",
        number="#8f3f71",
        comment="#928374",
        operator="#427b58",
        function="#458588",
        variable="#af3a03",
        constant="#8f3f71",
        identifier="#3c3836"
    )
)

# One Light Theme
ONE_LIGHT_THEME = Theme(
    name="One Light",
    is_dark=False,
    background="#fafafa",
    foreground="#383a42",
    accent="#4078f2",
    accent_hover="#526fff",
    panel_background="#f0f0f0",
    panel_border="#d4d4d4",
    editor_background="#fafafa",
    editor_foreground="#383a42",
    editor_line_highlight="#f0f0f0",
    editor_selection="#bfceff",
    editor_gutter_bg="#f0f0f0",
    editor_gutter_fg="#9d9d9f",
    tab_background="#f0f0f0",
    tab_active_background="#fafafa",
    tab_hover_background="#e5e5e6",
    tab_border="#d4d4d4",
    browser_background="#f0f0f0",
    browser_item_hover="#e5e5e6",
    browser_item_selected="#bfceff",
    terminal_background="#f0f0f0",
    terminal_foreground="#383a42",
    scrollbar_background="#f0f0f0",
    scrollbar_handle="#d4d4d4",
    scrollbar_handle_hover="#b4b4b4",
    button_background="#d4d4d4",
    button_foreground="#383a42",
    button_hover="#c4c4c4",
    button_pressed="#e5e5e6",
    input_background="#ffffff",
    input_border="#d4d4d4",
    input_focus_border="#4078f2",
    success="#50a14f",
    warning="#c18401",
    error="#e45649",
    info="#4078f2",
    syntax=SyntaxColors(
        keyword="#a626a4",
        builtin="#c18401",
        type="#c18401",
        string="#50a14f",
        number="#986801",
        comment="#a0a1a7",
        operator="#0184bc",
        function="#4078f2",
        variable="#e45649",
        constant="#986801",
        identifier="#383a42"
    )
)

BUILTIN_THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "monokai": MONOKAI_THEME,
    "nord": NORD_THEME,
    "dracula": DRACULA_THEME,
    "one dark": ONE_DARK_THEME,
    "gruvbox dark": GRUVBOX_DARK_THEME,
    "tokyo night": TOKYO_NIGHT_THEME,
    "solarized light": SOLARIZED_LIGHT_THEME,
    "github light": GITHUB_LIGHT_THEME,
    "gruvbox light": GRUVBOX_LIGHT_THEME,
    "one light": ONE_LIGHT_THEME,
}


class ThemeManager:
    """Manages themes for the IDE"""
    
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        self.themes = dict(BUILTIN_THEMES)
        self.custom_themes_dir = get_config_dir() / "themes"
        self.custom_themes_dir.mkdir(parents=True, exist_ok=True)
        self._load_custom_themes()
        self._current_theme: Optional[Theme] = None
    
    def _load_custom_themes(self):
        """Load custom themes from the themes directory"""
        for theme_file in self.custom_themes_dir.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    theme_name = theme_file.stem.lower()
                    # Convert dict to Theme object
                    syntax_data = data.pop('syntax', {})
                    syntax = SyntaxColors(**syntax_data) if syntax_data else SyntaxColors()
                    self.themes[theme_name] = Theme(syntax=syntax, **data)
            except Exception as e:
                print(f"Warning: Could not load theme {theme_file}: {e}")
    
    def get_theme(self, name: str) -> Theme:
        """Get a theme by name"""
        return self.themes.get(name.lower(), DARK_THEME)
    
    def get_current_theme(self) -> Theme:
        """Get the currently active theme"""
        if self._current_theme is None:
            theme_name = self.settings.settings.theme.current_theme
            self._current_theme = self.get_theme(theme_name)
        return self._current_theme
    
    def set_theme(self, name: str):
        """Set the current theme"""
        self.settings.settings.theme.current_theme = name
        self._current_theme = self.get_theme(name)
        self.settings.save()
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_current_stylesheet(self) -> str:
        """Generate Qt stylesheet for current theme"""
        return self.generate_stylesheet(self.get_current_theme())
    
    def generate_stylesheet(self, theme: Theme) -> str:
        """Generate a complete Qt stylesheet from a theme"""
        return f"""
/* Main Window */
QMainWindow, QWidget {{
    background-color: {theme.background};
    color: {theme.foreground};
    font-family: "Segoe UI", "SF Pro Display", "Ubuntu", sans-serif;
    font-size: 13px;
}}

/* Menu Bar */
QMenuBar {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border-bottom: 1px solid {theme.panel_border};
    padding: 4px 0px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 6px 12px;
    border-radius: 4px;
    margin: 0 2px;
}}

QMenuBar::item:selected {{
    background-color: {theme.button_hover};
}}

QMenuBar::item:pressed {{
    background-color: {theme.button_pressed};
}}

/* Menus */
QMenu {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border: 1px solid {theme.panel_border};
    border-radius: 8px;
    padding: 6px;
}}

QMenu::item {{
    padding: 8px 32px 8px 24px;
    border-radius: 4px;
    margin: 2px 4px;
}}

QMenu::item:selected {{
    background-color: {theme.accent};
    color: {theme.background};
}}

QMenu::separator {{
    height: 1px;
    background: {theme.panel_border};
    margin: 6px 12px;
}}

/* Toolbar */
QToolBar {{
    background-color: {theme.panel_background};
    border: none;
    padding: 4px;
    spacing: 4px;
}}

QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 8px;
    margin: 2px;
}}

QToolButton:hover {{
    background-color: {theme.button_hover};
}}

QToolButton:pressed {{
    background-color: {theme.button_pressed};
}}

/* Tabs */
QTabWidget::pane {{
    border: none;
    background-color: {theme.editor_background};
}}

QTabBar {{
    background-color: {theme.tab_background};
}}

QTabBar::tab {{
    background-color: {theme.tab_background};
    color: {theme.foreground};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 20px;
    margin-right: 1px;
}}

QTabBar::tab:selected {{
    background-color: {theme.tab_active_background};
    border-bottom: 2px solid {theme.accent};
}}

QTabBar::tab:hover:!selected {{
    background-color: {theme.tab_hover_background};
}}

QTabBar::close-button {{
    image: url(close.png);
    subcontrol-position: right;
    margin: 4px;
}}

/* Splitter */
QSplitter::handle {{
    background-color: {theme.panel_border};
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

QSplitter::handle:hover {{
    background-color: {theme.accent};
}}

/* Scrollbars */
QScrollBar:vertical {{
    background: {theme.scrollbar_background};
    width: 12px;
    border-radius: 6px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {theme.scrollbar_handle};
    border-radius: 5px;
    min-height: 30px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: {theme.scrollbar_handle_hover};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background: {theme.scrollbar_background};
    height: 12px;
    border-radius: 6px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {theme.scrollbar_handle};
    border-radius: 5px;
    min-width: 30px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {theme.scrollbar_handle_hover};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* Tree View (File Browser) */
QTreeView {{
    background-color: {theme.browser_background};
    color: {theme.foreground};
    border: none;
    outline: none;
    padding: 4px;
}}

QTreeView::item {{
    padding: 6px 8px;
    border-radius: 4px;
    margin: 1px 4px;
}}

QTreeView::item:hover {{
    background-color: {theme.browser_item_hover};
}}

QTreeView::item:selected {{
    background-color: {theme.browser_item_selected};
}}

QTreeView::branch {{
    background-color: {theme.browser_background};
}}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    image: url(branch-closed.png);
}}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    image: url(branch-open.png);
}}

/* Header View */
QHeaderView::section {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border: none;
    border-right: 1px solid {theme.panel_border};
    padding: 8px;
}}

/* Push Button */
QPushButton {{
    background-color: {theme.button_background};
    color: {theme.button_foreground};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {theme.button_hover};
}}

QPushButton:pressed {{
    background-color: {theme.button_pressed};
}}

QPushButton:disabled {{
    background-color: {theme.panel_border};
    color: {theme.editor_gutter_fg};
}}

/* Primary Button */
QPushButton[primary="true"] {{
    background-color: {theme.accent};
    color: {theme.background};
}}

QPushButton[primary="true"]:hover {{
    background-color: {theme.accent_hover};
}}

/* Line Edit */
QLineEdit {{
    background-color: {theme.input_background};
    color: {theme.foreground};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: {theme.accent};
}}

QLineEdit:focus {{
    border-color: {theme.input_focus_border};
}}

/* Text Edit */
QTextEdit, QPlainTextEdit {{
    background-color: {theme.editor_background};
    color: {theme.editor_foreground};
    border: none;
    selection-background-color: {theme.editor_selection};
}}

/* Combo Box */
QComboBox {{
    background-color: {theme.input_background};
    color: {theme.foreground};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: {theme.input_focus_border};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border: 1px solid {theme.panel_border};
    border-radius: 8px;
    selection-background-color: {theme.accent};
}}

/* Spin Box */
QSpinBox, QDoubleSpinBox {{
    background-color: {theme.input_background};
    color: {theme.foreground};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    padding: 8px;
}}

/* Check Box */
QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {theme.input_border};
    background-color: {theme.input_background};
}}

QCheckBox::indicator:checked {{
    background-color: {theme.accent};
    border-color: {theme.accent};
}}

/* Status Bar */
QStatusBar {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border-top: 1px solid {theme.panel_border};
    padding: 4px;
}}

QStatusBar::item {{
    border: none;
}}

/* Dock Widget */
QDockWidget {{
    titlebar-close-icon: url(close.png);
    titlebar-normal-icon: url(float.png);
}}

QDockWidget::title {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    padding: 8px;
    border-bottom: 1px solid {theme.panel_border};
}}

/* Group Box */
QGroupBox {{
    border: 1px solid {theme.panel_border};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
}}

QGroupBox::title {{
    color: {theme.foreground};
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {theme.input_background};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {theme.accent};
    border-radius: 4px;
}}

/* Tooltip */
QToolTip {{
    background-color: {theme.panel_background};
    color: {theme.foreground};
    border: 1px solid {theme.panel_border};
    border-radius: 6px;
    padding: 6px 10px;
}}

/* Label */
QLabel {{
    color: {theme.foreground};
}}

/* Dialog */
QDialog {{
    background-color: {theme.background};
}}

/* Message Box */
QMessageBox {{
    background-color: {theme.background};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}
"""
