import requests
import json

# Test the login endpoint
url = "http://localhost:8082/api/v1/auth/login"
headers = {"Content-Type": "application/json"}
data = {"email": "test@example.com", "password": "testpassword"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")