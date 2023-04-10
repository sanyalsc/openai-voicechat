import os

import openai

from speech_to_gpt.audio import record_mic


def main(api_key):
    openai.api_key_path = api_key
    speech = record_mic()
    speech_fi = open(speech, 'rb')
    transcript = openai.Audio.transcribe("whisper-1", speech_fi)
    print(transcript)

if __name__ == '__main__':
    main()
