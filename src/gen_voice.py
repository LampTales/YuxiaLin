from paddlespeech.cli.tts.infer import TTSExecutor

path = 'tts_output.wav'

class VoiceGenerator:
    def __init__(self):
        self.model = TTSExecutor()

    def generate(self, text, filename=path):
        wav_file = self.model(
            text=text, 
            output=filename,
            )
        
        return True