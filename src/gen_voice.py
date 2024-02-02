from paddlespeech.cli.tts.infer import TTSExecutor

path = 'tts_output.wav'

model_name = 'fastspeech2_csmsc'
language = 'zh'
device = 'gpu:3'

class VoiceGenerator:
    def __init__(self, device=device, model_name=model_name, language=language):
        self.model = TTSExecutor()
        self.device = device
        self.model_name = model_name
        self.language = language

    def generate(self, text, filename=path):
        wav_file = self.model(
            text=text, 
            output=filename,
            device=self.device,
            am=self.model_name,
            lang=self.language,
            use_onnx=True,
            )
        
        return True
    

if __name__ == '__main__':
    voice_generator = VoiceGenerator()
    voice_generator.generate('刚出炉的菠萝油，你都想食？')