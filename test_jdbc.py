from pyspark.sql import SparkSession

def test_postgres_jdbc_connection():
    spark = SparkSession.builder \
        .appName("PostgreSQL JDBC Test") \
        .getOrCreate()

    print("⏳ Testing JDBC connection to PostgreSQL...")

    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/etl_db") \
            .option("dbtable", "information_schema.tables") \
            .option("user", "postgres") \
            .option("password", "postgres") \
            .option("driver", "org.postgresql.Driver") \
            .load()

        print("✅ JDBC connection successful. Sample data:")
        df.show(5)
    except Exception as e:
        print(f"❌ JDBC connection failed: {e}")

if __name__ == "__main__":
    test_postgres_jdbc_connection()
