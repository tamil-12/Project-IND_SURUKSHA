import requests

# Define the URL of the endpoint
url = "http://127.0.0.1:5000/medication_reminder"

# Define the data to send in the request (replace with actual patient data)
data = {
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "condition": "Hypertension"
}

# Send the POST request
response = requests.post(url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Patient details sent successfully")
else:
    print("Failed to send patient details")
