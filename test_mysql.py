from pyspark.sql import SparkSession

def test_mysql_jdbc_connection():
    spark = SparkSession.builder \
        .appName("MySQL JDBC Test") \
        .getOrCreate()

    print("⏳ Testing JDBC connection to MySQL...")

    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:mysql://mysql:3306/etl_db") \
            .option("dbtable", "information_schema.tables") \
            .option("user", "root") \
            .option("password", "root") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .load()

        print("✅ JDBC connection successful. Sample data:")
        df.show(5)
    except Exception as e:
        print(f"❌ JDBC connection failed: {e}")

if __name__ == "__main__":
    test_mysql_jdbc_connection()
