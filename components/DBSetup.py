from pymongo import MongoClient
from pymongo.server_api import ServerApi

# import certifi


class DBSetup:
    def __init__(self):
        # allow for local users and importing single user from online

        # # connecting to mongodb instance (in this case localhost)
        # # otherwise, would require us to find the address
        # client = MongoClient("localhost", 27017)
        # # accessing user databse
        # db = client.userdb
        # users = db.users

        """
        VERY POOR IMPLEMENTATION FOR LOGIN SYSTEM
        - DID NOT USE SCHEMA FOR USERS
        """

        # ca = certifi.where()
        uri = "mongodb+srv://admin:nKzVUgEw8vA8wg2g@outfitlb.avl83kc.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

        # Create a new client and connect to the server
        # server_api=ServerApi("1"), tlsCAFile=ca
        self.client = MongoClient(uri)

        self.db = self.client["OutfitLB"]
        self.collection = self.db["Accounts_mongo"]

    def getCollection(self):
        return self.collection

    # uploading data back to database
    def insert(self, data):
        self.collection.insert_one(data)

    def update(self, authenU, data):
        self.collection.update_one({"account": authenU}, {"$push": {"data": data}})
        print("[>>>] Uploaded successfully")

    def quit(self):
        self.client.close()
