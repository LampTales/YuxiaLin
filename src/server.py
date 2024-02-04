import http.server
import os
import argparse
from urllib import parse as urlparse

from recognize import Recognizer
from response import Responser
from gen_voice import VoiceGenerator


recognizer = None
responser = None
voice_generator = None


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to listen', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to listen', type=int, default=8081)
    return parser.parse_args()


def act_judge(rec_result):
    if '你好' in rec_result.get('text'):
        return True
    else:
        return False


class VoiceServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print('POST request received')
        operation = self.headers['Operation']
        debug_flag = self.headers['debug'] is not None and self.headers['debug'] == 'True'
        print('Operation: {}'.format(operation))
        if operation == 'rec':
            self.rec(debug_flag=debug_flag)
        elif operation == 'rep':
            self.rep(debug_flag=debug_flag)
        elif operation == 'tts':
            self.tts(debug_flag=debug_flag)
        elif operation == 'p_t':
            self.rep_tts(debug_flag=debug_flag)
        elif operation == 'c_p_t':
            self.rec_rep_tts(debug_flag=debug_flag)
        elif operation == 'act':
            self.activate(debug_flag=debug_flag)


    def activate(self, debug_flag=False):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        with open('receive_from_client.wav', 'wb') as f:
            f.write(data)

        # recognize the wav file
        result = recognizer.recognize('receive_from_client.wav')

        # TODO: check if the recognized text is a activation word
        activate = False
        if act_judge(result):
            activate = True

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('activate', str(activate))
        self.end_headers()


    def rec(self, debug_flag=False):
        length = int(self.headers['Content-Length'])
        
        data = self.rfile.read(length)
        with open('receive_from_client.wav', 'wb') as f:
            f.write(data)
        result = recognizer.recognize('receive_from_client.wav')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('rec-result', urlparse.quote(result.get('text')))

        # TODO: check if the recognized text has text
        has_text = True
        self.send_header('has-text', str(has_text))

        self.end_headers()

        # send the wav file back to the client
        with open('receive_from_client.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def rep(self, debug_flag=False):
        text = urlparse.unquote(self.headers['text'])
        print('Receive text: {}'.format(text))

        response = responser.respond(text)
        print('Response: {}'.format(response))

        self.send_response(200) 
        self.send_header('Content-Type', 'text/plain')
        self.send_header('rep-result', urlparse.quote(response))
        self.end_headers()


    def tts(self, debug_flag=False):
        text = urlparse.unquote(self.headers['text'])
        print('Text to generate: {}'.format(text))

        voice_generator.generate(text, filename='response.wav')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        with open('response.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def rep_tts(self, debug_flag=False):
        text = urlparse.unquote(self.headers['text'])
        print('Receive text: {}'.format(text))

        response = responser.respond(text)
        print('Response: {}'.format(response))

        voice_generator.generate(text, filename='response.wav')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        with open('response.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def rec_rep_tts(self, debug_flag=False):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        # save the wav file from the client
        with open('receive_from_client.wav', 'wb') as f:
            f.write(data)

        # recognize the wav file
        result = recognizer.recognize('receive_from_client.wav')
        print('Receive wav: {}'.format(result.get('text')))

        # get the response according to the recognized text
        response = responser.respond(result.get('text'))
        print('Response: {}'.format(response))

        # generate the voice for the response text
        voice_generator.generate(response, filename='response.wav')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        # insert the text into the header, encode the text to avoid illegal characters
        self.send_header('rec-result', urlparse.quote(result.get('text')))
        self.send_header('rep-result', urlparse.quote(response))

        # TODO: check if the recognized text has text
        has_text = True
        self.send_header('has-text', str(has_text))

        self.end_headers()

        # send the response wav file back to the client
        with open('response.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def break_conn(self):
        self.close_connection = True



def main():

    print('Loading recognizer...')
    global recognizer
    recognizer = Recognizer()

    print('Loading responser...')
    global responser
    responser = Responser()

    print('Loading voice generator...')
    global voice_generator
    voice_generator = VoiceGenerator()

    print('Testing VoiceGenerator...')
    voice_generator.generate('刚出炉的菠萝油，你也想吃？')

    args = arg_parser()
    print('debug: {}'.format(args))
    # os.chdir(os.path.dirname(__file__))
    httpd = http.server.HTTPServer((args.host, args.port), VoiceServer)
    print('Server started at http://{}:{}'.format(args.host, args.port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()


