from pyspark.sql import DataFrame

class FileLoader:
    def __init__(self, df: DataFrame, path: str):
        # Initialize with Spark DataFrame and output path
        self.df = df
        self.path = path

    def __str__(self):
        return f"Loading data to {self.path}"

    def generate_csv(self):
        """Save DataFrame as CSV file."""
        try:
            self.df.write.format("csv").mode("overwrite").option("header", "true").save(self.path)
            print(f"CSV saved successfully to {self.path}")
        except Exception as e:
            print(f"Error while saving CSV file: {e}")

    def generate_json(self):
        """Save DataFrame as JSON file."""
        try:
            self.df.write.format("json").mode("overwrite").save(self.path)
            print(f"JSON saved successfully to {self.path}")
        except Exception as e:
            print(f"Error while saving JSON file: {e}")
