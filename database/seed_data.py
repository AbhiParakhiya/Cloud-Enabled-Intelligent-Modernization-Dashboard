import sqlite3
import random
import datetime
from faker import Faker

fake = Faker()
DB_PATH = 'legacy_system.db'

def create_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def init_db(conn):
    with open('schema.sql', 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    print("Database initialized.")

def generate_data(conn, num_customers=100, num_transactions=2000):
    cursor = conn.cursor()
    
    print(f"Generating {num_customers} customers...")
    customers = []
    segments = ['RETAIL', 'CORPORATE', 'SME']
    for _ in range(num_customers):
        customers.append((
            fake.name(),
            fake.email(),
            random.choice(segments),
            fake.date_between(start_date='-5y', end_date='today')
        ))
    
    cursor.executemany("INSERT INTO customers (name, email, segment, account_created_date) VALUES (?, ?, ?, ?)", customers)
    conn.commit()
    
    print(f"Generating {num_transactions} transactions...")
    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    transactions = []
    types = ['DEBIT', 'CREDIT', 'TRANSFER']
    statuses = ['PROCESSED', 'FAILED', 'PENDING'] # Most should be processed
    
    for _ in range(num_transactions):
        cust_id = random.choice(customer_ids)
        amount = round(random.uniform(10.0, 5000.0), 2)
        tx_type = random.choice(types)
        status = random.choices(statuses, weights=[90, 5, 5], k=1)[0]
        date = fake.date_time_between(start_date='-1y', end_date='now')
        
        processed_at = date if status == 'PROCESSED' else None
        
        transactions.append((
            cust_id,
            amount,
            tx_type,
            date,
            status,
            processed_at
        ))
        
    cursor.executemany("INSERT INTO transactions (customer_id, amount, transaction_type, transaction_date, status, processed_at) VALUES (?, ?, ?, ?, ?, ?)", transactions)
    conn.commit()
    print("Data generation complete.")

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        init_db(conn)
        generate_data(conn)
        conn.close()
