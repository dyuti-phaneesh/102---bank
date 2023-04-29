import mysql. connector

connection = mysql.connector.connect(
    user = 'c2cuser',
    database = 'c2c 1',
    password = 'passw0rd'
)

cursor = connection.cursor()

testQuery = ("SELECT * FROM students")
cursor.execute(testQuery)

for item in cursor:
    print(item)

cursor.close()
connection.close()