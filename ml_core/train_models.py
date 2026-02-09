import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report

# Paths
# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../analytics/cleaned_data.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

def train_models():
    if not os.path.exists(DATA_PATH):
        print("Data file not found. Run etl_process.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Prepare Features and Target
    # Predicting 'is_high_value' as a proxy for 'Risk/Priority'
    # Features: tx_hour, tx_day_of_week, account_age_days
    # Note: In a real app we'd use more complex features and encoding.
    
    features = ['tx_hour', 'tx_day_of_week', 'account_age_days']
    target = 'is_high_value'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 1. Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred_lr))
    
    with open(f'{MODEL_DIR}/logistic_regression.pkl', 'wb') as f:
        pickle.dump(lr_model, f)

    # 2. Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
    
    with open(f'{MODEL_DIR}/random_forest.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
        
    # 3. K-Means Clustering
    print("Training K-Means Clustering...")
    # Clustering on Amount and Frequency (proxy) or just Amount/Hour
    X_cluster = df[['amount', 'tx_hour']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_cluster)
    
    with open(f'{MODEL_DIR}/kmeans.pkl', 'wb') as f:
        pickle.dump(kmeans, f)
        
    print(f"Models saved to {os.path.abspath(MODEL_DIR)}")

if __name__ == "__main__":
    train_models()
