from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

class Extraction:
    def __init__(self, path: str, header: bool = True):
        self.path = path
        self.format = self.detect_format()
        self.header = header
        self.schema = None
        self.spark = SparkSession.builder.master("local[*]").appName("ETL-Extraction").getOrCreate()

    def __str__(self):
        return f'File: {self.path}, Format: {self.format}, Schema: {self.schema}, Header: {self.header}'

    def detect_format(self):
        """Detect file format based on his extension."""
        extension = self.path.split('.')[-1].lower()
        if extension in ['csv', 'json']:
            return extension
        else:
            raise ValueError(f"non supported Format  : {extension}. CSV et JSON are only supported.")

    def extract_name(self):
        """Extract file name from path."""
        return self.path.split('/')[-1].split('.')[0]
    
    def read_data(self):
        """Read the file, infere schema and return a Spark DataFrame."""
        try:
            if self.format == "csv":
                df = self.spark.read.format("csv").option("header", self.header).option("inferSchema", True).load(self.path)
            elif self.format == "json":
                df = self.spark.read.format("json").option("inferSchema", True).load(self.path)

            self.schema = df.schema
            return df
        
        except AnalysisException as e:
            print(f"Error while reading file : {e}")
            return None




