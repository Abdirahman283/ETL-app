from pyspark.sql import DataFrame
from Extraction import Extraction
from Transformation import Transformation

class Loading:
    def __init__(self, df: DataFrame, path: str):
        self.df = df
        self.path = path

    def __str__(self):
        return f"Chargement des données vers {self.path}"

    def generate_csv(self):
        """Sauvegarde le DataFrame sous format CSV."""
        try:
            self.df.write.format("csv").mode("overwrite").option("header", "true").save(self.path)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier CSV : {e}")
    
    def generate_json(self):
        """Sauvegarde le DataFrame sous format JSON."""
        try:
            self.df.write.format("json").mode("overwrite").save(self.path)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier JSON : {e}")

        

