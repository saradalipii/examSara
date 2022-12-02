from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of thoughts
class Thought:
    db_name='exam' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.description = data['description'],
        self.creator_id = data['creator_id'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #Method to  query the database and 
    #get all the thoughts, together with the creator's id and email,
    # and the number of likes

    @classmethod
    def getAllthoughts(cls):
        query= 'SELECT thoughts.id, creator_id, thoughts.description, COUNT(likes.id) as likesNr, users.id as creator_id, users.first_name as first_name, users.last_name as last_name FROM thoughts LEFT JOIN users on thoughts.creator_id = users.id LEFT JOIN likes on likes.thoughts_id = thoughts.id GROUP BY thoughts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        thoughts = []
        
        # if len(results) > 0:
        for row in results:
            thoughts.append(row)
        print(len(thoughts))   
        return thoughts
        
    @classmethod
    def create_thoughts(cls,data):
        query = 'INSERT INTO thoughts (description, creator_id) VALUES ( %(description)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_thoughts_by_id(cls, data):
        query= 'SELECT * FROM thoughts WHERE thoughts.id = %(thoughts_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]


    @classmethod
    def get_user_thoughts(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        if len(thoughts) > 0:
            for row in results:
                thoughts.append(row)
        return thoughts

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (thoughts_id, users_id) VALUES ( %(thoughts_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE thoughts_id = %(thoughts_id)s and users_id = %(users_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroythoughts(cls, data):
        query= 'DELETE FROM thoughts WHERE thoughts.id = %(thoughts_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def deleteAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.thoughts_id = %(thoughts_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_thoughts(thoughts):
        is_valid = True
        if len(thoughts['description']) < 5:
            flash("Thoughts description must be at least 5 characters.", 'description')
            is_valid = False
        return is_valid