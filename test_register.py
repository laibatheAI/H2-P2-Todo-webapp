import requests
import time
import json

# Test the registration endpoint to check if timeout issue is resolved
def test_registration():
    url = "http://127.0.0.1:8000/api/auth/register"

    # Test user data
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

    print("Testing registration endpoint...")
    start_time = time.time()

    try:
        response = requests.post(url, json=user_data, timeout=30)  # 30 second timeout
        end_time = time.time()

        print(f"Registration completed in {end_time - start_time:.2f} seconds")
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            print("SUCCESS: Registration completed successfully!")
            response_data = response.json()
            print(f"User ID: {response_data.get('id')}")
            print(f"Access token received: {'access_token' in response_data}")
        else:
            print(f"FAILED: Registration failed with status {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f"TIMEOUT: Registration timed out after {end_time - start_time:.2f} seconds")
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        print(f"ERROR: Request failed after {end_time - start_time:.2f} seconds")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_registration()