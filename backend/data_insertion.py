import os
import sys
sys.path.append('scraper')
sys.path.append('database')
from scraper.pokemon_details import get_pokemon_abilities
from database.setup import create_connection, close_connection
from database.commands import insert_data
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load environment variables from .env file
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", 3306)
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "test_db")
    print(f"Connecting to database at {host}:{port} as user {user}...")
    db_connection = create_connection(host, port, user, password, database)

    ability_tuples = get_pokemon_abilities()
    
    insert_data(db_connection, "Abilities", ability_tuples, columns=['name', 'description'])

    if db_connection:
        close_connection(db_connection)
        db_connection = None



if __name__ == "__main__":
    main()
