import os
from Extraction import Extraction
from Transformation import Transformation
from Loading import Loading

def main():
    # Demander le chemin du fichier d'entrée
    file_path = input("📂 Entrez le chemin du fichier CSV/JSON : ").strip()

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print("❌ Fichier introuvable. Vérifiez le chemin.")
        return

    # Étape 1 : Extraction
    extractor = Extraction(file_path)
    df = extractor.read_data()

    if df is None:
        print("❌ Échec de l'extraction des données.")
        return
    print("✅ Extraction réussie !")

    # Étape 2 : Transformation
    transformer = Transformation(df)
    
    # Appliquer les transformations
    df_transformed = transformer.delete_null_columns()
    df_transformed = transformer.delete_null_rows()
    df_transformed = transformer.drop_duplicates()
    print("✅ Transformation réussie !")

    # Étape 3 : Sauvegarde
    output_format = input("📁 Format de sortie (csv/json) : ").strip().lower()
    output_path = input("Provide the output path:  ")
    
    if output_format not in ["csv", "json"]:
        print("❌ Format non supporté.")
        return

    # Vérifier et créer le dossier de sortie si nécessaire
    os.makedirs(output_path, exist_ok=True)

    loader = Loading(df_transformed, output_path)
    if output_format == "csv":
        loader.generate_csv()
        print(f"✅ Données sauvegardées en CSV dans {output_path}")
    else:
        loader.generate_json()
        print(f"✅ Données sauvegardées en JSON dans {output_path}")

if __name__ == "__main__":
    main()