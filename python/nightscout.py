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
    self._devicestatus = None
  
  def get_entries(self, force=False):
    if force or self._entries is None:
      print('!cache miss, fetching from db')
      self._entries = self.find("entries")
      self._entries['ts'] = pd.to_datetime(self._entries['dateString']) 
      self._entries = self._entries.sort_values(by=['ts']).reset_index(drop=True)
    return self._entries
  
  def get_treatments(self, force=False):
    if force or self._treatments is None:
      print('!cache miss, fetching from db')
      self._treatments = self.find("treatments")#.sort_values(by=['dateString']).reset_index(drop=True)
      self._treatments['ts'] = pd.to_datetime(self._treatments['created_at']) 
      self._treatments = self._treatments.sort_values(by=['ts']).reset_index(drop=True)
    return self._treatments
  
  def get_devicestatus(self, force=False):
    if force or self._devicestatus is None:
      print('!cache miss, fetching from db')
      self._devicestatus = self.find("devicestatus")
  
  entries = property(get_entries)
  treatments = property(get_treatments)
  devicestatus = property(get_devicestatus)
  def align(self, minutes=5):
    pe, te = 0,0
    aligned_entries = []
    while pe < len(self.entries):
      entry = self.entries.iloc[pe]
      if 'sgv' in entry:
        print(entry['date'], entry['sgv'])
      
      pe+=1
      if pe > 10:
        break
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
  