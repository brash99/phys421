import requests
from bs4 import BeautifulSoup
import time
import hashlib
from plyer import notification

# URL of the website to monitor
url = "https://navigator.cnu.edu/FacultyScheduleofClasses/socresults.aspx"

# Function to get the hash of the website content
def get_page_hash(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract specific part of the content, e.g., an element with ID 'main'
    content = soup.find(id="form1")  # Modify this as per the part you want to monitor

    # Convert content to string and compute hash
    if content:
        page_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        return page_hash
    return None

# Function to notify
def notify_change():
    notification.notify(
        title="Website Content Change Detected",
        message=f"The content of {url} has changed.",
        timeout=10
    )

# Main function to monitor
def monitor_website(url, interval=60):
    previous_hash = get_page_hash(url)
    print(f"Monitoring {url} every {interval} seconds...")

    while True:
        time.sleep(interval)
        current_hash = get_page_hash(url)

        if current_hash and previous_hash != current_hash:
            print("Change detected!")
            notify_change()
            previous_hash = current_hash
        else:
            print("No change detected.")

# Start monitoring
if __name__ == "__main__":
    monitor_website(url, interval=6)  # Monitor every 60 seconds