# =========================================
# Model Layer - recipe_model.py
# =========================================
# The "Model" in MVC:
#
# Responsibilities:
#   - Define the Recipe data structure
#   - Provide CRUD methods (Create, Read, Update, Delete)
#   - Interact with the database layer (RecipeDatabase)
#
# The Model:
#   - Never directly talks to the UI (View)
#   - Acts as the middleman between Controller and Database
# =========================================

class Recipe:
    """
    Simple data container (Data Transfer Object) for a recipe.
    Fields map directly to the database columns.
    """
    def __init__(self, id, title, ingredients, instructions, image_path=None):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.image_path = image_path


class RecipeModel:
    """
    Handles all recipe-related operations by using the RecipeDatabase.
    Provides data as Recipe objects for the Controller/View to use.
    """

    def __init__(self, db):
        # db: an instance of RecipeDatabase from database.py
        self.db = db

    # ==================================================
    # CREATE (Controller → Model → Database)
    # ==================================================
    def add_recipe(self, title, ingredients, instructions, image_path=None):
        """Insert a new recipe into the database."""
        self.db.insert_recipe(title, ingredients, instructions, image_path)

    # ==================================================
    # READ
    # ==================================================
    def get_all_recipes(self):
        """
        Fetch all recipes from the database.
        Returns:
            list[Recipe]: A list of Recipe objects created from DB rows.
        """
        rows = self.db.get_all_recipes()  # Raw tuples from DB
        return [Recipe(*row) for row in rows]  # Convert to objects

    def get_recipe_by_id(self, recipe_id):
        """
        Fetch a single recipe by its ID.
        Returns:
            Recipe | None: The recipe if found, else None.
        """
        recipes = self.get_all_recipes()
        for recipe in recipes:
            if recipe.id == recipe_id:
                return recipe
        return None

    # ==================================================
    # UPDATE
    # ==================================================
    def update_recipe(self, recipe):
        """
        Update an existing recipe in the database.
        Args:
            recipe (Recipe): The updated Recipe object.
        """
        self.db.update_recipe(
            recipe.id,
            recipe.title,
            recipe.ingredients,
            recipe.instructions,
            recipe.image_path
        )

    # ==================================================
    # DELETE
    # ==================================================
    def delete_recipe(self, recipe_id):
        """Delete a recipe from the database by its ID."""
        self.db.delete_recipe(recipe_id)



