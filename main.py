#!/usr/bin/env python3
"""
EZ IDE - A modern IDE for the EZ programming language
"""

import sys
import os

# Add the package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from app.main_window import EZIDEMainWindow
from app.settings import SettingsManager


def main():
    """Main entry point for the EZ IDE"""
    # Enable high DPI scaling
    app = QApplication(sys.argv)
    app.setApplicationName("EZ IDE")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("EZ Language")
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "EZ_LOGO.jpeg")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Load settings
    settings = SettingsManager()
    
    # Apply theme
    from app.themes import ThemeManager
    theme_manager = ThemeManager(settings)
    app.setStyleSheet(theme_manager.get_current_stylesheet())
    
    # Create and show main window
    window = EZIDEMainWindow(settings, theme_manager)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
