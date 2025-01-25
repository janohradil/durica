from pymongo import MongoClient
from dotenv import dotenv_values
# from decouple import config

config = dotenv_values(".env")

client = MongoClient(f"mongodb+srv://{config["DB_USER"]}:"
                     f"{config["DB_PASSWORD"]}@{config["DB_HOST"]}/"
                     f"jan?retryWrites=true&w=majority")

db = client.durica
 
collection_name = db.vyrobky

