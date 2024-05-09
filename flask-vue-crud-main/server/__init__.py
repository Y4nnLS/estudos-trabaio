import sqlite3
 
# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('C:/Users/Ebenezer/Desktop/estudar/estudos/flask-vue-crud-main/server/jogo.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Creating table
table = '''CREATE TABLE IF NOT EXISTS jogo
                    
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL, empresa TEXT NOT NULL, jogou BOOLEAN)'''
 
cursor_obj.execute(table)
 
print("Table is Ready")
 
# Close the connection
connection_obj.close()