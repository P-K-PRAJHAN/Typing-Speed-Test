#!/usr/bin/env python3
"""
Script to test backend functionality
"""
import requests
import json

def test_backend():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing backend functionality...")
    
    # Test health check endpoint
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test generate-text endpoint
    print("\n2. Testing generate-text endpoint...")
    try:
        response = requests.post(
            f"{base_url}/api/generate-text",
            json={"difficulty": "easy", "sentences": 2}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nBackend testing completed!")

if __name__ == "__main__":
    test_backend()