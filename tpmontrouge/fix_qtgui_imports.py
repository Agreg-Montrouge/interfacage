#!/usr/bin/env python3
"""
Fix Qt imports to use QtWidgets instead of QtGui for widget classes.
This is needed for Qt5/Qt6 compatibility where widget classes moved from QtGui to QtWidgets.
"""

import re
import sys
from pathlib import Path

# Widget classes that moved from QtGui to QtWidgets in Qt5/Qt6
WIDGET_CLASSES = [
    'QWidget', 'QApplication', 'QMainWindow', 'QDialog',
    'QVBoxLayout', 'QHBoxLayout', 'QGridLayout', 'QFormLayout',
    'QPushButton', 'QLabel', 'QLineEdit', 'QTextEdit', 'QPlainTextEdit',
    'QCheckBox', 'QRadioButton', 'QComboBox', 'QSpinBox', 'QDoubleSpinBox',
    'QSlider', 'QProgressBar', 'QScrollBar',
    'QListWidget', 'QTableWidget', 'QTreeWidget',
    'QTabWidget', 'QStackedWidget', 'QSplitter',
    'QGroupBox', 'QFrame', 'QScrollArea',
    'QFileDialog', 'QMessageBox', 'QInputDialog', 'QColorDialog',
    'QFontDialog', 'QProgressDialog',
    'QSizePolicy', 'QAction', 'QMenu', 'QMenuBar', 'QToolBar', 'QStatusBar',
]

def fix_file(filepath):
    """Fix QtGui imports in a single file."""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Step 1: Add QtWidgets to imports if needed
    # Pattern: from pyqtgraph.Qt import QtCore, QtGui
    import_pattern = r'from pyqtgraph\.Qt import (.+)'
    
    def fix_import(match):
        imports = match.group(1)
        parts = [p.strip() for p in imports.split(',')]
        if 'QtWidgets' not in parts:
            parts.append('QtWidgets')
        return f'from pyqtgraph.Qt import {", ".join(parts)}'
    
    content = re.sub(import_pattern, fix_import, content)
    
    # Step 2: Replace QtGui.QWidget -> QtWidgets.QWidget for all widget classes
    for widget_class in WIDGET_CLASSES:
        # Replace QtGui.QClass with QtWidgets.QClass
        pattern = rf'\bQtGui\.{widget_class}\b'
        replacement = f'QtWidgets.{widget_class}'
        content = re.sub(pattern, replacement, content)
    
    # Write back if changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✓ Fixed {filepath}")
        return True
    else:
        print(f"  - No changes needed for {filepath}")
        return False

def main():
    # Find all Python files in tpmontrouge/interface/
    base_dir = Path(__file__).parent / 'tpmontrouge' / 'interface'
    
    if not base_dir.exists():
        print(f"Error: {base_dir} does not exist")
        sys.exit(1)
    
    py_files = list(base_dir.rglob('*.py'))
    
    # Filter out __pycache__ and backup files
    py_files = [f for f in py_files if '__pycache__' not in str(f) and not f.name.endswith('~')]
    
    print(f"Found {len(py_files)} Python files to process\n")
    
    fixed_count = 0
    for filepath in py_files:
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nDone! Fixed {fixed_count}/{len(py_files)} files")

if __name__ == '__main__':
    main()
