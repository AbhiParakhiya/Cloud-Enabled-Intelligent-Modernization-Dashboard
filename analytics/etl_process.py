import sqlite3
import pandas as pd
import os

# Paths
# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database/legacy_system.db')
OUTPUT_PATH = os.path.join(BASE_DIR, 'cleaned_data.csv')

def extract_data():
    print("Connecting to database...")
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

    query = """
    SELECT 
        t.transaction_id,
        t.customer_id,
        t.amount,
        t.transaction_type,
        t.transaction_date,
        t.status,
        c.segment,
        c.account_created_date
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    """
    
    print("Extracting data...")
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Extracted {len(df)} rows.")
    return df

def transform_data(df):
    print("Transforming data...")
    
    # 1. Handle Missing Values (Simulated)
    # The simulated data is mostly clean, but let's ensure
    df = df.dropna()
    
    # 2. Convert Dates
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['account_created_date'] = pd.to_datetime(df['account_created_date'])
    
    # 3. Feature Engineering
    # Feature 1: Transaction Hour
    df['tx_hour'] = df['transaction_date'].dt.hour
    
    # Feature 2: Day of Week
    df['tx_day_of_week'] = df['transaction_date'].dt.dayofweek
    
    # Feature 3: Account Age (days at time of tx)
    df['account_age_days'] = (df['transaction_date'] - df['account_created_date']).dt.days
    
    # Feature 4: High Value Transaction Flag
    df['is_high_value'] = (df['amount'] > 500).astype(int)
    
    # Encode Categorical Variables (One-Hot Encoding for 'transaction_type' and 'segment')
    # For a simple ETL, we might just keep them for now or encode them.
    # Let's keep them as is for EDA, but we might need to encode for ML later.
    # We'll save the "Analysis Ready" dataset.
    
    print("Transformation complete.")
    return df

def load_data(df):
    print(f"Saving data to {OUTPUT_PATH}...")
    df.to_csv(OUTPUT_PATH, index=False)
    print("Data saved successfully.")

if __name__ == "__main__":
    df = extract_data()
    if df is not None:
        df_clean = transform_data(df)
        load_data(df_clean)
