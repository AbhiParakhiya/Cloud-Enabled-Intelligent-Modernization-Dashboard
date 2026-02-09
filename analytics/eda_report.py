import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

DATA_PATH = 'cleaned_data.csv'
REPORT_DIR = 'reports'

def run_eda():
    if not os.path.exists(DATA_PATH):
        print("Data file not found. Run etl_process.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    print("Generating EDA Report...")
    
    # 1. Summary Statistics
    with open(f"{REPORT_DIR}/summary_stats.txt", "w") as f:
        f.write("Dataset Shape:\n")
        f.write(str(df.shape) + "\n\n")
        f.write("Columns:\n")
        f.write(str(df.columns.tolist()) + "\n\n")
        f.write("Missing Values:\n")
        f.write(str(df.isnull().sum()) + "\n\n")
        f.write("Descriptive Statistics:\n")
        f.write(str(df.describe()) + "\n")

    # 2. Distribution of Transaction Amounts
    plt.figure(figsize=(10, 6))
    sns.histplot(df['amount'], bins=50, kde=True)
    plt.title('Distribution of Transaction Amounts')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.savefig(f"{REPORT_DIR}/amount_distribution.png")
    plt.close()
    
    # 3. Transactions by Segment
    plt.figure(figsize=(8, 5))
    sns.countplot(x='segment', data=df)
    plt.title('Transaction Count by Customer Segment')
    plt.savefig(f"{REPORT_DIR}/segment_counts.png")
    plt.close()
    
    # 4. Correlation Heatmap (Numerical only)
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.savefig(f"{REPORT_DIR}/correlation_heatmap.png")
    plt.close()
    
    print(f"EDA Reports saved to {os.path.abspath(REPORT_DIR)}")

if __name__ == "__main__":
    run_eda()
