from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

class Recipe:

    DB = "share_a_taste"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.ingredients = data['ingredients']
        self.instructions = data['instructions']
        self.duration = data['duration']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['title']) < 3:
            flash("Recipe title must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Recipe description must be at least 3 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO recipes (title, description, ingredients, instructions, duration, category, user_id, created_at)
            VALUES (%(title)s, %(description)s, %(ingredients)s, %(instructions)s, %(duration)s, %(category)s, %(user_id)s, NOW());
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for result in results:
            recipes.append(cls(result))
        return recipes

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM recipes WHERE user_id = %(user_id)s;"
        data = {"user_id": user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("Query:", query)
        print("Results:", results)
        recipes = []
        for result in results:
            recipes.append(cls(result))
        return recipes

    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes
            SET title = %(title)s, description = %(description)s, ingredients = %(ingredients)s,
                instructions = %(instructions)s, duration = %(duration)s, category = %(category)s
            WHERE id = %(recipe_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, recipe_id):
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        data = {"recipe_id": recipe_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def delete(cls, recipe_id):
        comment_delete_query = "DELETE FROM comments WHERE Recipe_id = %(recipe_id)s;"
        connectToMySQL(cls.DB).query_db(comment_delete_query, {'recipe_id': recipe_id})
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        data = {"recipe_id": recipe_id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all_ordered_by_id_desc(cls):
        query = "SELECT * FROM recipes ORDER BY id DESC;"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = [cls(result) for result in results]
        return recipes