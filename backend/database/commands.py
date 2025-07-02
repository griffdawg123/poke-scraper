from .utils import sql_file_from_path

def get_tables(conn):
    """
    Get a list of all tables in the database.
    """
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return tables

def reset_table(conn, table_name):
    """
    Reset a specific table by truncating it.
    """
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    conn.commit()
    return f"Table {table_name} has been reset."

def setup_database(conn):
    """
    Set up the database by creating necessary tables.
    """
    cursor = conn.cursor()
    queries = None
    try:
        queries = sql_file_from_path('tables.sql')
    except FileNotFoundError:
        return "SQL setup file not found."
    print(queries)
    if not queries:
        return "No SQL queries to execute."

    for query in queries.split(';'):
        query = query.strip()
        if query:
            try:
                cursor.execute(query)
            except Exception as e:
                return f"Error executing query: {query}. Error: {e}"
    # query = """
    # CREATE TABLE IF NOT EXISTS Pokemon (
    #   id INTEGER PRIMARY KEY,
    #   name VARCHAR(255) NOT NULL
    # );
    # """
    # cursor.execute(query)
    conn.commit()
    return "Database setup completed successfully."

def drop_tables(conn):
    """
    Drop all tables in the database.
    """
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for (table_name,) in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    return "All tables have been dropped."

def insert_data(conn, table_name, data, columns=None):
    """
    Insert data into a specific table.
    """
    if not conn:
        return "No database connection established."
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(data[0]))
    if columns:
        column_names = ', '.join(columns)
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    else:
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    try:
        cursor.executemany(query, data)
        conn.commit()
        return f"Inserted {len(data)} rows into {table_name}."
    except Exception as e:
        return f"Error inserting data into {table_name}: {e}"
