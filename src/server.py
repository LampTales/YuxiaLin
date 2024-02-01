import http.server
import os
import argparse
from urllib import parse as urlparse

from recognize import Recognizer


recognizer = None

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

        # send the wav file back to the client to do the verification
        with open('receive_from_client.wav', 'rb') as f:
            data = f.read()
        self.wfile.write(data)


    def break_conn(self):
        self.close_connection = True



def main():

    print('Loading recognizer...')
    global recognizer
    recognizer = Recognizer()

    args = arg_parser()
    print('debug: {}'.format(args))
    # os.chdir(os.path.dirname(__file__))
    httpd = http.server.HTTPServer((args.host, args.port), VoiceServer)
    print('Server started at http://{}:{}'.format(args.host, args.port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()


