import os
from Extraction import Extraction
from Transformation import Transformation
from DBLoader import DBLoader
from FileLoader import FileLoader

def main():
    # Step 1: Get the input file path
    file_path = input("📂 Enter the CSV/JSON file path: ").strip()

    # Verify if the file exists
    if not os.path.exists(file_path):
        print("❌ File not found. Please check the path.")
        return

    # Step 2: Extraction
    extractor = Extraction(file_path)
    df = extractor.read_data()

    if df is None:
        print("❌ Data extraction failed.")
        return
    print("✅ Extraction completed!")

    # Step 3: Transformation
    transformer = Transformation(df)
    
    # Apply transformations based on user input
    choice = input(
    "📌 Choose the transformations to apply (separate numbers by commas):\n"
    "1. Delete null columns\n"
    "2. Delete null rows\n"
    "3. Drop duplicates\n"
    "4. Drop specific columns\n"
    "Your choice: ")
    choice = [int(i.strip()) for i in choice.split(",") if i.strip().isdigit()]
    df_transformed = df  # Initialize with the original DataFrame
    
    for i in choice:
        if i == 1:
            df_transformed = transformer.delete_null_columns()
        elif i == 2:
            df_transformed = transformer.delete_null_rows()
        elif i == 3:
            df_transformed = transformer.drop_duplicates()
        elif i == 4:
            print(f"Available columns: {', '.join(df.columns)}")
            columns = input("Enter the columns to drop (comma separated): ").strip()
            if columns:
                columns = [col.strip() for col in columns.split(",")]
                df_transformed = transformer.drop_columns(columns)
        else:
            print(f"⚠️ Invalid choice: {i}")
    print("✅ Transformation completed!")

    # Step 4: Saving the data
    # Ask user how to save the result
    choix = input("How would you like to save the outcome: \n"
                  "1. Generate a file (CSV or JSON) \n"
                  "2. Save into a database \n"
                  "Your Choice: ").strip()

    if choix == "1":
        # Request file format and output path
        output_format = input("📁 Output format (csv/json): ").strip().lower()
        output_path = input("📂 Provide the output folder path: ").strip()
        
        if output_format not in ["csv", "json"]:
            print("❌ Unsupported format.")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        f_loader = FileLoader(df_transformed, output_path)
        if output_format == "csv":
            f_loader.generate_csv()
            print(f"✅ Data saved as CSV in {output_path}")
        else:
            f_loader.generate_json()
            print(f"✅ Data saved as JSON in {output_path}")

    elif choix == "2":
        db_loader = DBLoader(df_transformed)
        print("🔑 Please provide your database credentials")
        credentials = db_loader.get_credentials()

        db_choice = input("Which database would you like to save your data into?\n"
                          "1. MySQL\n"
                          "2. PostgreSQL\n"
                          "3. MongoDB\n"
                          "Your Choice: ").strip()

        if db_choice == "1":
            db_loader.insert_to_mysql(credentials)
        elif db_choice == "2":
            db_loader.insert_to_postgres(credentials)
        elif db_choice == "3":
            db_loader.insert_to_mongodb(credentials)  # Missing call added
        else:
            print("⚠️ Invalid database choice.")

if __name__ == "__main__":
    main()
