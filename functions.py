#standard packages
import pandas as pd
import numpy as np

#webscraping packages & SQLite
import sqlite3
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib.request

client = MongoClient()
db = client.case_files
cases = db.cases


class gather_data():
    
    def __init__(self, token, starting_url):
        self.token = token
        self.starting_url = starting_url
        
    
    @staticmethod
    def into_mongo(json):
        for i in json['results']:
            _dict = {'case_id' : i['id'], 'frontend_url': i['frontend_url'], 'case_name': i['name'], 
                      'decision_date': i['decision_date'],
                      'court_name': i['court']['name'], 
                      'court_id': i['court']['id'], 
                      'judges': i['casebody']['data']['judges'],
                      'attorneys': i['casebody']['data']['attorneys'],
                      'case_text': i['casebody']['data']['opinions']}

            x = cases.insert_one(_dict)
      
               
    def scrape(self):
        r = requests.get(f'{self.starting_url}', headers={'Authorization': f'Token {self.token}'})
        #r.status_code
        temp = r.json()
        self.into_mongo(temp)
        next_url = temp['next']
        
        
        while next_url != None:
            
            r = requests.get(f'{next_url}', headers={'Authorization': f'Token f{self.token}'})
            print(r.status_code)
            temp = r.json()
            self.into_mongo(temp)
            next_url = temp['next']
            print(next_url)
            
            
            
def clean_data(df):
    pass 
            
        
        
        
        
        
        
        
        