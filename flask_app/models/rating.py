from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app


class Rating:

#     DB = "share_a_taste"

#     def __init__(self, data):
#         self.id = data['id']
#         self.user_id = data['user_id']
#         self.recipe_id = data['recipe_id']
#         self.rating = data['rating']
#         self.created_at = data['created_at']
#         self.updated_at = data['updated_at']

#     @staticmethod
#     def validate_rating(rating):
#         is_valid = True
#         try:
#             rating_value = int(rating['rating'])
#             if not 1 <= rating_value <= 5:
#                 flash("Rating must be between 1 and 5.")
#                 is_valid = False
#         except ValueError:
#             flash("Invalid rating value.")
#             is_valid = False
#         return is_valid


#     @classmethod
#     def save(cls, data):
#         query = """
#             INSERT INTO ratings (user_id, recipe_id, rating, created_at)
#             VALUES (%(user_id)s, %(recipe_id)s, %(rating)s, NOW());
#         """
#         result = connectToMySQL(cls.DB).query_db(query, data)
#         return result

#     @classmethod
#     def get_ratings_by_recipe(cls, recipe_id):
#         query = "SELECT * FROM ratings WHERE recipe_id = %(recipe_id)s;"
#         data = {'recipe_id': recipe_id}
#         results = connectToMySQL(cls.DB).query_db(query, data)
#         ratings = []
#         for result in results:
#             ratings.append(cls(result))
#         return ratings



    DB = "share_a_taste"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.recipe_id = data['recipe_id']
        self.rating = data['rating']
        self.created_at = data['created_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO ratings (user_id, recipe_id, rating, created_at)
            VALUES (%(user_id)s, %(recipe_id)s, %(rating)s, NOW());
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_ratings_by_recipe(cls, recipe_id):
        query = "SELECT * FROM ratings WHERE recipe_id = %(recipe_id)s;"
        data = {'recipe_id': recipe_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        ratings = []
        for result in results:
            ratings.append(cls(result))
        return ratings

    @classmethod
    def validate_rating(rating_data):
        is_valid = True
        try:
            rating_value = int(rating_data['rating'])
            if not 1 <= rating_value <= 5:
                flash("Rating must be between 1 and 5.")
                is_valid = False
        except (ValueError, TypeError):
            flash("Invalid rating value.")
            is_valid = False
        return is_valid
