from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

class Comment:

    DB = "share_a_taste"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.recipe_id = data['recipe_id']
        self.comment = data['comment']
        self.name = data['name']
        self.created_at = data['created_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comments (user_id, recipe_id, comment, name, created_at)
            VALUES (%(user_id)s, %(recipe_id)s, %(comment)s, %(name)s, NOW());
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_comments_by_recipe(cls, recipe_id):
        query = "SELECT * FROM comments WHERE recipe_id = %(recipe_id)s;"
        data = {'recipe_id': recipe_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        comments = []
        for result in results:
            comments.append(cls(result))
        return comments