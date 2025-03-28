import mysql.connector
import psycopg2
from pymongo import MongoClient

class DBLoader:
    def __init__(self, df):
        # Initialize with Spark DataFrame
        self.df = df

    def store_to_db(self, choice: int):
        """Store DataFrame to the selected database."""
        creds = {
            "host": input("Server (default: localhost): ").strip() or "localhost",
            "port": input("Port: ").strip(),
            "user": input("Username: ").strip(),
            "password": input("Password: ").strip(),
            "database": input("Database name: ").strip()
        }

        try:
            if choice == 1:  # MySQL
                # Connect to MySQL
                conn = mysql.connector.connect(
                    host=creds["host"],
                    user=creds["user"],
                    password=creds["password"],
                    database=creds["database"],
                    port=creds["port"]
                )
                print("Successfully connected to MySQL")
                conn.close()

            elif choice == 2:  # PostgreSQL
                # Connect to PostgreSQL
                conn = psycopg2.connect(
                    host=creds["host"],
                    port=creds["port"],
                    user=creds["user"],
                    password=creds["password"],
                    database=creds["database"]
                )
                print("Successfully connected to PostgreSQL")
                conn.close()

            elif choice == 3:  # MongoDB
                # Connect to MongoDB
                if creds["user"] and creds["password"]:
                    # Authentication required
                    uri = f"mongodb://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
                else:
                    # No authentication
                    uri = f"mongodb://{creds['host']}:{creds['port']}/"

                client = MongoClient(uri)
                print("Successfully connected to MongoDB")
                client.close()

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Connection error: {e}")
