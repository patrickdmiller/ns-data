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
    self._entries = None
    self._treatments = None
  
  
  def get_entries(self, force=False):
    if force or self._entries is None:
      print('!cache miss, fetching from db')
      self._entries = self.find("entries")
    return self._entries
  
  def get_treatments(self, force=False):
    if force or self._treatments is None:
      print('!cache miss, fetching from db')
      self._treatments = self.find("treatments")
    return self._treatments
  
  entries = property(get_entries)
  treatments = property(get_treatments)
  
  def align(self, minutes=5):
    pass
    

  #return all rows of collection > more for debugging.
  def find(self, collection="entries", query={}, limit=0):
    cursor = self.dbConnection[DB][collection].find(query).limit(limit)
    df =  pd.DataFrame(list(cursor))
    return df

  # build function for each collection, wrapper that calls find
  #entries
  #treatments
  


if __name__ == "__main__":
  ns = Nightscout()
  print(ns.find())
  