# reusable query context manager that inputs and executes it, managing both connection and query execution

import sqlite3
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
            return False
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return True
    
# Example usage
# it takes the query SELECT * FROM users WHERE age > ? and the parameter 25 and eturns the results
if __name__ == "__main__":
    with ExecuteQuery('example.db', 'SELECT * FROM users WHERE age > ?', (25,)) as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 20))
        
        cursor.execute('SELECT * FROM users WHERE age > ?', (25,))
        print(cursor.fetchall())  # Output: [(1, 'Alice', 30)]
        cursor.execute('SELECT * FROM users WHERE age <= ?', (25,))
        print(cursor.fetchall())  # Output: [(2, 'Bob', 20)]
        cursor.close()

    