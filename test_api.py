import requests

try:
    response = requests.post(
        "http://localhost:8000/predict/risk",
        json={
            "tx_hour": 14,
            "tx_day_of_week": 1,
            "account_age_days": 365,
            "amount": 150.0
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
