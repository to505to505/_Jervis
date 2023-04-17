import requests

url = "http://your-fastapi-app.com/my-handle"
data = {"name": "John", "age": 30}

response = requests.post(url, json=data)
print(response.content)
if response.status_code == 200:
    print("Data was successfully posted to the handle")
    print(response.text) # Debugging line
    try:
        response_data = response.json()
        # Process the JSON data here
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from the server")
else:
    print("There was an error posting data to the handle")