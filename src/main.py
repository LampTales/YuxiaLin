import whisper
from record import get_word
from recognize import Recognizer

WHISPER_MODEL = 'tiny'
VOICE_FILE = 'test.wav'



def main():
    recognizer = Recognizer()
    result = recognizer.recognize('../lin_voice/信赖触摸.wav')
    print(result.get('text'))


if __name__ == '__main__':
    main()