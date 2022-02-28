import sqlite3

con = sqlite3.connect('patterns.sqlite')
cur = con.cursor()
with open('create_db.sql') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
