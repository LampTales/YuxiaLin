import http.client
import os
import argparse
from playsound import playsound

from urllib import parse as urlparse
from record import get_word


conn = None

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-i', help='host to connect', type=str, default='localhost')
    parser.add_argument('--port', '-p', help='port to connect', type=int, default=8081)
    return parser.parse_args()

def activate():
    return True

def rec_rep_tts():
    pass

def go_on():
    pass


def run_client(host, port):
    

    while True:
        global conn
        conn = http.client.HTTPConnection(host, port)

        while not activate():
            continue

        get_word()

        while True:
            rec_rep_tts()

            if not go_on():
                break

    # !!! This structrue is wrong, the judgement should be all thrown to the server side, but I am too sleepy to fix it now
    # also, I haven't test the conn yet, I start to get too many things to do, maybe I should keep a log to follow the progress




        
    

def main():
    wav_path = 'test.wav'

    get_word(filename=wav_path)

    args = arg_parser()

    conn = http.client.HTTPConnection(args.host, args.port)
    # send the wav to the server
    # wav_path = '../lin_voice/zh/信赖触摸.wav'
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

    # play the wav
    playsound('./receive_from_server.wav')


def play_test():
    # playsound('../lin_voice/zh/信赖触摸.wav')
    playsound('receive_from_server.wav')



if __name__ == '__main__':
    main()
    # play_test()