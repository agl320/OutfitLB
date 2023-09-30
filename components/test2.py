from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
import json

# uri = "mongodb+srv://admin:nKzVUgEw8vA8wg2g@cluster0.yplfxh7.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
# # server_api=ServerApi("1"), tlsCAFile=ca
# client = MongoClient(uri)

# db = client["OutfitLB"]
# collection = db["Accounts_mongo"]

# data = {
#     "account": "test2",
#     "password": "asdkalsdjask",
#     "data": [],
# }
# collection.insert_one(data)

####


class DBMaster:
    def __init__(self):
        pass

    def getData(self):
        GET_URL = (
            "https://us-east-2.aws.data.mongodb-api.com/app/data-tlmse/endpoint/getData"
        )

        accountname = "test"
        password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

        response = requests.get(
            GET_URL, params={"accountname": accountname, "password": password}
        )

        if response.status_code == 200:
            account_data = response.json()
            print(f"Account Data for {accountname}: {account_data}")
        else:
            print(f"Function call failed: {response.status_code}, {response.text}")

        return account_data

    def userExists(self, accountname):
        GET_URL = "https://us-east-2.aws.data.mongodb-api.com/app/data-tlmse/endpoint/userExists"

        # accountname = "test"

        response = requests.get(GET_URL, params={"accountname": accountname})

        if response.status_code == 200:
            exists = response.json()
            print(exists)
        else:
            print(f"Function call failed: {response.status_code}, {response.text}")


def main():
    db = DBMaster()
    db.insertData("test3", "hashed_pw", [1, 2, 3])


if __name__ == "__main__":
    main()
