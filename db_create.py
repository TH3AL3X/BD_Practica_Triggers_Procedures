import sqlite3, mariadb, pymysql, db.config

connie = mariadb.connect(host="localhost",
                port=3306,
                user="root",
                password="usuario",
                database="student")
c = connie.cursor()

with open('mariadb.sql', 'r') as sql_file:
     sql_script = sql_file.read()

c.execute(sql_script)

connie.commit()
connie.close()