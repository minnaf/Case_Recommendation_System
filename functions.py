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

class gather_data():
    
    def __init__(self, Auth):
        self.Auth = Auth
    
    
    def into_mongo(self, json):
        for i in json['results']:
            _dict = {'case_id' : i['id'], 'frontend_url': i['frontend_url'], 'case_name': i['name'], 
                      'decision_date': i['decision_date'],
                      'court_name': i['court']['name'], 
                      'court_id': i['court']['id'], 
                      'judges': i['casebody']['data']['judges'],
                      'attorneys': i['casebody']['data']['attorneys'],
                      'majority_case_text': i['casebody']['data']['opinions'][0]['text'],
                      'dissent_case_text': None }
            x = cases.insert_one(_dict)
        
            if len(i['casebody']['data']['opinions']) > 1:
                myquery = { "dissent_case_text": None }
                newvalues = { "$set": { "dissent_case_text":  i['casebody']['data']['opinions'][1]['text']} }
                cases.update_one(myquery, newvalues)  
      
                
    def scrape(self):
        r = requests.get('https://api.case.law/v1/cases/?cite=&name_abbreviation=&jurisdiction=&reporter=&decision_date_min=2000-06-01&decision_date_max=&docket_number=&court=&court_id=&search=&full_case=true&body_format=text', headers={'Authorization': f'Token {self.Auth}'})
        #r.status_code
        temp = r.json()
        next_url = temp['next']
        
        
        while next_url != None:
            r = requests.get(f'{next_url}', headers={'Authorization': f'Token f{self.Auth}'})
            print(r.status_code)
            temp = r.json()
            self.into_mongo(temp)
            next_url = temp['next']
            print(next_url)
        
        
        
        
        
        
        
        