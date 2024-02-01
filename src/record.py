import pyaudio,wave
import numpy as np

def get_word(mindb=6000, delayTime=1.3, filename='test.wav', CHUNK=1024, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=16000):
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
    flag = False            # voice detected flag
    stat = True				# recording flag
    stat2 = False			# voice turning low flag

    tempnum = 0				#tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0

    hasContent = False		# whether the recording has content

    while stat:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.short)
        cur_vol = np.max(audio_data)
        if not flag and cur_vol > mindb:
            flag = True
            print("Voice detected, recording...")
            hasContent = True
            tempnum2=tempnum

        if flag:
            frames.append(data)
            if cur_vol < mindb and not stat2:
                stat2 = True
                tempnum2 = tempnum
                print("Low sound, waiting...")
            if(cur_vol > mindb):
                # go back to recording
                stat2 = False
                tempnum2 = tempnum

            if stat2 and tempnum > tempnum2 + delayTime*15:
                print('time waited: %.2fs, ' % (delayTime) + 'rejudging...')

                if(stat2 and cur_vol < mindb):
                    # stop recording
                    stat = False
                    print("Recording stopped.")
                else:
                    # go back to recording
                    stat2 = False
                    print("recording resumed...")


        # print(str(cur_vol)  +  "      " +  str(tempnum))
        tempnum = tempnum + 1
        if tempnum > 900:	# time out
            stat = False
    print("Done.")

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return hasContent


if __name__ == '__main__':
    get_word()