import mysql.connector
import psycopg2
from pymongo import MongoClient

class DBLoader:
    def __init__(self, df):
        # Initialize with Spark DataFrame
        self.df = df

    def get_credentials(self):
        """Ask user to provide their credentials to connect to the desired database."""
        creds = {
            "host": input("Server (default: localhost): ").strip() or "localhost",
            "port": input("Port: ").strip(),
            "user": input("Username: ").strip(),
            "password": input("Password: ").strip(),
            "database": input("Database name: ").strip(),
            "table_name": input("Table name: ").strip()
        }
        return creds

    def insert_to_mysql(self, creds):
        try:
            conn = mysql.connector.connect(
                host=creds["host"],
                user=creds["user"],
                password=creds["password"],
                database=creds["database"],
                port=creds["port"]
            )
            print("✅ Successfully connected to MySQL")
            self.df.write.format("jdbc").options(
                url=f"jdbc:mysql://{creds['host']}:{creds['port']}/{creds['database']}",
                driver="com.mysql.cj.jdbc.Driver",
                dbtable=creds["table_name"],
                user=creds["user"],
                password=creds["password"]
            ).mode("append").save()
            print("✅ Data inserted into MySQL")
            conn.close()
        except Exception as e:
            print(f"❌ MySQL error: {e}")

    def insert_to_postgres(self, creds):
        try:
            conn = psycopg2.connect(
                host=creds["host"],
                port=creds["port"],
                user=creds["user"],
                password=creds["password"],
                database=creds["database"]
            )
            print("✅ Successfully connected to PostgreSQL")
            self.df.write.format("jdbc").options(
                url=f"jdbc:postgresql://{creds['host']}:{creds['port']}/{creds['database']}",
                driver="org.postgresql.Driver",
                dbtable=creds["table_name"],
                user=creds["user"],
                password=creds["password"]
            ).mode("append").save()
            print("✅ Data inserted into PostgreSQL")
            conn.close()
        except Exception as e:
            print(f"❌ PostgreSQL error: {e}")

    def insert_to_mongodb(self, creds):
        try:
            if creds["user"] and creds["password"]:
                uri = f"mongodb://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
            else:
                uri = f"mongodb://{creds['host']}:{creds['port']}/"

            client = MongoClient(uri)
            print("✅ Successfully connected to MongoDB")
            db = client[creds["database"]]
            collection = db[creds["table_name"]]
            # Convert Spark DataFrame to Pandas DataFrame for insertion
            pandas_df = self.df.toPandas()
            collection.insert_many(pandas_df.to_dict("records"))
            print("✅ Data inserted into MongoDB")
            client.close()
        except Exception as e:
            print(f"❌ MongoDB error: {e}")
