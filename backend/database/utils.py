import os

def sql_file_from_path(path):
    """Read SQL file from the given path and return its content."""
    filepath = os.path.join(os.path.dirname(__file__), path)
    print(filepath)
    try:
        with open(filepath, 'r') as file:
            sql_content = file.read()
        print(f"SQL file read successfully from {filepath}")
        return sql_content
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
