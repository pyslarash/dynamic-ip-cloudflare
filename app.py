import threading
from update_ip import monitor_dns

def monitor_zones(file_path, check_time):
    """
    Reads a file with domain zones and runs the monitor_dns function for each zone in a separate thread.
    """
    try:
        with open(file_path, "r") as file:
            zones = [line.strip() for line in file if line.strip()]  # Read and clean lines
        
        if not zones:
            print("No zones found in the file.")
            return

        print(f"Found {len(zones)} zones. Starting monitoring...")

        # Start a separate thread for each domain
        for zone in zones:
            thread = threading.Thread(target=monitor_dns, args=(zone, check_time))
            thread.daemon = True  # Ensure threads close when the main program exits
            thread.start()
            print(f"Monitoring started for {zone}")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    zones_file = "zones.txt"  # Path to your zones file
    check_time = 900  # Time in seconds between checks
    monitor_zones(zones_file, check_time)

    # Keep the main thread alive so the threads can continue running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping all monitors.")
