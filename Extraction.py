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
    
    def read_data(self, encoding="utf-8"):
        """Read the file, infer schema and return a Spark DataFrame."""
        try:
            if self.format == "csv":
                df = self.spark.read.format("csv") \
                    .option("header", self.header) \
                    .option("inferSchema", True) \
                    .option("encoding", encoding) \
                    .load(self.path)
            elif self.format == "json":
                df = self.spark.read.format("json") \
                    .option("inferSchema", True) \
                    .load(self.path)
            else:
                raise ValueError("Unsupported file format.")

            self.schema = df.schema
            return df

        except AnalysisException as e:
            print(f"❌ Spark AnalysisException while reading file: {e}")
        except UnicodeDecodeError as e:
            print(f"❌ Unicode error: {e} — try another encoding (e.g., 'ISO-8859-1').")
        except Exception as e:
            print(f"❌ General error while reading file: {e}")

        return None




