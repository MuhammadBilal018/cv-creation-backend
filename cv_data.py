from pymongo import MongoClient
import json

uri = "mongodb+srv://Cv-creation:Cv-creation@cluster0.l0udf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["Cv-creation"]
collection_users = db["users"]
collection_cv_data = db["cv-data"]

def get_cv_data(user_id):
    cv_document = collection_cv_data.find_one({"user_id": user_id})
    if cv_document:
        cv_data = cv_document["cv_data"]
        # print(cv_data)
        return cv_data
    else:
        return None

def update_data(cv_json, user_id):
    existing_document = collection_cv_data.find_one({"user_id": user_id})

    if existing_document:
        collection_cv_data.update_one(
            {"user_id": user_id}, {"$set": {"cv_data": json.loads(cv_json)}}
        )
        print("CV data updated for user ID:", user_id)
        return None
    else:
        cv_data = {"user_id": user_id, "cv_data": json.loads(cv_json)}
        inserted_data = collection_cv_data.insert_one(cv_data)
        cv_id = inserted_data.inserted_id
        print("New CV data inserted with ID:", cv_id)

        return None

def update_cv_content(cv_text, user_id):
    print("Hello World")
    existing_document = collection_cv_data.find_one({"user_id": user_id})
    print("I was Lagend")
    if existing_document:
        collection_cv_data.update_one(
            {"user_id": user_id}, {"$set": {"cv_data": cv_text}}
        )
        print("CV data updated for user ID:", user_id)
        return True
    else:
        return False
