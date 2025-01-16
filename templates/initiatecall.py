import requests

url = "http://192.168.1.11:8225/ConVoxCCS/Agent/bridge.php"

# Define headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "PHPSESSID=i4rhoc6t67shs2o65lpi753vv1"
}

# Define data
data = {
    "ACTION": "DIAL",
    "user": "test",
    "phone_number": "8595381723"
}

try:
    # Make POST request
    response = requests.post(url, headers=headers, data=data)
    
    # Check if the response is successful
    response.raise_for_status()
    
    # Print success message
    print("Success:", response.text)
    print("Call initiated successfully!")
except requests.exceptions.RequestException as e:
    # Handle errors
    print("Error:", e)
    print("Failed to initiate call.")
