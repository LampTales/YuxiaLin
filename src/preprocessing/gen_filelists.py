import os
import whisper

data_name = 'lin'

file_list_path = 'filelists/' + data_name + '.list'

raw_data_path = 'raw/' + data_name + '/'

model_size = 'medium'
model = whisper.load_model(name=model_size)

def gen_list(file_list_path, raw_data_path):
    file_list = open(file_list_path, 'w')
    
    # deal with all the dirs in raw_data_path
    for dir in os.listdir(raw_data_path):
        lang = dir.split('_')[0]
        speaker = data_name + '_' + lang
        for file in os.listdir(raw_data_path + dir):
            text = model.transcribe(raw_data_path + dir + '/' + file)
            entry = f'./dataset/{data_name}/{dir}/{file}|{speaker}|{lang.upper()}|{text}\n'
            file_list.write(entry)
            print(entry)