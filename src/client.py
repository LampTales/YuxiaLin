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


def activate(filename='test.wav'):
    if not get_word(filename=filename):
        return False
    
    with open(filename, 'rb') as f:
        data = f.read()
        length = len(data)

    conn.request('POST', '/act', headers={'Operation': 'act', 'Content-Length': length})
    conn.send(data)

    response = conn.getresponse()
    print(response.status, response.reason)

    activate = (response.getheader('activate') == 'True')

    return activate


def get_word_rec(filename='test.wav'):
    if not get_word(filename=filename):
        return False
    
    with open(filename, 'rb') as f:
        data = f.read()
        length = len(data)

    conn.request('POST', '/rec', headers={'Operation': 'rec', 'Content-Length': length})
    conn.send(data)

    response = conn.getresponse()
    print(response.status, response.reason)

    result = urlparse.unquote(response.getheader('rec-result'))
    has_text = (response.getheader('has-text') == 'True')

    return has_text, result
    

def rep_tts(text, filename='receive_from_server.wav'):
    conn.request('POST', '/p_t', headers={'Operation': 'p_t', 'Content-Length': len(text), 'text': text})

    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    with open(filename, 'wb') as f:
        f.write(data)

    return filename



retry_limit = 3

def run_client(host, port):
    while True:
        global conn
        conn = http.client.HTTPConnection(host, port)

        while not activate():
            continue

        cnt = 0
        while cnt < retry_limit:
            has_text, result = get_word_rec()
            if has_text:
                wav_path = rep_tts(result)
                playsound(wav_path)
            else:
                cnt += 1

        conn.close()

        
    

def test1():
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


def test2():
    global conn
    conn = http.client.HTTPConnection('localhost', 8081)

    path = rep_tts('新鲜出炉的菠萝油，你也想吃？')

    playsound(path)


from record import just_record
def test3():
    just_record()



if __name__ == '__main__':
    # run_client('localhost', 8081)
    # test2()
    test3()