import os
import requests
from configparser import ConfigParser
import json

conversation_memory_limit = 10

# TODO: Find out how to do the role play
init_system_sentence = "你需要扮演游戏明日方舟中的角色林雨霞来完成对话。" + \
                        "林雨霞是未来龙门黑道的话事人，因此给人神秘而阴沉的印象。" + \
                        "但实际上其本人是个易于相处的可爱少女，永远是一副从容有度的样子，更被许多人评价为“非常符合他国干员对温文尔雅的炎国人的想象”。" + \
                        "林小姐绝不会彰显出一点给人压力的气场，待人接物的礼节娴熟至极又不显痕迹。" + \
                        "此外林雨霞小姐对炎国的书法、绘画、茶道、建筑等艺术有很深的造诣。" + \
                        "你需要扮演林雨霞，你的谈话对象是你的好友，与对方闲聊。" + \
                        "请使用更口语化的风格来回答，因为对方与你很熟，所以不需要过多的礼貌用语，但仍然需要端庄娴静一些。" + \
                        "另外，请尝试真正地代入角色进行对话，而不是机械重复自己的身份设定。"

# init_system_sentence = "You are a helpful assistant."

# print(init_system_sentence)

class Responser:
    def __init__(self, init_system_sentence=init_system_sentence, conversation_memory_limit=conversation_memory_limit):
        conn = ConfigParser()
        file_path = os.path.join(os.path.dirname(__file__), 'configs/response.ini')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File not found: {file_path}')
        conn.read(file_path)
        self.url = conn.get('response', 'URL')
        self.authorization = 'Bearer ' + conn.get('response', 'Authorization')
        self.model = conn.get('response', 'Model')
        self.messages = [{
                    "role": "system",
                    "content": init_system_sentence
                    }]
        self.conversation_memory_limit = conversation_memory_limit

    def respond(self, text):
        try:
            if len(self.messages) > self.conversation_memory_limit:
                self.messages.pop(1)
                self.messages.pop(2)

            self.messages.append({'role': 'user',
                                  'content': text})
            headers = {
                "Content-Type": "application/json",
                # "Accept": "application/json",
                "Authorization": self.authorization,

            }
            payload = json.dumps({
                "model": self.model,
                "messages": self.messages,
            })
            # response = requests.post(url=self.url, headers=headers, json=params)
            response = requests.request("POST", self.url, headers=headers, data=payload)
            message = response.json()
            
            # just for testing
            # print(message['choices'][0]['message']['content'])
            self.messages.append(message['choices'][0]['message'])
            return message['choices'][0]['message']['content']
        except Exception as e:
            print(f'Error: {e}')

    def refresh(self):
        self.messages = [{
                    "role": "system",
                    "content": init_system_sentence
                    }]
        
        

def conversation_test():
    responser = Responser()
    while True:
        text = input('You >>> ')
        if text == 'exit':
            break
        if text == 'check':
            print('Output the conversation history: ')
            for message in responser.messages:
                role = message['role']
                if role == 'system':
                    role = 'Ini'
                elif role == 'user':
                    role = 'You'
                elif role == 'assistant':
                    role = 'Lin'
                print(f'\t{role} >>> {message["content"]}')
            continue
        response = responser.respond(text)
        print(f'Lin >>> {response}')

if __name__ == '__main__':
    # responser = Responser()
    conversation_test()
    
    