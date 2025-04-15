import os
import datetime
from pyspark.sql import DataFrame

class FileLoader:
    def __init__(self, df: DataFrame, base_path: str):
        """
        Initialize with a Spark DataFrame and a base output path.
        A subfolder will be auto-generated to avoid Spark overwrite issues.
        """
        self.df = df
        self.base_path = base_path
        self.path = self._generate_unique_path()

    def _generate_unique_path(self):
        """Generate a subfolder with timestamp to avoid Spark overwrite issues."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        subfolder = f"output_{timestamp}"
        return os.path.join(self.base_path, subfolder)

    def __str__(self):
        return f"Loading data to {self.path}"

    def generate_csv(self):
        """Save DataFrame as CSV file."""
        try:
            self.df.write.format("csv").mode("overwrite").option("header", "true").save(self.path)
            print(f"✅ CSV saved successfully to {self.path}")
        except Exception as e:
            print(f"❌ Error while saving CSV file: {e}")

    def generate_json(self):
        """Save DataFrame as JSON file."""
        try:
            self.df.write.format("json").mode("overwrite").save(self.path)
            print(f"✅ JSON saved successfully to {self.path}")
        except Exception as e:
            print(f"❌ Error while saving JSON file: {e}")
