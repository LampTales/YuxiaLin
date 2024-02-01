import http.client
import os
import argparse
from urllib import parse as urlparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to connect', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to connect', type=int, default=8081)
    return parser.parse_args()

def main():
    args = arg_parser()

    # os.chdir(os.path.dirname(__file__))
    conn = http.client.HTTPConnection(args.host, args.port)
    # send the wav to the server
    with open('../lin_voice/zh/信赖触摸.wav', 'rb') as f:
        data = f.read()
        length = len(data)
    conn.request('POST', '/rec', headers={'Operation': 'rec', 'Content-Length': length})
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

if __name__ == '__main__':
    main()