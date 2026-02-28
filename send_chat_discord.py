import os
import json
import requests

WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']

def seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def convert_chat_to_txt():
    try:
        with open('chat.json', 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        
        txt_path = 'chat.txt'
        with open(txt_path, 'w', encoding='utf-8') as f:
            comments = chat_data.get('comments', [])
            
            for comment in comments:
                try:
                    commenter = comment.get('commenter', {})
                    username = commenter.get('display_name') or commenter.get('name', 'Unknown')
                    
                    message = comment.get('message', {}).get('body', '')
                    
                    content_offset = comment.get('content_offset_seconds', 0)
                    timestamp = seconds_to_timestamp(content_offset)
                    
                    f.write(f"[{timestamp}] {username}: {message}\n")
                except Exception as e:
                    pass
        
        return txt_path
        
    except FileNotFoundError:
        print("chat.json not found")
        return None
    except json.JSONDecodeError:
        print("Error parsing chat.json")
        return None

def send_to_discord(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(WEBHOOK_URL, files=files)
            
            if response.status_code == 204:
                print("Chat sent to Discord")
            else:
                print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    txt_file = convert_chat_to_txt()
    if txt_file:
        send_to_discord(txt_file)
