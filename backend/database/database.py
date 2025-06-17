import mysql.connector

conn = mysql.connector.connect(
    host="localhost",     # or 'db' if running inside another container in the same compose network
    port=3306,
    user="testuser",
    password="testpass",
    database="testdb"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS example (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
cursor.execute("INSERT INTO example (name) VALUES (%s)", ("Alice",))
conn.commit()

cursor.execute("SELECT * FROM example")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()

