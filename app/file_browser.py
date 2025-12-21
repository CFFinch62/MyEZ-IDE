"""
File Browser Widget for EZ IDE
Full-featured file/folder browser with bookmarks, context menu, and navigation
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QPushButton, QLineEdit, QMenu, QMessageBox, QInputDialog,
    QToolButton, QFrame, QLabel, QListWidget, QListWidgetItem,
    QSplitter, QHeaderView, QAbstractItemView, QToolBar, QComboBox
)
from PyQt6.QtCore import (
    Qt, QDir, QModelIndex, pyqtSignal, QFileInfo, QSize, QMimeData, QTimer
)
from PyQt6.QtGui import (
    QIcon, QAction, QKeySequence, QFileSystemModel,
    QDragEnterEvent, QDropEvent
)

from app.settings import SettingsManager


class BookmarksWidget(QWidget):
    """Widget for displaying folder bookmarks"""
    
    bookmark_clicked = pyqtSignal(str)  # path
    bookmark_removed = pyqtSignal(str)  # path
    
    def __init__(self, settings: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._setup_ui()
        self._load_bookmarks()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName("bookmarks_header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 4, 8, 4)
        
        label = QLabel("Bookmarks")
        label.setStyleSheet("font-weight: bold; font-size: 11px; opacity: 0.7;")
        header_layout.addWidget(label)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Bookmarks list
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)
        self.list_widget.itemDoubleClicked.connect(self._on_item_clicked)
        self.list_widget.setMaximumHeight(150)
        layout.addWidget(self.list_widget)
    
    def _load_bookmarks(self):
        """Load bookmarks from settings"""
        self.list_widget.clear()
        for path in self.settings.settings.file_browser.bookmarks:
            if os.path.exists(path):
                item = QListWidgetItem(os.path.basename(path) or path)
                item.setData(Qt.ItemDataRole.UserRole, path)
                item.setToolTip(path)
                self.list_widget.addItem(item)
    
    def add_bookmark(self, path: str):
        """Add a new bookmark"""
        self.settings.add_bookmark(path)
        self._load_bookmarks()
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle bookmark item click"""
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and os.path.exists(path):
            self.bookmark_clicked.emit(path)
    
    def _show_context_menu(self, pos):
        """Show context menu for bookmark"""
        item = self.list_widget.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)
        
        open_action = menu.addAction("Open")
        open_action.triggered.connect(lambda: self._on_item_clicked(item))
        
        menu.addSeparator()
        
        remove_action = menu.addAction("Remove Bookmark")
        remove_action.triggered.connect(lambda: self._remove_bookmark(item))
        
        menu.exec(self.list_widget.mapToGlobal(pos))
    
    def _remove_bookmark(self, item: QListWidgetItem):
        """Remove a bookmark"""
        path = item.data(Qt.ItemDataRole.UserRole)
        self.settings.remove_bookmark(path)
        self._load_bookmarks()
        self.bookmark_removed.emit(path)


class FileBrowserWidget(QWidget):
    """Main file browser widget"""
    
    file_opened = pyqtSignal(str)  # file path
    file_created = pyqtSignal(str)  # file path
    folder_changed = pyqtSignal(str)  # folder path
    
    def __init__(self, settings: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.current_root = ""
        
        # Timer for distinguishing single vs double clicks
        self._click_timer = QTimer(self)
        self._click_timer.setSingleShot(True)
        self._click_timer.timeout.connect(self._on_single_click_timeout)
        self._pending_click_index = None
        
        self._setup_ui()
        self._setup_connections()
        self._load_initial_directory()
    
    def _setup_ui(self):
        """Set up the file browser UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setMovable(False)
        
        # Navigation buttons
        self.back_btn = QToolButton()
        self.back_btn.setText("←")
        self.back_btn.setToolTip("Go Back")
        self.toolbar.addWidget(self.back_btn)
        
        self.forward_btn = QToolButton()
        self.forward_btn.setText("→")
        self.forward_btn.setToolTip("Go Forward")
        self.toolbar.addWidget(self.forward_btn)
        
        self.up_btn = QToolButton()
        self.up_btn.setText("↑")
        self.up_btn.setToolTip("Go Up")
        self.toolbar.addWidget(self.up_btn)
        
        self.home_btn = QToolButton()
        self.home_btn.setText("⌂")
        self.home_btn.setToolTip("Go Home")
        self.toolbar.addWidget(self.home_btn)
        
        self.toolbar.addSeparator()
        
        self.refresh_btn = QToolButton()
        self.refresh_btn.setText("⟳")
        self.refresh_btn.setToolTip("Refresh")
        self.toolbar.addWidget(self.refresh_btn)
        
        self.new_file_btn = QToolButton()
        self.new_file_btn.setText("+📄")
        self.new_file_btn.setToolTip("New File")
        self.toolbar.addWidget(self.new_file_btn)
        
        self.new_folder_btn = QToolButton()
        self.new_folder_btn.setText("+📁")
        self.new_folder_btn.setToolTip("New Folder")
        self.toolbar.addWidget(self.new_folder_btn)
        
        self.toolbar.addSeparator()
        
        self.bookmark_btn = QToolButton()
        self.bookmark_btn.setText("⭐")
        self.bookmark_btn.setToolTip("Bookmark Current Folder")
        self.toolbar.addWidget(self.bookmark_btn)
        
        layout.addWidget(self.toolbar)
        
        # Path bar
        self.path_bar = QLineEdit()
        self.path_bar.setPlaceholderText("Enter path...")
        layout.addWidget(self.path_bar)
        
        # Main splitter for bookmarks and tree
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Bookmarks
        self.bookmarks = BookmarksWidget(self.settings)
        splitter.addWidget(self.bookmarks)
        
        # File tree
        tree_container = QWidget()
        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        
        # File tree header
        tree_header = QFrame()
        tree_header_layout = QHBoxLayout(tree_header)
        tree_header_layout.setContentsMargins(8, 4, 8, 4)
        
        self.folder_label = QLabel("Files")
        self.folder_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        tree_header_layout.addWidget(self.folder_label)
        tree_header_layout.addStretch()
        
        # Toggle hidden files button
        self.hidden_toggle = QToolButton()
        self.hidden_toggle.setText("👁")
        self.hidden_toggle.setToolTip("Toggle Hidden Files")
        self.hidden_toggle.setCheckable(True)
        self.hidden_toggle.setChecked(self.settings.settings.file_browser.show_hidden_files)
        tree_header_layout.addWidget(self.hidden_toggle)
        
        tree_layout.addWidget(tree_header)
        
        # File system model
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self._update_filters()
        
        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(16)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        
        # Hide extra columns
        self.tree.setColumnHidden(1, True)  # Size
        self.tree.setColumnHidden(2, True)  # Type
        self.tree.setColumnHidden(3, True)  # Date
        
        tree_layout.addWidget(self.tree)
        splitter.addWidget(tree_container)
        
        # Set splitter sizes
        splitter.setSizes([100, 400])
        layout.addWidget(splitter)
        
        # History for navigation
        self.history: List[str] = []
        self.history_index = -1
    
    def _setup_connections(self):
        """Set up signal connections"""
        self.tree.clicked.connect(self._on_item_clicked)
        self.tree.doubleClicked.connect(self._on_item_double_clicked)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        
        self.path_bar.returnPressed.connect(self._on_path_entered)
        
        self.back_btn.clicked.connect(self._go_back)
        self.forward_btn.clicked.connect(self._go_forward)
        self.up_btn.clicked.connect(self._go_up)
        self.home_btn.clicked.connect(self._go_home)
        self.refresh_btn.clicked.connect(self._refresh)
        self.new_file_btn.clicked.connect(self._create_new_file)
        self.new_folder_btn.clicked.connect(self._create_new_folder)
        self.bookmark_btn.clicked.connect(self._bookmark_current_folder)
        
        self.hidden_toggle.toggled.connect(self._toggle_hidden_files)
        
        self.bookmarks.bookmark_clicked.connect(self.navigate_to)
    
    def _load_initial_directory(self):
        """Load the initial directory"""
        last_dir = self.settings.settings.file_browser.last_directory
        if last_dir and os.path.exists(last_dir):
            self.navigate_to(last_dir)
        else:
            self.navigate_to(str(Path.home()))
    
    def _update_filters(self):
        """Update file filters based on settings"""
        if self.settings.settings.file_browser.show_hidden_files:
            self.model.setFilter(
                QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | 
                QDir.Filter.Hidden | QDir.Filter.AllDirs
            )
        else:
            self.model.setFilter(
                QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | 
                QDir.Filter.AllDirs
            )
    
    def navigate_to(self, path: str, add_to_history: bool = True):
        """Navigate to a directory"""
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return
        
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        self.current_root = path
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.path_bar.setText(path)
        self.folder_label.setText(os.path.basename(path) or path)
        
        # Update history
        if add_to_history:
            # Remove forward history
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index = len(self.history) - 1
        
        # Update navigation buttons
        self.back_btn.setEnabled(self.history_index > 0)
        self.forward_btn.setEnabled(self.history_index < len(self.history) - 1)
        
        # Save to settings
        self.settings.settings.file_browser.last_directory = path
        self.settings.save()
        
        self.folder_changed.emit(path)
    
    def _on_item_clicked(self, index: QModelIndex):
        """Handle click on item - delay to check for double-click"""
        path = self.model.filePath(index)
        if os.path.isdir(path):
            # Store the index and start timer - if double-click comes, timer is cancelled
            self._pending_click_index = index
            self._click_timer.start(250)  # 250ms delay to wait for potential double-click
    
    def _on_single_click_timeout(self):
        """Called when single-click timer expires (no double-click detected)"""
        if self._pending_click_index is not None:
            index = self._pending_click_index
            self._pending_click_index = None
            path = self.model.filePath(index)
            if os.path.isdir(path):
                # Toggle expand/collapse for folders
                if self.tree.isExpanded(index):
                    self.tree.collapse(index)
                else:
                    self.tree.expand(index)
    
    def _on_item_double_clicked(self, index: QModelIndex):
        """Handle double-click on item"""
        # Cancel any pending single-click action
        self._click_timer.stop()
        self._pending_click_index = None
        
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.navigate_to(path)
        else:
            self.file_opened.emit(path)
    
    def _on_path_entered(self):
        """Handle path entered in path bar"""
        path = self.path_bar.text()
        if os.path.exists(path):
            if os.path.isfile(path):
                self.file_opened.emit(path)
            else:
                self.navigate_to(path)
        else:
            QMessageBox.warning(self, "Invalid Path", f"Path does not exist: {path}")
    
    def _go_back(self):
        """Navigate back in history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.navigate_to(self.history[self.history_index], add_to_history=False)
    
    def _go_forward(self):
        """Navigate forward in history"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.navigate_to(self.history[self.history_index], add_to_history=False)
    
    def _go_up(self):
        """Navigate to parent directory"""
        if self.current_root:
            parent = os.path.dirname(self.current_root)
            if parent and parent != self.current_root:
                self.navigate_to(parent)
    
    def _go_home(self):
        """Navigate to home directory"""
        self.navigate_to(str(Path.home()))
    
    def _bookmark_current_folder(self):
        """Add the current folder to bookmarks"""
        if self.current_root:
            self.bookmarks.add_bookmark(self.current_root)
    
    def _refresh(self):
        """Refresh the current directory"""
        if self.current_root:
            # Force refresh by re-setting root
            self.model.setRootPath("")
            self.model.setRootPath(self.current_root)
            self.tree.setRootIndex(self.model.index(self.current_root))
    
    def _toggle_hidden_files(self, show: bool):
        """Toggle display of hidden files"""
        self.settings.settings.file_browser.show_hidden_files = show
        self.settings.save()
        self._update_filters()
        self._refresh()
    
    def _show_context_menu(self, pos):
        """Show context menu for file browser"""
        index = self.tree.indexAt(pos)
        menu = QMenu(self)
        
        if index.isValid():
            path = self.model.filePath(index)
            is_dir = os.path.isdir(path)
            
            # Open
            if is_dir:
                open_action = menu.addAction("Open Folder")
                open_action.triggered.connect(lambda: self.navigate_to(path))
            else:
                open_action = menu.addAction("Open File")
                open_action.triggered.connect(lambda: self.file_opened.emit(path))
            
            menu.addSeparator()
            
            # New items
            if is_dir:
                new_file_action = menu.addAction("New File Here...")
                new_file_action.triggered.connect(lambda: self._create_new_file(path))
                
                new_folder_action = menu.addAction("New Folder Here...")
                new_folder_action.triggered.connect(lambda: self._create_new_folder(path))
                
                menu.addSeparator()
            
            # Rename
            rename_action = menu.addAction("Rename...")
            rename_action.triggered.connect(lambda: self._rename_item(path))
            
            # Delete
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self._delete_item(path))
            
            menu.addSeparator()
            
            # Copy path
            copy_path_action = menu.addAction("Copy Path")
            copy_path_action.triggered.connect(
                lambda: self._copy_to_clipboard(path)
            )
            
            if is_dir:
                menu.addSeparator()
                
                # Bookmark
                if path in self.settings.settings.file_browser.bookmarks:
                    bookmark_action = menu.addAction("Remove Bookmark")
                    bookmark_action.triggered.connect(
                        lambda: self.settings.remove_bookmark(path)
                    )
                else:
                    bookmark_action = menu.addAction("Add to Bookmarks")
                    bookmark_action.triggered.connect(
                        lambda: self.bookmarks.add_bookmark(path)
                    )
        else:
            # Context menu for empty space
            new_file_action = menu.addAction("New File...")
            new_file_action.triggered.connect(lambda: self._create_new_file())
            
            new_folder_action = menu.addAction("New Folder...")
            new_folder_action.triggered.connect(lambda: self._create_new_folder())
            
            menu.addSeparator()
            
            refresh_action = menu.addAction("Refresh")
            refresh_action.triggered.connect(self._refresh)
        
        menu.exec(self.tree.viewport().mapToGlobal(pos))
    
    def _create_new_file(self, directory: str = None):
        """Create a new file"""
        if directory is None:
            directory = self.current_root
        
        name, ok = QInputDialog.getText(
            self, "New File", "Enter file name:",
            text="untitled.ez"
        )
        
        if ok and name:
            filepath = os.path.join(directory, name)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("")
                self._refresh()
                self.file_created.emit(filepath)
                self.file_opened.emit(filepath)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {e}")
    
    def _create_new_folder(self, directory: str = None):
        """Create a new folder"""
        if directory is None:
            directory = self.current_root
        
        name, ok = QInputDialog.getText(
            self, "New Folder", "Enter folder name:",
            text="New Folder"
        )
        
        if ok and name:
            folderpath = os.path.join(directory, name)
            try:
                os.makedirs(folderpath, exist_ok=True)
                self._refresh()
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not create folder: {e}")
    
    def _rename_item(self, path: str):
        """Rename a file or folder"""
        old_name = os.path.basename(path)
        new_name, ok = QInputDialog.getText(
            self, "Rename", "Enter new name:",
            text=old_name
        )
        
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            try:
                os.rename(path, new_path)
                self._refresh()
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not rename: {e}")
    
    def _delete_item(self, path: str):
        """Delete a file or folder"""
        name = os.path.basename(path)
        is_dir = os.path.isdir(path)
        
        msg = f"Are you sure you want to delete {'folder' if is_dir else 'file'} '{name}'?"
        if is_dir:
            msg += "\n\nThis will delete all contents!"
        
        reply = QMessageBox.question(
            self, "Confirm Delete", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if is_dir:
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self._refresh()
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not delete: {e}")
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
    
    def get_selected_path(self) -> Optional[str]:
        """Get the currently selected path"""
        indexes = self.tree.selectedIndexes()
        if indexes:
            return self.model.filePath(indexes[0])
        return None
    
    def select_file(self, filepath: str):
        """Select a file in the tree"""
        index = self.model.index(filepath)
        if index.isValid():
            self.tree.setCurrentIndex(index)
            self.tree.scrollTo(index)
