# =========================================
# View Layer - main_window.py
# =========================================
# This file is the "View" in the MVC pattern.
#
# Responsibilities:
#   - Build and arrange the GUI using PySide6 widgets.
#   - Display recipe data received from the Controller.
#   - Collect user input to be sent to the Controller.
#   - Never directly access the database (Model).
#
# In this app, the "View" is a QWidget that holds:
#   - Form fields for a recipe
#   - A preview area for the recipe image
#   - A list of recipes
#   - Buttons for actions (add, edit, save, delete, cancel)
# =========================================

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QListWidget,
    QLineEdit, QListWidgetItem, QLabel
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class RecipeMainWindow(QWidget):
    """Main application window for the Recipe Book."""

    def __init__(self):
        super().__init__()

        # --------------------------
        # Window setup
        # --------------------------
        self.setWindowTitle("Recipe Book")
        self.setMinimumSize(600, 500)

        # Main vertical layout
        layout = QVBoxLayout()

        # --------------------------
        # Input fields
        # --------------------------
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Recipe Title")

        self.ingredients_input = QTextEdit()
        self.ingredients_input.setPlaceholderText("Ingredients")

        self.instructions_input = QTextEdit()
        self.instructions_input.setPlaceholderText("Instructions")

        # --------------------------
        # Image selection and preview
        # --------------------------
        self.image_button = QPushButton("Select Image")

        self.image_label = QLabel("No Image Selected")
        self.image_label.setFixedSize(300, 200)  # Reserve space for preview
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #555; background: #222;")
        # We don't stretch images to fill the box; scaling is handled in set_image_path()
        self.image_label.setScaledContents(False)

        # --------------------------
        # Action buttons
        # --------------------------
        self.add_button = QPushButton("Add Recipe")
        self.edit_button = QPushButton("Edit Selected Recipe")
        self.save_button = QPushButton("Save Changes")
        self.cancel_button = QPushButton("Cancel Edit")
        self.delete_button = QPushButton("Delete Selected Recipe")

        # --------------------------
        # Recipe list
        # --------------------------
        self.recipe_list = QListWidget()

        # --------------------------
        # Add all widgets to layout
        # --------------------------
        layout.addWidget(self.title_input)
        layout.addWidget(self.ingredients_input)
        layout.addWidget(self.instructions_input)
        layout.addWidget(self.image_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.recipe_list)

        self.setLayout(layout)

        # --------------------------
        # Internal state
        # --------------------------
        self._selected_image_path = None    # Stores current image file path
        self._current_recipe_id = None      # Stores current recipe ID
        self.mode = "add"                   # Modes: add, edit, view

        self.set_mode("add")  # Start in add mode

    # ==================================================
    # Mode handling
    # ==================================================
    def set_mode(self, mode):
        """
        Change the interface mode:
          - 'add'  : Ready to create a new recipe
          - 'edit' : Editing an existing recipe
          - 'view' : Viewing an existing recipe
        Mode determines which buttons are active.
        """
        self.mode = mode
        if mode == "add":
            self.add_button.setEnabled(True)
            self.save_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
        elif mode == "edit":
            self.add_button.setEnabled(False)
            self.save_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
        elif mode == "view":
            self.add_button.setEnabled(True)
            self.save_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

    # ==================================================
    # Form helpers
    # ==================================================
    def get_input_data(self):
        """Return form field values as a tuple."""
        return (
            self.title_input.text(),
            self.ingredients_input.toPlainText(),
            self.instructions_input.toPlainText(),
            self._selected_image_path
        )

    def clear_inputs(self):
        """Clear all inputs and return to add mode."""
        self.title_input.clear()
        self.ingredients_input.clear()
        self.instructions_input.clear()
        self.image_label.setText("No Image Selected")
        self._selected_image_path = None
        self._current_recipe_id = None
        self.set_mode("add")

    def set_image_path(self, path):
        """Store and display the selected image while keeping its aspect ratio."""
        self._selected_image_path = path
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def update_recipe_list(self, recipes):
        """
        Populate the recipe list widget.
        Stores recipe.id in Qt.UserRole (data role 32) for retrieval later.
        """
        self.recipe_list.clear()
        for recipe in recipes:
            item = QListWidgetItem(recipe.title)
            item.setData(32, recipe.id)  # Qt.UserRole
            self.recipe_list.addItem(item)

    def get_selected_recipe_id(self):
        """Return the recipe ID of the currently selected list item."""
        item = self.recipe_list.currentItem()
        return item.data(32) if item else None

    def get_current_recipe_id(self):
        """Return the ID of the recipe currently loaded in the form."""
        return self._current_recipe_id

    def show_recipe_details(self, recipe):
        """Display recipe details in the form."""
        self._current_recipe_id = recipe.id
        self.title_input.setText(recipe.title)
        self.ingredients_input.setPlainText(recipe.ingredients)
        self.instructions_input.setPlainText(recipe.instructions)

        if recipe.image_path:
            pixmap = QPixmap(recipe.image_path)
            scaled = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
            self._selected_image_path = recipe.image_path
        else:
            self.image_label.setText("No Image Selected")
            self._selected_image_path = None


