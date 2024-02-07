import os
import whisper

file_list_path = 'filelists/lin.list'

raw_data_path = 'raw/'

model_size = 'medium'
model = whisper.load_model(name=model_size)

def gen_list(file_list_path, raw_data_path):
    file_list = open(file_list_path, 'w')
    