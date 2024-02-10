import requests



host = '10.16.88.247'
port = 8086

voice_api = '/voice'
def GET_voice():
    url = f'http://{host}:{port}{voice_api}'

    # fill params
    text = '需要加载的所有模型的配置，可以填多个模型，也可以不填模型，等网页成功后手动加载模型'
    model_id = 0
    speaker_name = 'lin_zh'
    sdp_ratio = 0.5
    noise = 0.6
    noise_w = 0.9
    length = 1
    language = 'ZH'
    auto_translate = False
    auto_split = False
    emotion = None
    style_text = None
    style_weight = 0.7

    params = {
        'text': text,
        'model_id': model_id,
        'speaker_name': speaker_name,
        'sdp_ratio': sdp_ratio,
        'noise': noise,
        'noise_w': noise_w,
        'length': length,
        'language': language,
        'auto_translate': auto_translate,
        'auto_split': auto_split,
        'emotion': emotion,
        'style_text': style_text,
        'style_weight': style_weight,
    }

    # send request
    response = requests.get(url, params=params)

    # check response
    print(response.status_code)

    # save the response
    with open('test_bs.wav', 'wb') as f:
        f.write(response.content)



if __name__ == '__main__':
    GET_voice()