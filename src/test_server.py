import http.client
import os
import argparse
from urllib import parse as urlparse
# from record import get_word
from gradio_client import Client

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to connect', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to connect', type=int, default=8081)
    return parser.parse_args()

def main():
    wav_path = 'test.wav'
    # get_word(filename=wav_path)

    args = arg_parser()

    conn = http.client.HTTPConnection(args.host, args.port)
    # send the wav to the server
    wav_path = '../lin_voice/zh/戳一下.wav'
    with open(wav_path, 'rb') as f:
        data = f.read()
        length = len(data)
    conn.request('POST', '/rep', headers={'Operation': 'rep', 'Content-Length': length})
    conn.send(data)
    response = conn.getresponse()
    print(response.status, response.reason)
    result = urlparse.unquote(response.getheader('rec-result'))
    print(result)
    # receive the wav from the server
    data = response.read()
    with open('receive_from_server.wav', 'wb') as f:
        f.write(data)

    # end the connection
    conn.close()

def test_conn():
    n = 0
    args = arg_parser()

    while n < 10:
        conn = http.client.HTTPConnection(args.host, args.port)
        conn.close()
        print()

def test():
    activate = False
    print(str(activate))
        

host_bs = '127.0.0.1'
port_bs = 8085


class BertVITS2_generater:
    def __init__(self, host=host_bs, port=port_bs):
        self.client = Client(f"http://{host}:{port}/")

    def generate(self, text, filename='tts_output.wav'):
        result = self.client.predict(
		    "hello?",	# str  in '输入文本内容' Textbox component
		    "lin_en,lin_en",	# str (Option from: [('lin_jp', 'lin_jp'), ('lin_en', 'lin_en'), ('lin_zh', 'lin_zh')]) in 'Speaker' Dropdown component
		    0.5,	# int | float (numeric value between 0 and 1) in 'SDP Ratio' Slider component
		    0.6,	# int | float (numeric value between 0.1 and 2) in 'Noise' Slider component
		    0.9,	# int | float (numeric value between 0.1 and 2) in 'Noise_W' Slider component
		    1,	# int | float (numeric value between 0.1 and 2) in 'Length' Slider component
		    "EN,EN",	# str (Option from: [('ZH', 'ZH'), ('JP', 'JP'), ('EN', 'EN'), ('mix', 'mix'), ('auto', 'auto')]) in 'Language' Dropdown component
		    None,	# str (filepath on your computer (or URL) of file) in 'Audio prompt' Audio component
		    "Happy",	# str  in 'Text prompt' Textbox component
		    "Text prompt",	# str  in 'Prompt Mode' Radio component
		    "",	# str  in '辅助文本' Textbox component
		    0.7,	# int | float (numeric value between 0 and 1) in 'Weight' Slider component
		    
            fn_index=0
        )
        print(result)

        # result = self.client.predict(
		#     "Text prompt",	# str  in 'Prompt Mode' Radio component
		#     fn_index=1
        # )
        # print(result)

        return True
    
def test_gen():
    bs = BertVITS2_generater(host='10.16.88.247', port=8085)
    bs.generate('新鲜出炉的菠萝油，你也想吃？')



if __name__ == '__main__':
    test_gen()