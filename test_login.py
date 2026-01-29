import requests
import time
import json

# Test the login endpoint to check performance
def test_login():
    url = "http://127.0.0.1:8000/api/auth/login"

    # Test user data
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    print("Testing login endpoint...")
    start_time = time.time()

    try:
        response = requests.post(url, json=user_data, timeout=30)  # 30 second timeout
        end_time = time.time()

        print(f"Login completed in {end_time - start_time:.2f} seconds")
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            print("SUCCESS: Login completed successfully!")
            response_data = response.json()
            print(f"Access token received: {'access_token' in response_data}")
            print(f"User ID: {response_data.get('user', {}).get('id')}")
        else:
            print(f"FAILED: Login failed with status {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f"TIMEOUT: Login timed out after {end_time - start_time:.2f} seconds")
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        print(f"ERROR: Request failed after {end_time - start_time:.2f} seconds")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()