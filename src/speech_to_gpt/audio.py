from io import BytesIO

import wave
import pyaudio
import keyboard
import pygame

TMP_AUDIO_FILEPATH='tmp.wav'


def play_reply(reply):
    mp3_fi = BytesIO()
    reply.write_to_fp(mp3_fi)
    pygame.init()
    pygame.mixer.init()
    mp3_fi.seek(0)
    pygame.mixer.music.load(mp3_fi)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def record_mic():
    """
    Records the mic and saves audio.
    
    Mostly from realpython.com
    """
    # set the chunk size of 1024 samples
    chunk = 1024
    # sample format
    FORMAT = pyaudio.paInt16
    channels = 1
    # 44100 samples per second
    sample_rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    print('press and hold "t" to record audio.')
    pressed = False
    while True:
        if keyboard.is_pressed("t"):
            data = stream.read(chunk)
            frames.append(data)
            pressed = True
        else:
            if pressed == True:
                break

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    #Can't pipe bytes directly into transcribe.
    #Need to use a tmp file for now...

    with wave.open(TMP_AUDIO_FILEPATH, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return TMP_AUDIO_FILEPATH
