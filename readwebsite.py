#The script is to generate SQLite DB for english words -
#Used http://www.mso.anu.edu.au/~ralph/OPTED/ to get all the words using requests module and BeautifulSoup
#
#DB Used - SQLite
#DB Name - entries
#Tbl Name - dictionary
#Columns -
#   id (Auto Increment)
#   word(contains the word)
#   wordtype(contains noun, verb, preposition etc)
#   definition (contains the meaning of word)

import requests
from bs4 import BeautifulSoup
import sqlite3

class ConnectToSqlite:
    conn = None
    cur = None
    success_count = 0
    error_count = 0


    def __init__(self, db):
        try:
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
            exit(1)

    def executeSelect(self,word):
        try:
            self.cur.execute("select * from dictionary where word like (?)", (word))
            return self.cur
        except Exception as exc:
            print('There was a problem: %s' % (exc))
            self.error_count += 1


    def executeQuery(self,word,word_type,definition):
        #print ("The words are %s %s %s" %(word,word_type,definition))
        try:
            self.cur.execute("insert into dictionary (word,wordtype,definition) values (?, ?,?)", (word, word_type,definition))
            self.conn.commit()
            self.success_count += 1
        except Exception as exc:
            print('There was a problem: %s' % (exc))
            self.error_count += 1

    def __del__(self):
        self.conn.close()


def processlist(input_list,new_conn):
    for item in input_list:
        word = item.b.string
        word_type = item.i.string
        definition = item.getText()[item.getText().find(')')+2:]

        new_conn.executeQuery(word,word_type,definition)



new_conn = ConnectToSqlite('/Users/tusharsaurabh/entries.db')
alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

for alphabet in alphabet_list:
    link = "http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_"+ alphabet +".html"
    res = requests.get(link)
    try:
        res.raise_for_status()
        soup = BeautifulSoup(res.text,'html.parser')
        all_words = soup.find_all('p')
        processlist(all_words,new_conn)
    except Exception as exc:
        print('There was a problem: %s' % (exc))
        exit(1)

print ("The number of successfull Entries are : %s" %(new_conn.success_count))
print ("The number of wrong Entries are : %s" %(new_conn.error_count))

del new_conn