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


class VoiceServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print('POST request received')
        operation = self.headers['Operation']
        print('Operation: {}'.format(operation))
        if operation == 'rec':
            self.recognize()
        elif operation == 'rep':
            self.rec_rep_tts()

    def recognize(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        with open('receive_from_client.wav', 'wb') as f:
            f.write(data)
        result = recognizer.recognize('receive_from_client.wav')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('rec-result', urlparse.quote(result.get('text')))
        self.end_headers()

        # send the wav file back to the client
        with open('receive_from_client.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def rec_rep_tts(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        # save the wav file from the client
        with open('receive_from_client.wav', 'wb') as f:
            f.write(data)

        # recognize the wav file
        result = recognizer.recognize('receive_from_client.wav')
        print('Receive: {}'.format(result.get('text')))

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


