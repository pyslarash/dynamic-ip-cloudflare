import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

def verify_api_token():
    if not API_TOKEN:
        print("Error: API token not found in .env file.")
        return False

    # API endpoint and headers
    url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request to verify the token
        response = requests.get(url, headers=headers)
        response_data = response.json()

        # Check if the response indicates success
        if response.status_code == 200 and response_data.get("success"):
            result = response_data.get("result", {})
            if result.get("status") == "active":
                print("API token is valid and active.")
                return True
            else:
                print("API token is not active.")
                return False
        else:
            print(f"API token verification failed: {response_data}")
            return False

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

# Example usage
if __name__ == "__main__":
    if verify_api_token():
        print("Token verification successful!")
    else:
        print("Token verification failed.")
