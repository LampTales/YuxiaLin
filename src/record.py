import pyaudio,wave
import numpy as np

def get_word(mindb=2000, delayTime=1.3, filename='test.wav', CHUNK=1024, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=16000):
    '''
    mindb: the minimum volume to start recording
    delayTime: the time to wait after the volume drops below mindb
    filename: the name of the file to save the recording to
    CHUNK: the size of the audio buffer
    FORMAT: the audio format
    CHANNELS: the number of audio channels
    RATE: the sample rate
    '''

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Listening...")

    frames = []
    flag = False            # Voice detected flag
    stat = True				#判断是否继续录音
    stat2 = False			#判断声音小了

    tempnum = 0				#tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0

    while stat:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.short)
        cur_vol = np.max(audio_data)
        if not flag and cur_vol > mindb:
            flag = True
            print("Voice detected, recording...")
            tempnum2=tempnum

        if flag:
            frames.append(data)
            if cur_vol < mindb and not stat2:
                stat2 = True
                tempnum2 = tempnum
                print("Low sound, waiting...")
            if(cur_vol > mindb):
                stat2 = False
                tempnum2 = tempnum
                # go back to recording

            if stat2 and tempnum > tempnum2 + delayTime*15:
                print("间隔%.2lfs后开始检测是否还是小声"%delayTime)
                if(stat2 and cur_vol < mindb):
                    stat = False
                    #还是小声，则stat=True
                    print("小声！")
                else:
                    stat2 = False
                    print("大声！")


        print(str(cur_vol)  +  "      " +  str(tempnum))
        tempnum = tempnum + 1
        if tempnum > 600:	# time out
            stat = False
    print("录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    get_word()