import mysql.connector
import psycopg2

def get_user_choice(prompt, choices):
    while True:
        print(prompt)
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        try:
            index = int(input("Your Choice: "))
            if 1 <= index <= len(choices):
                return index
        except ValueError:
            pass
        print("❌ Invalid choice. Please try again.\n")

def query_postgres():
    creds = {
        "host": input("Host (default: postgres): ") or "postgres",
        "port": input("Port (default: 5432): ") or "5432",
        "user": input("Username (default: postgres): ") or "postgres",
        "password": input("Password (default: postgres): ") or "postgres",
        "database": input("Database name (default: etl_db): ") or "etl_db"
    }

    try:
        conn = psycopg2.connect(**creds)
        cursor = conn.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables 
                          WHERE table_schema = 'public';""")
        tables = cursor.fetchall()
        if not tables:
            print("No tables found.")
            return
        print("Available tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")

        while True:
            query = input("Enter your SQL query (or 'stop' to exit): ")
            if query.lower() == "stop":
                break
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except Exception as e:
                print(f"❌ Query error: {e}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL connection error: {e}")

def query_mysql():
    creds = {
        "host": input("Host (default: mysql): ") or "mysql",
        "port": input("Port (default: 3306): ") or "3306",
        "user": input("Username (default: etluser): ") or "etluser",
        "password": input("Password (default: etlpass): ") or "etlpass",
        "database": input("Database name (default: etl_db): ") or "etl_db"
    }

    try:
        conn = mysql.connector.connect(**creds)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        if not tables:
            print("No tables found.")
            return
        print("Available tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")

        while True:
            query = input("Enter your SQL query (or 'stop' to exit): ")
            if query.lower() == "stop":
                break
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except Exception as e:
                print(f"❌ Query error: {e}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ MySQL connection error: {e}")

def explore_data():
    db_choice = get_user_choice("Which database would you like to explore?", ["PostgreSQL", "MySQL"])
    if db_choice == 1:
        query_postgres()
    else:
        query_mysql()
