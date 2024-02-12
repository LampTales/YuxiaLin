import whisper
import os

# possible values: 'tiny', 'base', 'samll', 'medium', 'large'
model_size = 'medium'

class Recognizer:
    def __init__(self, size=model_size):
        self.model = whisper.load_model(name=size, device="cuda:1")

    def recognize(self, filename):
        file = os.path.join(os.path.dirname(__file__), filename)
        print(file)
        result = self.model.transcribe(file)
        return result

if __name__ == '__main__':
    r = Recognizer()
    result = r.recognize('test.wav')
    print(result.get('text'))