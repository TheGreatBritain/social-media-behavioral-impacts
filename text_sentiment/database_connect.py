import MySQLdb
db = MySQLdb.connect(host="tethys",user="satyasiv",passwd="ChangeMe",db="cse611e_db")
cur = db.cursor()

cur.execute("show tables;")

for row in cur.fetchall():
    print (row[0])

db.close()
