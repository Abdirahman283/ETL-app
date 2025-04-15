from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from Extraction import Extraction
from Transformation import Transformation
from DBLoader import DBLoader
from flask import Flask, render_template, request
import psycopg2
import mysql.connector

# Stocker temporairement le DataFrame
extracted_df = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingest')
def ingest():
    return render_template('etl/extraction.html')

@app.route('/extract', methods=['POST'])
def extract():
    global extracted_df  # Important pour garder le DataFrame accessible dans d'autres routes

    file = request.files['datafile']
    fmt = request.form.get('format')

    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    # Détection du format si non précisé
    if not fmt:
        if filename.endswith(".csv"):
            fmt = "csv"
        elif filename.endswith(".json"):
            fmt = "json"
        else:
            return render_template(
                'etl/extraction.html',
                error="❌ Unsupported file format. Please upload a CSV or JSON file."
            )

    try:
        extractor = Extraction(filepath)
        df = extractor.read_data()

        if df is None:
            return "❌ Failed to read the data file", 500

        extracted_df = df  # 🔥 Stocker pour la suite (cleaning)
        df.show(5)

        return redirect('/clean')

    except Exception as e:
        return f"❌ Extraction error: {str(e)}", 500

    

@app.route('/clean', methods=['GET', 'POST'])
def clean():
    global extracted_df  # Le DataFrame extrait stocké en mémoire

    if extracted_df is None:
        return "❌ No data loaded", 400

    if request.method == 'GET':
        # Afficher les colonnes dans le formulaire
        return render_template('etl/cleaning.html', columns=extracted_df.columns)

    if request.method == 'POST':
        transformer = Transformation(extracted_df)
        selected_transforms = request.form.getlist("transforms")
        drop_cols = request.form.getlist("drop_cols")

        # Appliquer les transformations cochées
        if "null_cols" in selected_transforms:
            extracted_df = transformer.delete_null_columns()
        if "null_rows" in selected_transforms:
            extracted_df = transformer.delete_null_rows()
        if "duplicates" in selected_transforms:
            extracted_df = transformer.drop_duplicates()
        if drop_cols:
            extracted_df = transformer.drop_columns(drop_cols)

        print("✅ Cleaning done.")
        extracted_df.show(5)  # Pour debug

        return redirect('/output')

@app.route('/output')
def output():
    global extracted_df
    if extracted_df is None:
        return "❌ No cleaned data to display", 400

    return render_template("etl/output.html")

@app.route('/save_file', methods=['GET', 'POST'])
def save_file():
    global extracted_df
    if extracted_df is None:
        return "❌ No data available to save", 400

    if request.method == 'POST':
        output_format = request.form.get("format")

        if output_format not in ['csv', 'json']:
            return "❌ Unsupported format", 400

        try:
            base_path = "outputs"
            os.makedirs(base_path, exist_ok=True)

            from FileLoader import FileLoader  # Assure-toi que c’est bien importé
            f_loader = FileLoader(extracted_df, base_path)

            if output_format == 'csv':
                f_loader.generate_csv()
            else:
                f_loader.generate_json()

            return render_template(
                "etl/save_success.html",
                format=output_format,
                path=f_loader.path  # 🔥 Le vrai chemin avec sous-dossier
            )

        except Exception as e:
            return f"❌ Saving error: {str(e)}", 500

    return render_template("etl/save_file.html")


@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'GET':
        return render_template('db/connect_store.html')

    db_choice = request.form.get("db")

    if db_choice == "mysql":
        return render_template("db/mysql.html")
    elif db_choice == "postgres":
        return render_template("db/postgres.html")
    elif db_choice == "mongodb":
        return render_template("db/mongodb.html")
    else:
        return "❌ Invalid choice", 400

from DBLoader import DBLoader  # assure-toi que ce module est bien importé

@app.route("/store_mysql", methods=["POST"])
def store_mysql():
    global extracted_df

    if extracted_df is None:
        return "❌ No data to insert", 400

    creds = {
        "host": request.form["host"],
        "port": request.form["port"],
        "user": request.form["user"],
        "password": request.form["password"],
        "database": request.form["database"],
        "table_name": request.form["table"]
    }

    try:
        loader = DBLoader(extracted_df)
        loader.insert_to_mysql(creds)
        return render_template("db/store_success.html", db="MySQL")

    except Exception as e:
        return f"❌ MySQL insertion failed: {str(e)}", 500

@app.route('/store_postgres', methods=['POST'])
def store_postgres():
    if extracted_df is None:
        return "❌ No data to store", 400

    creds = {
        "host": request.form["host"],
        "port": request.form["port"],
        "user": request.form["user"],
        "password": request.form["password"],
        "database": request.form["database"],
        "table_name": request.form["table"]
    }

    try:
        loader = DBLoader(extracted_df)
        loader.insert_to_postgres(creds)
        return render_template("db/store_success.html", db="PostgreSQL")
    except Exception as e:
        return f"❌ PostgreSQL storage error: {e}", 500

@app.route('/store_mongodb', methods=['POST'])
def store_mongodb():
    if extracted_df is None:
        return "❌ No data to store", 400

    creds = {
        "host": request.form["host"],
        "port": request.form["port"],
        "user": request.form["user"],
        "password": request.form["password"],
        "database": request.form["database"],
        "table_name": request.form["table"]
    }

    try:
        loader = DBLoader(extracted_df)
        loader.insert_to_mongodb(creds)
        return render_template("db/store_success.html", db="MongoDB")
    except Exception as e:
        return f"❌ MongoDB storage error: {e}", 500

from flask import Flask, render_template, request
import psycopg2
import mysql.connector

@app.route("/explore")
def explore():
    return render_template("query/connect_query.html")


@app.route("/query", methods=["POST", "GET"])
def query():
    if request.method == "POST":
        db_type = request.form["db_type"]
        host = request.form["host"]
        port = request.form["port"]
        user = request.form["user"]
        password = request.form["password"]
        database = request.form["database"]

        try:
            if db_type == "postgres":
                conn = psycopg2.connect(
                    host=host, port=port, user=user, password=password, database=database
                )
            elif db_type == "mysql":
                conn = mysql.connector.connect(
                    host=host, port=port, user=user, password=password, database=database
                )
            else:
                return "❌ Invalid database type."

            cursor = conn.cursor()

            # Obtenir les tables disponibles
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog')")
            tables = cursor.fetchall()

            # Demander la requête SQL à exécuter (dans une nouvelle page ou directement ici)
            return render_template("query/query.html", db_type=db_type, tables=tables, creds=request.form)

        except Exception as e:
            return f"❌ Database connection failed: {str(e)}"

    return redirect("/")

from flask import jsonify

@app.route("/run_query", methods=["POST"])
def run_query():
    db_type = request.form["db_type"]
    sql_query = request.form["sql_query"]

    creds = {
        "host": request.form["host"],
        "port": request.form["port"],
        "user": request.form["user"],
        "password": request.form["password"],
        "database": request.form["database"]
    }

    try:
        # Connexion à la base de données choisie
        if db_type == "postgres":
            conn = psycopg2.connect(**creds)
        elif db_type == "mysql":
            conn = mysql.connector.connect(**creds)
        else:
            return "❌ Unsupported DB type.", 400

        cursor = conn.cursor()
        cursor.execute(sql_query)

        # Récupération des résultats s'il y en a
        try:
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        except:
            rows, columns = [], []

        conn.commit()
        conn.close()

        # Rendre la même page avec les résultats en dessous
        return render_template("query/query.html", rows=rows, columns=columns, db_type=db_type, creds=creds)

    except Exception as e:
        return f"❌ Query failed: {str(e)}", 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
