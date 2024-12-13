import os
import time
import requests
from dotenv import load_dotenv

from current_ip import get_current_ip

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

def needs_dns_update(zone_name):
    """
    Fetch all A records from Cloudflare, compare them with the current IP,
    and determine if any record needs updating.
    """
    if not API_TOKEN:
        print("Error: API token not found in .env file.")
        return False

    # API endpoints and headers
    base_url = "https://api.cloudflare.com/client/v4"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Get the Zone ID for the given zone name
        zones_url = f"{base_url}/zones"
        zones_response = requests.get(zones_url, headers=headers, params={"name": zone_name})
        zones_data = zones_response.json()

        if not zones_data.get("success") or not zones_data["result"]:
            print(f"Failed to retrieve zone ID for {zone_name}: {zones_data}")
            return False

        zone_id = zones_data["result"][0]["id"]
        print(f"Zone ID for {zone_name}: {zone_id}")

        # Step 2: Fetch all DNS records for the zone
        dns_records_url = f"{base_url}/zones/{zone_id}/dns_records"
        dns_records_response = requests.get(dns_records_url, headers=headers)
        dns_records_data = dns_records_response.json()

        if not dns_records_data.get("success"):
            print(f"Failed to retrieve DNS records for {zone_name}: {dns_records_data}")
            return False

        dns_records = dns_records_data["result"]

        # Step 3: Get the current public IP
        current_ip = get_current_ip()
        if not current_ip:
            print("Could not determine current public IP.")
            return False

        # Step 4: Check if any A record (excluding mail) needs an update
        needs_update = False
        for record in dns_records:
            if record["type"] == "A" and not record["name"].startswith("mail"):
                if record["content"] != current_ip:
                    print(f"Record {record['name']} needs updating: current IP {current_ip}, record IP {record['content']}")
                    needs_update = True
                else:
                    print(f"Record {record['name']} is up-to-date.")

        return needs_update

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    
def monitor_dns(zone_name, check_time):
    """
    Run checks every minute to see if DNS records need updating.
    """
    while True:
        print("\nRunning DNS check...")
        if needs_dns_update(zone_name):
            update_dns_a_records(zone_name)
            print("DNS records need updating.")
        else:
            print("All DNS records are up-to-date.")
        print("Next check in 1 minute...\n")
        time.sleep(check_time)

def update_dns_a_records(zone_name, new_ip=None):
    if not API_TOKEN:
        print("Error: API token not found in .env file.")
        return False
    
    if new_ip is None:
        new_ip = get_current_ip()

    # API endpoints and headers
    base_url = "https://api.cloudflare.com/client/v4"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Get the Zone ID for the given zone name
        zones_url = f"{base_url}/zones"
        zones_response = requests.get(zones_url, headers=headers, params={"name": zone_name})
        zones_data = zones_response.json()

        if not zones_data.get("success") or not zones_data["result"]:
            print(f"Failed to retrieve zone ID for {zone_name}: {zones_data}")
            return False

        zone_id = zones_data["result"][0]["id"]
        print(f"Zone ID for {zone_name}: {zone_id}")

        # Step 2: Fetch all DNS records for the zone
        dns_records_url = f"{base_url}/zones/{zone_id}/dns_records"
        dns_records_response = requests.get(dns_records_url, headers=headers)
        dns_records_data = dns_records_response.json()

        if not dns_records_data.get("success"):
            print(f"Failed to retrieve DNS records for {zone_name}: {dns_records_data}")
            return False

        dns_records = dns_records_data["result"]

        # Step 3: Filter A records that are not related to mail
        records_to_update = [
            record for record in dns_records
            if record["type"] == "A" and not record["name"].startswith("mail")
        ]

        # Step 4: Update each filtered record with the new IP
        for record in records_to_update:
            update_url = f"{dns_records_url}/{record['id']}"
            update_data = {
                "type": "A",
                "name": record["name"],
                "content": new_ip,
                "ttl": record["ttl"],
                "proxied": record["proxied"]
            }
            update_response = requests.put(update_url, headers=headers, json=update_data)
            update_response_data = update_response.json()

            if update_response_data.get("success"):
                print(f"Updated {record['name']} to {new_ip}")
            else:
                print(f"Failed to update {record['name']}: {update_response_data}")

        return True

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

# Example usage
if __name__ == "__main__":
    zone_name = "imadenet.work"  # Replace with your domain name
    monitor_dns(zone_name)