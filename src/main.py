import whisper
from record import get_word
from recognize import recognize

WHISPER_MODEL = 'tiny'
VOICE_FILE = 'test.wav'

def get_whisper_model(model_size='tiny'):
    model = whisper.load_model(name=model_size)
    return model

def main():
    model = get_whisper_model(WHISPER_MODEL)

    get_word(filename=VOICE_FILE)
    result = recognize(model, VOICE_FILE)
    word = result.get('text')
    







if __name__ == '__main__':
    main()