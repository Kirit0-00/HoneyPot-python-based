import requests
import time

def test_web_decoy():
    url = "http://127.0.0.1:8080/login"
    data = {
        "username": "admin",
        "password": "password123"
    }
    
    print(f"Testing Web Decoy Login at {url}...")
    try:
        response = requests.post(url, data=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.json()}")
        print("✓ Web Decoy Login test successful")
    except Exception as e:
        print(f"✗ Web Decoy Login test failed: {e}")

if __name__ == "__main__":
    test_web_decoy()
