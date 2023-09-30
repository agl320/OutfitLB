import requests

GET_URL = "https://us-east-2.aws.data.mongodb-api.com/app/data-zzkgk/endpoint/getData"

# Replace with the actual username and password
accountname = "test"
password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

response = requests.get(
    GET_URL, params={"accountname": accountname, "password": password}
)

if response.status_code == 200:
    account_data = response.json()
    print(f"Account Data for {accountname}: {account_data}")
else:
    print("Wrong account details")
    print(f"Function call failed: {response.status_code}, {response.text}")

# exports = async function(accountname) {
#   // assume password already hashed
#   const accountsCollection = context.services
#     .get("OutfitLB")
#     .db("OutfitLB")
#     .collection("Accounts_mongo");

#   const pipeline = [
#     {
#       $match: {
#         account: accountname
#       }
#     },
#     {
#       $count: "count"
#     }
#   ];

#   const result = await accountsCollection.aggregate(pipeline).toArray();

#   // Check if any documents match the criteria
#   if (result.length > 0 && result[0].count > 0) {
#     return true;
#   } else {
#     return false;
#   }

# };
