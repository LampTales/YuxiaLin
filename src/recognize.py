import whisper
import os

def recognize(model, filename):
    file = os.path.join(os.path.dirname(__file__), filename)
    print(file)
    result = model.transcribe(file)
    return result.text

if __name__ == '__main__':
    model = whisper.load_model(name='tiny')
    result = recognize(model, 'test.wav')
    print(result)