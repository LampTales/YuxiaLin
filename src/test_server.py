import http.client
import os
import argparse
from urllib import parse as urlparse
# from record import get_word

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
        



if __name__ == '__main__':
    main()