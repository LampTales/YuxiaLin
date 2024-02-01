import http.server
import os
import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to listen', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to listen', type=int, default=8084)
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
        with open('out.wav', 'wb') as f:
            f.write(data)
        result = recognize(model, 'out.wav')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(result.get('text').encode('utf-8'))

    def break_conn(self):
        self.close_connection = True



def main():
    args = arg_parser()

    model = whisper.load_model(name='small', device='cpu')
    os.chdir(os.path.dirname(__file__))
    httpd = http.server.HTTPServer((args.host, args.port), VoiceServer)
    print('Server started at http://{}:{}'.format(args.host, args.port))
    httpd.serve_forever()


