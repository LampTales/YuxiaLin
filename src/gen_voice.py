from paddlespeech.cli.tts.infer import TTSExecutor

tts = TTSExecutor()

wav_file = tts(
    text='新鲜出炉的菠萝油，你也想吃？',
    output='out.wav'
)