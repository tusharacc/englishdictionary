###The program is just to solve ne word puzzle that I got on whatsapp
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
            #print (word)
            self.cur.execute("select * from dictionary where word like (?)", (word,))
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


db = ConnectToSqlite('/Users/tusharsaurabh/entries.db')

word_list = ['_lb__t','G_r_','_nkn_wn','Sp__r','C_t_l_g__','_r__','_rg_n_z_t__n','_c_n_my','L_g_t_m_t_','M_b_l_']

temp_word = ""
for item in word_list:
    cursor = db.executeSelect(item)
    #print (type(cursor))
    for row in cursor:
        if (row[1] != temp_word):
            print (" The word with %s is %s"%(item,row[1]))
        temp_word = row[1]

del db