import requests

def get_current_ip():
    try:
        # Use a free IP lookup service to fetch the public IP
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        ip = response.json().get("ip")
        return ip
    except requests.RequestException as e:
        print(f"An error occurred while fetching the current IP: {e}")
        return None

# Example usage
if __name__ == "__main__":
    current_ip = get_current_ip()
    if current_ip:
        print(f"My current public IP is: {current_ip}")
    else:
        print("Failed to retrieve current IP.")
