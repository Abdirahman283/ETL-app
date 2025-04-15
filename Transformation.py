from Extraction import Extraction
from pyspark.sql import SparkSession

class Transformation:
    def __init__(self, df):
        self.df = df


    def __str__(self):
        return "Transformation du DataFrame"

    def delete_null_columns(self):
        # Supprimer les colonnes dont toutes les valeurs sont nulles
        return self.df.select([col for col in self.df.columns if self.df.filter(self.df[col].isNotNull()).count() > 0])


    def delete_null_rows(self):
        """Supprime les lignes contenant uniquement des valeurs nulles."""
        return self.df.dropna(how="all")
    
    def drop_columns(self, columns: list):
        """Supprime les colonnes spécifiées."""
        return self.df.drop(*columns)

    
    def drop_duplicates(self):
        """Supprime les lignes dupliquées."""
        return self.df.dropDuplicates()

