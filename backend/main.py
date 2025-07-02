from flask import Flask
import os
import sys
sys.path.append('database')
from database.setup import create_connection, close_connection
from database.commands import get_tables, setup_database, drop_tables
import logging

app = Flask(__name__)
db_connection = None

# Ensure the database connection is established when the app starts
def before_first_request():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", 3306)
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "test_db")
    global db_connection
    db_connection = create_connection(host, port, user, password, database)

# Ensure the database connection is closed when the app stops
def teardown_db_connection():
    global db_connection
    if db_connection:
        close_connection(db_connection)
        db_connection = None

@app.route('/')
def hello_world():
    return 'Hello, World! This is a Flask app running in a Docker container.'

@app.route('/health')
def health_check():
    """Health check endpoint to verify if the app is running."""
    return 'OK', 200

@app.route('/db_status')
def db_status():
    """Endpoint to check the database connection status."""
    if db_connection:
        return 'Database connection is active.', 200
    else:
        return 'Database connection is not established.', 500

@app.route('/tables')
def get_tables_route():
    """Endpoint to get a list of all tables in the database."""
    if db_connection:
        tables = get_tables(db_connection)
        return {'tables': tables}, 200
    else:
        return 'Database connection is not established.', 500

@app.route('/setup')
def setup_database_route():
    """Endpoint to set up the database by creating necessary tables."""
    if db_connection:
        try:
            return setup_database(db_connection)
        except Exception as e:
            return f'Error during database setup: {str(e)}', 500
    else:
        return 'Database connection is not established.', 500

@app.route('/reset')
def reset_database_route():
    """Endpoint to reset the database by dropping all tables."""
    if db_connection:
        try:
            drop_tables(db_connection)
            return 'All tables have been dropped successfully.', 200
        except Exception as e:
            return f'Error during database reset: {str(e)}', 500
    else:
        return 'Database connection is not established.', 500

@app.route('/pokemon')
def get_pokemon():
    """Endpoint to get a list of Pokémon."""
    if db_connection:
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM Pokemon")
            pokemon_list = cursor.fetchall()
            return {'pokemon': pokemon_list}, 200
        except Exception as e:
            return f'Error fetching Pokémon: {str(e)}', 500
    else:
        return 'Database connection is not established.', 500

@app.route('/tables/<table_name>')
def read_table(table_name):
    """Endpoint to read a specific table."""
    if db_connection:
        try:
            cursor = db_connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return {'rows': rows}, 200
        except Exception as e:
            return f'Error reading table {table_name}: {str(e)}', 500
    else:
        return 'Database connection is not established.', 500

if __name__ == '__main__':

    before_first_request()

    host = os.getenv("SERVER_HOST", "8000")
    port = int(os.getenv("SERVER_PORT", 5000))
    app.run(host=host, port=port, debug=True)

    teardown_db_connection()
