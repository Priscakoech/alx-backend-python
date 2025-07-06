import mysql.connector
from mysql.connector import errorcode
import csv
import uuid
import os

# I'll probably make this a config later
DB_NAME = "ALX_prodev"

# Define the tables here. Only one for now
TABLES = {
    "user_data": (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id CHAR(36) NOT NULL,"
        "  name VARCHAR(255) NOT NULL,"
        "  email VARCHAR(255) NOT NULL,"
        "  age DECIMAL NOT NULL,"
        "  PRIMARY KEY (user_id),"
        "  INDEX(user_id)"
        ") ENGINE=InnoDB"
    )
}


def connect_db():
    # Initial DB connection - no database selected yet
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here"  # TODO: Use environment variables
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL server:", e)
        return None


def create_database(conn):
    # Creates the main DB if it doesn't already exist
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' is ready.")
    except mysql.connector.Error as db_err:
        print("Failed to create DB:", db_err)
    finally:
        cursor.close()


def connect_to_prodev():
    # Connects directly to the named database
    try:
        db_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",
            database=DB_NAME
        )
        return db_conn
    except mysql.connector.Error as conn_err:
        print(f"Couldn't connect to DB '{DB_NAME}':", conn_err)
        return None


def create_table(conn):
    # Just sets up the user_data table
    try:
        cur = conn.cursor()
        cur.execute(TABLES["user_data"])
        print("Table 'user_data' created or already exists.")
    except mysql.connector.Error as t_err:
        print("Table creation failed:", t_err)
    finally:
        cur.close()


def insert_data(conn, csv_path):
    # Feeds data into the user_data table from a CSV file.
    # Prevents duplicates based on email field.

    try:
        cur = conn.cursor()
        with open(csv_path, newline='') as f:
            csv_reader = csv.DictReader(f)

            for entry in csv_reader:
                # Check for existing email - no duplicates allowed
                cur.execute("SELECT user_id FROM user_data WHERE email = %s", (entry['email'],))
                exists = cur.fetchone()

                if not exists:
                    # UUID for the user ID - we use string version
                    new_id = str(uuid.uuid4())

                    cur.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (new_id, entry['name'], entry['email'], entry['age'])
                    )
                else:
                    # Skipping existing email
                    print(f"Skipping duplicate email: {entry['email']}")

        conn.commit()
        print("Data loaded into 'user_data' from CSV.")
    except Exception as load_err:
        print("Something went wrong during CSV load:", load_err)
    finally:
        cur.close()
