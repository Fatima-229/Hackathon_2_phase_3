import requests
import json

# First, register a user to get a token
register_url = "http://localhost:8082/api/v1/auth/register"
headers = {"Content-Type": "application/json"}
register_data = {"email": "testuser@example.com", "password": "testpassword"}

try:
    register_response = requests.post(register_url, headers=headers, data=json.dumps(register_data))
    print(f"Register Status Code: {register_response.status_code}")
    print(f"Register Response: {register_response.text}")
    
    if register_response.status_code == 200:
        token_data = register_response.json()
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
        print("\nRegistration failed, cannot proceed with task creation.")
        
except Exception as e:
    print(f"Error: {e}")