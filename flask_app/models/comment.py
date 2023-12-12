from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

class Comment:

    DB = "share_a_taste"

    def __init__(self, data):
        self.id = data['id']
        self.User_id = data['User_id']
        self.Recipe_id = data['Recipe_id']
        self.comment = data['comment']
        self.name = data['name']
        self.created_at = data['created_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comments (user_id, recipe_id, comment, name, created_at)
            VALUES (%(user_id)s, %(recipe_id)s, %(comment)s, %(name)s, NOW());
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_comments_by_recipe(cls, recipe_id):
        query = "SELECT * FROM comments WHERE recipe_id = %(recipe_id)s;"
        data = {'recipe_id': recipe_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        comments = []
        for result in results:
            comments.append(cls(result))
        return comments
    
    @classmethod
    def validate_comment(comment_data):
        is_valid = True
        if len(comment_data['comment'].strip()) == 0:
            is_valid = False
            flash("Comment cannot be empty.")
        return is_valid

    @classmethod
    def get_by_id(cls, comment_id):
        query = "SELECT * FROM comments WHERE id = %(comment_id)s;"
        data = {'comment_id': comment_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def update(cls, data):
        query = """
            UPDATE comments
            SET comment = %(comment)s
            WHERE id = %(comment_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, comment_id):
        query = "DELETE FROM comments WHERE id = %(comment_id)s;"
        data = {'comment_id': comment_id}
        return connectToMySQL(cls.DB).query_db(query, data)