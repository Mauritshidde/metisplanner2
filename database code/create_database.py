import mysql.connector as mysql

conn = mysql.connect(
   host=HOST, database=DATABASE, user=USER, password=PASSWORD
)
c = conn.cursor()

sql ='''CREATE TABLE dataUitExcel(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
type TEXT,
waarde TEXT,
klas TEXT,
vak TEXT,
week_nummer INT
)'''

sql2 ='''CREATE TABLE datums(
   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   datum TEXT,
   week INT
)'''
sql3 ='''CREATE TABLE weken(
   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   week INT
)'''


sql4 ='''CREATE TABLE vakken(
   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   vak TEXT,
   klas TEXT
)'''

sql5 ='''CREATE TABLE belangrijk(
   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   data TEXT,
   klas TEXT,
   week INT
)'''



c.execute(sql)
c.execute(sql2)
c.execute(sql3)
c.execute(sql4)
c.execute(sql5)

conn.close()
