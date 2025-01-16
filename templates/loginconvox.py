import requests

# Define the login URL
url = "http://192.168.1.11:8225/ConVoxCCS/index.php"

# Define the payload
data = {
    "username": "test",
    "password": "test",
    "station": "1029",
    "mode": "LOGINUSER",
    "user_type": "Agent"
}

# Send the POST request
response = requests.post(url, data=data)

# Print all headers
print("Response Headers:")
print(response.headers)

# Check cookies in the session
session_cookies = requests.utils.dict_from_cookiejar(response.cookies)
print("Session Cookies:")
print(session_cookies)
