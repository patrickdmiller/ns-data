from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

HOST = os.environ.get("NSHOST") or "localhost"
PORT = os.environ.get("NSPORT") or "27017"
USERNAME = os.environ.get("NSUSER") or "nightscout"
PASSWORD = os.environ.get("NSPASSWORD") or "nightscout"
DB = os.environ.get("NSDB") or "Nightscout"

def absolute_seconds_delta(t1, t2):
  return abs((t2 - t1).total_seconds())


class Nightscout:
  def __init__(self, host=HOST, port=PORT, username=USERNAME, password=PASSWORD, db=DB):
    self.mongo_uri = 'mongodb://%s:%s@%s:%s' % (username, password, host, port)
    self.dbConnection = MongoClient(self.mongo_uri)
    self.db = self.dbConnection[DB]
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
  def align(self, entries_filter=None,  minutes=5):
    #we will go in reverse
    entries_r = self.entries.iloc[::-1]
    t = entries_r.iloc[0]['ts']
    i = 0
    counter = 0
    index = pd.date_range(start=t, freq=-timedelta(minutes=minutes), periods=500)
    df = pd.DataFrame(index=index, columns=['sgv', 'ts'])
    df.index.name = 'date'
    
    for di, row in df.iterrows():
      while i < len(self.entries)-1 and absolute_seconds_delta(entries_r.iloc[i]['ts'], di) > absolute_seconds_delta(entries_r.iloc[i+1]['ts'], di):
        i = i + 1
      if absolute_seconds_delta(t, entries_r.iloc[i]['ts']) > 240 and entries_r.iloc[i]['ts'] > di:
        i+=1
      df.loc[di] = [entries_r.iloc[i]['sgv'], entries_r.iloc[i]['ts']]
    return df
   
    
    return 
    while counter < 100:
      #which is closer
      #keep incrementing until the current delta is < next detla
      while i < len(self.entries)-1 and absolute_seconds_delta(entries_r.iloc[i]['ts'], t) > absolute_seconds_delta(entries_r.iloc[i+1]['ts'], t):
        i = i + 1
      #if the delta is > 4:30 , we're going to assume that we need the previous. this is a fill forward
      if absolute_seconds_delta(t, entries_r.iloc[i]['ts']):
        i+=1
      
      
      
      
      t = t - timedelta(minutes=minutes)
      counter+=1

      
    
    
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
  