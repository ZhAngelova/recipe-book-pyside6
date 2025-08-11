# =========================================
# Main Entry Point
# =========================================
# This file is where the program starts.
# Its main job is to:
#   1. Set up the PySide6 application.
#   2. Create the Model, View, and Controller objects.
#   3. Connect everything together.
#   4. Optionally insert sample data into the database.
#   5. Start the Qt event loop so the app stays open.
# =========================================

import sys
import os
from PySide6.QtWidgets import QApplication

# Import the three MVC layers
# ---------------------------
# Model    → Holds the data and logic.
# View     → The GUI (what the user sees).
# Controller → The middleman: connects View and Model.
from model.database import RecipeDatabase
from model.recipe_model import RecipeModel
from view.main_window import RecipeMainWindow
from controller.recipe_controller import RecipeController


# =========================================
# Function: populate_sample_data
# =========================================
# Purpose:
#   This function checks if the database is empty.
#   If it is, it adds a couple of pre-made recipes
#   (with optional images) so the app isn't blank
#   when first launched.
# =========================================
def populate_sample_data(model):
    """Insert a couple of sample recipes with images if the database is empty."""
    
    # Only add samples if there are NO recipes yet
    if not model.get_all_recipes():
        
        # Determine the path to the "images" folder in the project
        image_dir = os.path.join(os.path.dirname(__file__), "images")
        
        # Build full paths for the two sample images
        carbonara_img = os.path.join(image_dir, "carbonara.jpg")
        cake_img = os.path.join(image_dir, "chocolate_cake.jpg")

        # Add first sample recipe
        model.add_recipe(
            "Spaghetti Carbonara",
            "Spaghetti, Eggs, Parmesan cheese, Bacon, Pepper",
            "1. Boil pasta.\n2. Fry bacon.\n3. Mix eggs and cheese.\n4. Combine all with pasta.",
            carbonara_img if os.path.exists(carbonara_img) else None
        )

        # Add second sample recipe
        model.add_recipe(
            "Chocolate Cake",
            "Flour, Cocoa powder, Sugar, Eggs, Butter, Baking powder",
            "1. Mix dry ingredients.\n2. Add wet ingredients.\n3. Bake at 180°C for 35 min.",
            cake_img if os.path.exists(cake_img) else None
        )


# =========================================
# Function: main
# =========================================
# Purpose:
#   Sets up the Qt application and wires the MVC layers together.
#   Also inserts sample recipes if needed, shows the window,
#   and starts the application event loop.
# =========================================
def main():
    # --------------------------
    # Step 1: Qt Application setup
    # --------------------------
    # QApplication handles the app's event loop and resources.
    # sys.argv passes any command-line arguments to Qt.
    app = QApplication(sys.argv)

    # --------------------------
    # Step 2: Create the MVC layers
    # --------------------------
    db_path = "recipes.db"            # SQLite database file
    db = RecipeDatabase(db_path)      # Low-level database handler (Data Layer)
    model = RecipeModel(db)           # Business logic (Model Layer)
    view = RecipeMainWindow()         # GUI layout & widgets (View Layer)
    controller = RecipeController(model, view)  # Event handling (Controller Layer)

    # --------------------------
    # Step 3: Preload sample data
    # --------------------------
    populate_sample_data(model)       # Only runs if DB is empty
    controller.refresh_recipe_list()  # Refresh the list in the View

    # --------------------------
    # Step 4: Show the window
    # --------------------------
    view.show()  # Makes the main window visible

    # --------------------------
    # Step 5: Start the Qt event loop
    # --------------------------
    # sys.exit ensures a clean exit code when the app closes.
    sys.exit(app.exec())


# =========================================
# Python entry point check
# =========================================
# This ensures that `main()` runs only if this file
# is executed directly, not if it's imported.
# =========================================
if __name__ == "__main__":
    main()





