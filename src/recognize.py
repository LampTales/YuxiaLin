import whisper
import os

# possible values: 'tiny', 'base', 'samll', 'medium', 'large'
model_size = 'medium'
prompt = '林雨霞，你是一只可爱宝宝。'
device = 'cuda:1'

class Recognizer:
    def __init__(self, size=model_size, prompt=prompt, device='cuda:1'):
        self.model = whisper.load_model(name=size, device=device)
        self.prompt = prompt

    def recognize(self, filename):
        file = os.path.join(os.path.dirname(__file__), filename)
        print(file)
        result = self.model.transcribe(file, initial_prompt=self.prompt)
        return result

if __name__ == '__main__':
    r = Recognizer()
    result = r.recognize('test.wav')
    print(result.get('text'))