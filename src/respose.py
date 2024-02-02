import os
import requests
from configparser import ConfigParser

# TODO: Implement a class that will respond to the user's input
class Responser:
    def __init__(self):
        conn = ConfigParser()
        file_path = os.path.join(os.path.dirname(__file__), 'configs/response.ini')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File not found: {file_path}')
        conn.read(file_path)
        self.url = conn.get('response', 'URL')
        self.authorization = conn.get('response', 'Authorization')
        self.model = conn.get('response', 'Model')

    def respond(self, text):
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": self.authorization
            }
            params = {
                "model": self.model,
                "message": {
                    "role": "user",
                    "content": text
                }
            }
            response = requests.post(url=self.url, headers=headers, json=params)
            message = response.json()
            # just for testing
            return message['choice'][0]['message']['content']
        except Exception as e:
            print(f'Error: {e}')
        
    