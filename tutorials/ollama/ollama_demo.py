import requests
import json
import sys
from haversine import haversine

country = sys.argv[1]
schema = {
    "city": {
        "type": "string",
        "description": "The name of the city"
    },
    "latitude": {
        "type": "float",
        "description": "The decimal latitude of the city"
    },
    "longitude": {
        "type": "float",
        "description": "The decimal longitude of the city"
    }
}
payload = {
    "model": "llama3.1:latest",
    "messages": [
        {
            "role": "system",
            "content": f"You are a helpful AI assistant. The user will enter a country name and the assistant will return the decimal latitude and decimal longitude of the capital of the country. Output in JSON using the schema defined here: {schema}."
        },
        # one shot example
        {"role": "user", "content": f"China"},
        {"role": "assistant", "content": "{ \"city\": \"Beijing\", \"latitude\": 39.9042, \"longitude\": 116.4074 }"},
        # user query
        {"role": "user", "content": f"{country}"}
    ],
    'format': 'json',
    'stream': False
}

response = requests.post("http://localhost:11434/api/chat", json=payload)
if response.status_code != 200:
    print(response.text)
for message in response.iter_lines():
    jsonstr = json.loads(message)
    print(jsonstr["message"]["content"], end="")
