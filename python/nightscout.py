from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from pymongo import MongoClient

HOST = os.environ.get("NSHOST") or "localhost"
PORT = os.environ.get("NSPORT") or "27017"
USERNAME = os.environ.get("NSUSERNAME") or "nightscout"
PASSWORD = os.environ.get("NSPASSWORD") or "nightscout"
DB = os.environ.get("NSDB") or "Nightscout"



class Nightscout:
  def __init__(self, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, db=DB):
    self.mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
    self.dbConnection = MongoClient(self.mongo_uri)

  def find(self, collection="entries", query={}, limit=0):
    cursor = self.dbConnection[DB][collection].find(query).limit(limit)
    df =  pd.DataFrame(list(cursor))
    return df

if __name__ == "__main__":
  ns = Nightscout()
  print(ns.find())
  