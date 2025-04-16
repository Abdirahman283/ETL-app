# 🔧 ETL App — Data Processing Framework with PySpark, CLI and Web UI

This project is a modular ETL (Extract, Transform, Load) application developed using PySpark and Flask. It allows users to either use a Command Line Interface (CLI) or an interactive Web UI to perform ETL tasks on CSV and JSON files. 
Data can be saved locally or inserted into a MySQL, PostgreSQL, or MongoDB database.

---

## 🚀 Features

- **Extraction** of data from CSV or JSON files
- **Transformation** operations:
  - Drop null columns
  - Drop null rows
  - Drop duplicate rows
  - Drop specific columns
- **Loading** into:
  - Local CSV or JSON files
  - PostgreSQL / MySQL / MongoDB
- **Data Exploration** (SQL queries) via CLI or Web UI
- Supports both **CLI** and **Flask Web UI**
- Dockerized environment with **docker-compose**

---

## 📁 Project Structure

ETL-app/  
├── app.py             # Main script for CLI or Flask app  
├── Extraction.py      # Extraction module  
├── Transformation.py  # Transformation module  
├── DBLoader.py # Loads to MySQL/Postgres/MongoDB  
├── FileLoader.py # Saves data to CSV/JSON  
├── query.py # SQL query CLI feature  
├── templates/ # HTML templates for Flask UI  
│       ├── index.html  
│       ├── etl/  
│       │   ├── extraction.html  
│       │   ├── cleaning.html  
│       │   ├── output.html  
│       │   ├── save_file.html  
│       │   └── save_success.html  
│       ├── db/   
│       │   ├── connect_store.html  
│       │   ├── mysql.html  
│       │   ├── postgres.html  
│       │   ├── mongodb.html  
│       │   └── store_success.html  
│       └── query/  
│           ├── connect_query.html  
│           ├── execute_query.html  
│           └── query.html  
├── Dockerfile  
├── docker-compose.yml  
└── requirements.txt 

![architecture](https://github.com/user-attachments/assets/f4fc4e98-b9e1-492e-9d2d-7beccd65b26d)
> 🛈 Logos and trademarks (e.g. Python, Spark, Docker, MySQL, PostgreSQL) used in the diagram belong to their respective owners.  
> This project is for educational/demo purposes and is not affiliated with or endorsed by any of these organizations.


---

## 🧪 How to Use

Download all files in a folder 
or 
use github to clone it into a local folder ( repository link: https://github.com/Abdirahman283/ETL-app.git)

### ✅ 1. Web Interface (Flask)



#### Run the app with Docker:

```bash
docker compose build
docker compose up
```

#### Access the UI:
Go to: http://localhost:5000

#### Copy your data file into the container:
```bash
docker cp ./your_dataset.csv etl-flash:/app/uploads/
```
#### File is stored in /app/uploads/ in the container.

### ✅ 2. Command Line Interface (CLI)
You can run the CLI app directly inside the container:

```bash
docker exec -it etl-flash bash
python3 app.py
```

Follow the prompt to:
- Select a file to ingest
- Choose transformations
- Save the result to a file or a database

### ⚠️ Notes on Spark Output

 Spark does not support saving directly into an existing file. So:

 Output paths (like /app/outputs/) must be treated as directories

Old outputs will be cleared by Spark when using mode("overwrite")

Make sure your output folder is mounted in the container:

```yaml
volumes:
  - ./outputs:/app/outputs
```
### 🔄 Supported Databases

| **Database** | **Host**                  | **Port** | **Default Container Name** |
|--------------|---------------------------|----------|-----------------------------|
| PostgreSQL   | `localhost` or `postgres` | `5432`   | `pg-etl`                    |
| MySQL        | `localhost` or `mysql`    | `3306`   | `mysql-etl`                 |
| MongoDB      | *Not containerized*       | –        | –                           |

### 🔐 Default Credentials for Docker Compose

| **DB**       | **Username** | **Password** | **Database** |
|--------------|--------------|--------------|--------------|
| PostgreSQL   | `postgres`   | `postgres`   | `etl_db`     |
| MySQL        | `etluser`    | `etlpass`    | `etl_db`     |

### 📦 Sample Docker Commands
Build the image:
```bash
docker build -t etl-flash .
```
Start the environment:
```bash
docker compose up -d
```
Access the app container:
```bash
docker exec -it etl-flash bash
```

## 🛡 License & Disclaimer

This project is provided under the MIT License and is intended for educational and personal use.

It uses open-source technologies such as Apache Spark, Python, Flask, PostgreSQL, MySQL, and Docker. All trademarks and logos remain the property of their respective owners.

This project is **not affiliated with** or endorsed by the Apache Software Foundation, the Python Software Foundation, Oracle/MySQL, or Docker Inc.

The icons and diagrams included are for illustrative purposes only and should not be interpreted as official branding.

Use at your own discretion.
 
👨‍💻 Author
Abdirahman

