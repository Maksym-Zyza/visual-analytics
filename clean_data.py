import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    print(f"Loading data from {input_file}...")
    df = pd.read_excel(input_file, sheet_name="Data")
    
    initial_rows = len(df)
    print(f"Initial row count: {initial_rows}")
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    print(f"Removed duplicates. Row count: {len(df)}")
    
    # 2. Handle completely empty columns or mostly empty columns
    if 'Number' in df.columns:
        df = df.drop(columns=['Number'])
    if 'Column1' in df.columns:
        df = df.drop(columns=['Column1'])
    print("Dropped mostly empty columns ('Number', 'Column1').")

    # 3. Drop rows missing essential identifiers
    essential_cols = ['Order ID', 'Date']
    df = df.dropna(subset=[col for col in essential_cols if col in df.columns])
    print(f"Dropped rows missing Order ID or Date. Row count: {len(df)}")

    # 4. Fill or drop missing values in other columns
    business_cols = ['Customer Age', 'Quantity', 'Unit Cost', 'Unit Price', 'Cost', 'Product Category', 'Sub Category']
    df = df.dropna(subset=[col for col in business_cols if col in df.columns])
    print(f"Dropped rows missing business metrics. Row count: {len(df)}")

    # 5. Logical Consistency: Gender
    if 'Customer Gender' in df.columns:
        gender_map = {'Famale': 'F', 'Male': 'M', 'F': 'F', 'M': 'M'}
        df['Customer Gender'] = df['Customer Gender'].map(gender_map).fillna(df['Customer Gender'])
        print("Standardized 'Customer Gender' to 'M' and 'F'.")

    # 6. Data Integrity: Year and Month alignment with Date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        if 'Year' in df.columns:
            df['Year'] = df['Date'].dt.year
        if 'Month' in df.columns:
            df['Month'] = df['Date'].dt.strftime('%B')
        print("Synchronized 'Year' and 'Month' columns with 'Date'.")
        
    print(f"Final row count: {len(df)}")
    print(f"Saving cleaned data to {output_file}...")
    df.to_excel(output_file, index=False)
    print("Done!")

if __name__ == "__main__":
    clean_data("Go IT Data.xlsx", "Go IT Data_Cleaned.xlsx")
