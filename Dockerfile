FROM bitnami/spark:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

# Copie des scripts Python
COPY app.py Extraction.py Transformation.py FileLoader.py DBLoader.py query.py test_jdbc.py test_mysql.py main.py /app/

# Copier les templates HTML
COPY templates /app/templates

# Drivers JDBC
COPY postgresql-42.7.5.jar /opt/bitnami/spark/jars/
COPY mysql-connector-j-8.3.0.jar /opt/bitnami/spark/jars/

# Créer les dossiers d'upload/output
RUN mkdir -p /app/uploads /app/outputs

EXPOSE 5000

CMD ["python3", "main.py"]
