import os
import requests
from configparser import ConfigParser
import json

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
                "Authorization": self.authorization,
            }
            payload = json.dumps({
                "model": self.model,
                "messages": [
                    {
                    "role": "system",
                    "content": "You are a helpful assistant."
                    },
                    {
                    "role": "user",
                    "content": text
                    },

                ]
            })
            # response = requests.post(url=self.url, headers=headers, json=params)
            response = requests.request("POST", self.url, headers=headers, data=payload)
            message = response.json()
            
            # just for testing
            # print(message['choices'][0]['message']['content'])

            return message['choices'][0]['message']['content']
        except Exception as e:
            print(f'Error: {e}')


        
        

if __name__ == '__main__':
    responser = Responser()
    print(responser.respond('新鲜出炉的菠萝油，你也想吃吗？'))
    