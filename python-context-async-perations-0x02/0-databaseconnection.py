#context manager for opening and closing database connections automatically using __enter__ and __exit__

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
            return False
        return True # Returning True suppresses the exception, False propagates it

# Example usage
if __name__ == "__main__": 
    with DatabaseConnection('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
        cursor.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
        conn.commit()
        
        cursor.execute('SELECT * FROM users')
        print(cursor.fetchall())  # Output: [(1, 'Alice')]
        cursor.close()
        
            
   

    