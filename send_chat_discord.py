import os
import requests

WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']

try:
    with open('chat.json', 'rb') as f:
        files = {'file': f}
        response = requests.post(WEBHOOK_URL, files=files)
        
        if response.status_code == 204:
            print("Chat sent to Discord")
        else:
            print(f"Error: {response.status_code}")
except FileNotFoundError:
    print("chat.json not found")
except Exception as e:
    print(f"Error: {e}")
