# =========================================
# Data Layer - database.py
# =========================================
# The "Data Layer" in MVC architecture.
#
# Responsibilities:
#   - Connect to the SQLite database file.
#   - Create the 'recipes' table if it doesn't exist.
#   - Perform raw SQL queries (INSERT, SELECT, UPDATE, DELETE).
#
# Notes:
#   - Knows nothing about the GUI (View).
#   - The Controller → Model → Database chain handles all interaction.
# =========================================

import sqlite3


class RecipeDatabase:
    """
    Handles low-level database operations for recipes.
    Uses Python's built-in sqlite3 module.
    """

    def __init__(self, db_name="recipes.db"):
        """
        Connect to the SQLite database.
        If it doesn't exist, it will be created automatically.
        """
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    # ==================================================
    # TABLE CREATION
    # ==================================================
    def create_table(self):
        """
        Create the 'recipes' table if it doesn't already exist.
        Columns:
          - id           → Primary key (auto-increment)
          - title        → Recipe name (text, required)
          - ingredients  → Ingredients list (text)
          - instructions → Cooking steps (text)
          - image_path   → Path to an image file (text, optional)
        """
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT,
                instructions TEXT,
                image_path TEXT
            )
        """)

    # ==================================================
    # CREATE (Controller → Model → Database)
    # ==================================================
    def insert_recipe(self, title, ingredients, instructions, image_path):
        """Insert a new recipe into the database."""
        self.conn.execute("""
            INSERT INTO recipes (title, ingredients, instructions, image_path)
            VALUES (?, ?, ?, ?)
        """, (title, ingredients, instructions, image_path))
        self.conn.commit()

    # ==================================================
    # READ
    # ==================================================
    def get_all_recipes(self):
        """
        Fetch all recipes from the database.
        Returns:
            list[tuple]: Each tuple = (id, title, ingredients, instructions, image_path)
        """
        cursor = self.conn.execute("SELECT * FROM recipes")
        return cursor.fetchall()

    # ==================================================
    # UPDATE
    # ==================================================
    def update_recipe(self, recipe_id, title, ingredients, instructions, image_path):
        """Update an existing recipe in the database."""
        self.conn.execute("""
            UPDATE recipes
            SET title = ?, ingredients = ?, instructions = ?, image_path = ?
            WHERE id = ?
        """, (title, ingredients, instructions, image_path, recipe_id))
        self.conn.commit()

    # ==================================================
    # DELETE
    # ==================================================
    def delete_recipe(self, recipe_id):
        """Delete a recipe from the database by its ID."""
        self.conn.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
        self.conn.commit()


