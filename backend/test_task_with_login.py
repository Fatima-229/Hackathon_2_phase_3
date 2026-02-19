import requests
import json

# First, login to get a token (since user already exists)
login_url = "http://localhost:8082/api/v1/auth/login"
headers = {"Content-Type": "application/json"}
login_data = {"email": "testuser@example.com", "password": "testpassword"}

try:
    login_response = requests.post(login_url, headers=headers, data=json.dumps(login_data))
    print(f"Login Status Code: {login_response.status_code}")
    print(f"Login Response: {login_response.text}")
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data['access_token']
        print(f"\nAccess Token: {access_token}")
        
        # Now try to create a task with the token
        task_url = "http://localhost:8082/api/v1/tasks/"
        task_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium"
        }
        
        task_response = requests.post(task_url, headers=task_headers, data=json.dumps(task_data))
        print(f"\nTask Creation Status Code: {task_response.status_code}")
        print(f"Task Creation Response: {task_response.text}")
    else:
        print("\nLogin failed, cannot proceed with task creation.")
        
except Exception as e:
    print(f"Error: {e}")