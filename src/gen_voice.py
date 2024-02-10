from paddlespeech.cli.tts.infer import TTSExecutor
from gradio_client import Client
import requests

path = 'tts_output.wav'

model_name_ps = 'fastspeech2_csmsc'
language_ps = 'zh'
device_ps = 'gpu:3'

class PaddleSpeech_generater:
    def __init__(self, device=device_ps, model_name=model_name_ps, language=language_ps):
        self.model = TTSExecutor()
        self.device = device
        self.model_name = model_name
        self.language = language

    def generate(self, text, filename=path, **kwargs):
        wav_file = self.model(
            text=text, 
            output=filename,
            device=self.device,
            am=self.model_name,
            lang=self.language,
            use_onnx=True,
            )
        
        return True
    


host_bs = '127.0.0.1'
port_bs = 8086
model_id_bs = 0
speaker_name_bs = 'lin_zh'
sdp_ratio_bs = 0.5
noise_bs = 0.6
noise_w_bs = 0.9
length_bs = 1
language_bs = 'ZH'
auto_translate_bs = False
auto_split_bs = False
emotion_bs = None
style_text_bs = None
style_weight_bs = 0.7


class BertVITS2_generater:
    def __init__(self, host=host_bs, port=port_bs):
        self.url = f'http://{host}:{port}'
        self.voice_url = f'http://{host_bs}:{port_bs}/voice'

        self.model = model_id_bs
        self.speaker_name = speaker_name_bs
        self.sdp_ratio = sdp_ratio_bs
        self.noise = noise_bs
        self.noise_w = noise_w_bs
        self.length = length_bs
        self.language = language_bs
        self.auto_translate = auto_translate_bs
        self.auto_split = auto_split_bs
        self.emotion = emotion_bs
        self.style_text = style_text_bs
        self.style_weight = style_weight_bs
        

    # TODO: Test the params passing
    def generate(self, text, filename=path, **kwargs):
        # fill params
        params = {
            'text': text if 'text' not in kwargs else kwargs['text'],
            'model_id': self.model if 'model_id' not in kwargs else kwargs['model_id'],
            'speaker_name': self.speaker_name if 'speaker_name' not in kwargs else kwargs['speaker_name'],
            'sdp_ratio': self.sdp_ratio if 'sdp_ratio' not in kwargs else kwargs['sdp_ratio'],
            'noise': self.noise if 'noise' not in kwargs else kwargs['noise'],
            'noise_w': self.noise_w if 'noise_w' not in kwargs else kwargs['noise_w'],
            'length': self.length if 'length' not in kwargs else kwargs['length'],
            'language': self.language if 'language' not in kwargs else kwargs['language'],
            'auto_translate': self.auto_translate if 'auto_translate' not in kwargs else kwargs['auto_translate'],
            'auto_split': self.auto_split if 'auto_split' not in kwargs else kwargs['auto_split'],
            'emotion': self.emotion if 'emotion' not in kwargs else kwargs['emotion'],
            'style_text': self.style_text if 'style_text' not in kwargs else kwargs['style_text'],
            'style_weight': self.style_weight if 'style_weight' not in kwargs else kwargs['style_weight'],
        }

        # send request
        response = requests.get(self.voice_url, params=params)

        # check response
        print(f'From BertVITS2_generater: {response.status_code}, {response.reason}')

        # save the response
        with open(filename, 'wb') as f:
            f.write(response.content)

        return True
    
    # No test done yet
    # TODO: make it really useful
    def any_api(self, filename=path, method='GET', api='/voice', params=None):
        try:
            if method == 'GET':
                response = requests.get(self.url+api, params=params)
            elif method == 'POST':
                response = requests.post(self.url+api, params=params)
            else:
                raise ValueError('Invalid method')
            
            print(f'From BertVITS2_generater: {response.status_code}, {response.reason}')
            
            # Obviously here are some problems, but I want to put it aside for now.
            if response.content:
                with open(filename, 'wb') as f:
                    f.write(response.content)

            return True

        except Exception as e:
            print(e)
            return False
        
    

use_generator = 'BertVITS2_generater'
class VoiceGenerator:
    def __init__(self, generator=use_generator):
        self.generator = None
        self.use_generator = generator
        if generator == 'PaddleSpeech_generater':
            self.generator = PaddleSpeech_generater()
        elif generator == 'BertVITS2_generater':
            self.generator = BertVITS2_generater()
        else:
            raise ValueError('Invalid generator')
        

    def generate(self, text, filename=path, **kwargs):
        return self.generator.generate(text, filename, **kwargs)
    
    

if __name__ == '__main__':
    bs = BertVITS2_generater(host='127.0.0.1', port=8086)
    bs.generate('新鲜出炉的菠萝油，你也想吃？')