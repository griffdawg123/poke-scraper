import mysql.connector
import os
from dotenv import load_dotenv

def create_connection(host, port, user, password, database):
    """Create a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Connection to MySQL DB successful")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_connection(conn):
    """Close the connection to the MySQL database."""
    if conn:
        conn.close()
        print("Connection closed")

def create_tables(conn):
    """Create tables in the database if they do not exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    print("Tables created successfully")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", 3306)
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "test_db")

    conn = create_connection(host, port, user, password, database)
    if conn:
        try:
            # Example usage of the connection
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            for table in cursor.fetchall():
                print(table)
        finally:
            close_connection(conn)




