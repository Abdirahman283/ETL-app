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
    choice = input(
    "📌 Choose the transformations to apply (separate numbers by commas):\n"
    "1. Delete null columns\n"
    "2. Delete null rows\n"
    "3. Drop duplicates\n"
    "4. Drop specific columns\n"
    "Your choice: ")
    choice = [int(i.strip()) for i in choice.split(",") if i.strip().isdigit()]
    df_transformed = df  # Initialiser avec le DataFrame d'origine
    for i in choice:
        if i == 1:
            df_transformed = transformer.delete_null_columns()
        elif i == 2:
            df_transformed = transformer.delete_null_rows()
        elif i == 3:
            df_transformed = transformer.drop_duplicates()
        elif i == 4:
            print(f"Available columns: {', '.join(df.columns)}")
            columns = input("Enter the columns you want to drop (comma separated): ").strip()
            if columns:
                columns = [col.strip() for col in columns.split(",")]
                df_transformed = transformer.drop_columns(columns)
        else:
            print(f"⚠️ Invalid choice: {i}")
    print("✅ Transformation completed!")

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