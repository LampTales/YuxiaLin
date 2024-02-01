import http.client
import os
import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to connect', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to connect', type=int, default=8084)
    return parser.parse_args()

def main():
    args = arg_parser()

    os.chdir(os.path.dirname(__file__))
    conn = http.client.HTTPConnection(args.host, args.port)
    conn.request('POST', '/rec', headers={'Operation': 'rec'})
    # send the wav to the server
    with open('../lin_voice/zh/信赖触摸.wav', 'rb') as f:
        data = f.read()
    conn.send(data)
    response = conn.getresponse()
    print(response.status, response.reason)
    print(response.getheaders())
    result = response.getheader('rec-result')
    print(result)
    # receive the wav from the server
    data = response.read()
    with open('receive_from_server.wav', 'wb') as f:
        f.write(data)

    conn.close()

    # end the connection
        