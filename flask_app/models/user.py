from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db_name='exam'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name']
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def getAllUsers(cls):
        query= 'SELECT * FROM users;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        users= []
        if len(results) > 0:
            for row in results:
                users.append(row)
        return users
    
    @classmethod
    def get_user_by_id(cls, data):
        query= 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
        
    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
        

    @classmethod
    def get_all_user_info(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.creator_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        if len(results) > 0:
            for row in results:
                thoughts.append(row)
        return thoughts
    
    #Class Method to create a user
    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users (email, first_name, last_name, password) VALUES ( %(email)s, %(first_name)s, %(last_name)s, %(password)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_logged_user_liked_thoughts(cls, data):
        query = 'SELECT thoughts_id as id FROM likes LEFT JOIN users on users.id = likes.users_id WHERE likes.users_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        thoughtsLiked = []
        if len(results) > 0:
            for row in results:
                thoughtsLiked.append(row['id'])
        return thoughtsLiked

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name be at least 2 characters.", 'last_name')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'password')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid
    
