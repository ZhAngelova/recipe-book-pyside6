# =========================================
# Controller Layer - recipe_controller.py
# =========================================
# The "Controller" in MVC:
#
#   - Listens to signals (button clicks, list selections) from the View
#   - Calls Model methods to create, read, update, or delete data
#   - Updates the View with fresh data from the Model
#   - Implements logic to prevent invalid actions (e.g., duplicates)
#
# The Controller knows about both the Model and the View,
# but Model and View never directly talk to each other.
# =========================================

from PySide6.QtWidgets import QFileDialog
from model.recipe_model import Recipe


class RecipeController:
    """Connects the Recipe View and Recipe Model."""

    def __init__(self, model, view):
        self.model = model  # Data handling (Model)
        self.view = view    # GUI (View)

        # --------------------------
        # Connect View events to Controller actions
        # --------------------------
        self.view.add_button.clicked.connect(self.add_recipe)
        self.view.edit_button.clicked.connect(self.edit_selected_recipe)
        self.view.save_button.clicked.connect(self.save_edited_recipe)
        self.view.cancel_button.clicked.connect(self.cancel_edit)
        self.view.delete_button.clicked.connect(self.delete_selected_recipe)
        self.view.image_button.clicked.connect(self.select_image)
        self.view.recipe_list.itemSelectionChanged.connect(self.display_selected_recipe)

        # Load recipe list when app starts
        self.refresh_recipe_list()

    # ==================================================
    # CREATE
    # ==================================================
    def add_recipe(self):
        """
        Add a new recipe to the database.
        If not currently in 'add' mode, clear the form and switch modes first
        to prevent accidental duplication.
        """
        if self.view.mode != "add":
            self.view.clear_inputs()
            self.view.set_mode("add")
            return

        title, ingredients, instructions, image_path = self.view.get_input_data()

        # Title is mandatory; ignore if blank
        if not title.strip():
            return

        # Controller → Model: Create new recipe
        self.model.add_recipe(
            title.strip(),
            ingredients.strip(),
            instructions.strip(),
            image_path
        )

        # Refresh list in View and reset form
        self.refresh_recipe_list()
        self.view.clear_inputs()

    # ==================================================
    # READ + switch to edit mode
    # ==================================================
    def edit_selected_recipe(self):
        """
        Load the selected recipe into the form for editing.
        Switch to 'edit' mode so Save/Cancel buttons are active.
        """
        recipe_id = self.view.get_selected_recipe_id()
        if recipe_id is None:
            return

        recipe = self.model.get_recipe_by_id(recipe_id)
        if recipe:
            self.view.show_recipe_details(recipe)
            self.view.set_mode("edit")

    # ==================================================
    # UPDATE
    # ==================================================
    def save_edited_recipe(self):
        """
        Save the current form's changes back to the database.
        Stay on the same recipe afterward (switch to 'view' mode).
        """
        recipe_id = self.view.get_current_recipe_id()
        if recipe_id is None:
            return

        title, ingredients, instructions, image_path = self.view.get_input_data()
        if not title.strip():
            return

        # Create updated Recipe object and pass to Model
        updated_recipe = Recipe(
            recipe_id,
            title.strip(),
            ingredients.strip(),
            instructions.strip(),
            image_path
        )
        self.model.update_recipe(updated_recipe)

        # Refresh list and reload this recipe
        self.refresh_recipe_list()
        recipe = self.model.get_recipe_by_id(recipe_id)
        if recipe:
            self.view.show_recipe_details(recipe)

        # Switch to read-only view mode
        self.view.set_mode("view")

    # ==================================================
    # CANCEL EDIT
    # ==================================================
    def cancel_edit(self):
        """
        Abort editing:
        - If a recipe was loaded, restore its details.
        - If none was loaded, just clear the form.
        Return to 'add' mode.
        """
        recipe_id = self.view.get_current_recipe_id()
        if recipe_id:
            recipe = self.model.get_recipe_by_id(recipe_id)
            if recipe:
                self.view.show_recipe_details(recipe)
        else:
            self.view.clear_inputs()
        self.view.set_mode("add")

    # ==================================================
    # DELETE
    # ==================================================
    def delete_selected_recipe(self):
        """Remove the selected recipe from the database and clear the form."""
        recipe_id = self.view.get_selected_recipe_id()
        if recipe_id is None:
            return

        self.model.delete_recipe(recipe_id)
        self.view.clear_inputs()
        self.refresh_recipe_list()

    # ==================================================
    # VIEW (display without editing)
    # ==================================================
    def display_selected_recipe(self):
        """
        Show details of the currently selected recipe.
        Mode is set to 'view' so editing buttons stay disabled.
        """
        recipe_id = self.view.get_selected_recipe_id()
        if recipe_id:
            recipe = self.model.get_recipe_by_id(recipe_id)
            if recipe:
                self.view.show_recipe_details(recipe)
                self.view.set_mode("view")

    # ==================================================
    # IMAGE PICKER
    # ==================================================
    def select_image(self):
        """Open a file dialog to pick a recipe image and update the form."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Select Recipe Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.view.set_image_path(file_path)

    # ==================================================
    # HELPER
    # ==================================================
    def refresh_recipe_list(self):
        """Ask Model for all recipes and send them to the View."""
        recipes = self.model.get_all_recipes()
        self.view.update_recipe_list(recipes)


    
        
        