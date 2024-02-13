import http.client
import os
import argparse
from playsound import playsound
import random

from urllib import parse as urlparse
from record import get_word


conn = None

act_rep_list = [
    "怎么了？",
    "有什么事？",
    "有话快说。",
    "有什么要帮忙的？",
]
def random_rep(list):
    return random.choice(list)


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
        f.close()

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
        f.close()

    conn.request('POST', '/rec', headers={'Operation': 'rec', 'Content-Length': length, 'debug': 'True'})
    conn.send(data)

    response = conn.getresponse()
    print(response.status, response.reason)

    result = urlparse.unquote(response.getheader('rec-result'))
    has_text = (response.getheader('has-text') == 'True')

    return has_text, result


def rec(filename='test.wav', save_path='receive_from_server.wav', debug_flag=False):
    with open(filename, 'rb') as f:
        data = f.read()
        length = len(data)
        f.close()

    conn.request('POST', '/rec', headers={'Operation': 'rec', 'Content-Length': length, 'debug': str(debug_flag)})
    conn.send(data)

    response = conn.getresponse()
    print(response.status, response.reason)

    result = urlparse.unquote(response.getheader('rec-result'))
    has_text = (response.getheader('has-text') == 'True')

    with open(save_path, 'wb') as f:
        f.write(response.read())
        f.close()

    return has_text, result


def tts(text, filename='receive_from_server.wav'):
    conn.request('POST', '/tts', headers={'Operation': 'tts', 'Content-Length': len(text), 'text': urlparse.quote(text)})

    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()

    return filename
    

def rep_tts(text, filename='receive_from_server.wav'):
    conn.request('POST', '/p_t', headers={'Operation': 'p_t', 'Content-Length': len(text), 'text': urlparse.quote(text)})

    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()

    return filename


def control_switch(result):
    # TODO: really implement a switch
    rep_needed = True
    rep_text = '晓得了。'

    return rep_needed, rep_text



retry_limit = 3

def run_client(host, port):
    while True:
        global conn
        conn = http.client.HTTPConnection(host, port)

        print('Lin is listening.')

        while not activate():
            print('Activation failed. Retry.')
            continue
        print('Activated!')
        act_rep = random_rep(act_rep_list)
        wav_path = tts(act_rep)
        playsound(wav_path)

        cnt = 0
        print('Conversation start.')
        while cnt < retry_limit:
            has_text, result = get_word_rec()
            if has_text:
                cnt = 0
                rep_needed, rep_text = control_switch(result)
                if rep_needed:
                    wav_path = rep_tts(result)
                else:
                    wav_path = tts(rep_text)
                playsound(wav_path)
            else:
                cnt += 1
                print('No text recognized. Retry: {}'.format(cnt))

        conn.close()

        print('Conversation end.')

        
    

def test1():
    pass




from record import just_record
def rec_test():
    just_record(filename='test.wav')

    args = arg_parser()
    global conn
    conn = http.client.HTTPConnection(args.host, args.port)
    
    has_text, result = rec(filename='test.wav', debug_flag=True)

    print('has_text: {}'.format(has_text))
    print('result: {}'.format(result))
    conn.close()

    



if __name__ == '__main__':
    # run_client('localhost', 8081)
    rec_test()    