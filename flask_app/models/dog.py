from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Dog:
    db = "dog_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.breed = data["breed"]
        self.name = data["name"]
        self.age = data["age"]
        self.description = data["description"]
        self.user_id = data["users_id"]
        self.creator = None



    @classmethod
    def get_all(cls):
        query =  "SELECT * FROM dogs;"
        results = connectToMySQL(cls.db).query_db(query)
        all_dogs = []
        for row in results:
            print(row)
            all_dogs.append(cls(row))
        return all_dogs


    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO dogs(breed, name, age, description, users_id) VALUES (%(breed)s,%(name)s,%(age)s,%(description)s,%(users_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM dogs LEFT JOIN users ON users.id = dogs.users_id WHERE dogs.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            row = results[0]
            dog_data = {
                "id": row["id"],
                "breed": row["breed"],
                "name": row["name"],
                "age": row["age"],
                "description": row["description"],
                "users_id": row["users_id"]
            }
            one_dog = cls(dog_data)

            user_data = {
                "id": row["users_id"],  # Use the correct user ID from row["users_id"]
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            one_dog.creator = user.User(user_data)
            return one_dog
        else:
            return None



    
    @classmethod
    def update (cls, data):
        query = "Update dogs SET breed=%(breed)s, name=%(name)s, age=%(age)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM dogs WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)



    
    @staticmethod
    def is_valid(dog):
        is_valid = True
        if len(dog["breed"]) < 1:
            flash("breed must be at least 1 characters")
            is_valid = False
        if len(dog["name"]) < 1:
            flash("dog name must be at least 1 characters")
            is_valid = False
        if len(dog["age"]) < 1:
            flash("age must be at least 1 characters")
            is_valid = False
        if len(dog["description"]) <10:
            flash("dog description must be at least 10 characters")
            is_valid = False
        return is_valid
