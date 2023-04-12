import os
from pathlib import Path

from dotenv import load_dotenv
import openai
import gtts

from speech_to_gpt.audio import record_mic, play_reply

SUPPORTED_LANG = gtts.lang.tts_langs()
LANG_LOOKUP = {v:k for k,v in SUPPORTED_LANG.items()}
#For my In-laws
LANG_LOOKUP['Macedonian'] = 'sr'


def login(api_key):
    """Saves a .env file with login credentials."""
    root = Path(__file__).parent
    with open(root / '.env', 'w') as envfi:
        envfi.write(f"OPENAI_API_KEY={api_key}")
    print("API key stored.")


def main(language='English'):
    """Main App."""
    
    if language not in LANG_LOOKUP.keys():
        raise ValueError(f'{language} not supported.  Supported Languages: {LANG_LOOKUP.keys()}')
    load_dotenv()
    if "OPENAI_API_KEY" not in os.environ:
        raise LookupError("API Key not set.  Set key using the 'config' command.")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    while True:
        speech = record_mic()
        speech_fi = open(speech, 'rb')
        if language=='English':
            transcript = openai.Audio.transcribe("whisper-1", speech_fi)
        else:
            transcript = openai.Audio.translate("whisper-1", speech_fi)
        voice_out = transcript["text"]
        filtered_input = openai.Moderation.create(input=voice_out)['results'][0]
        if not filtered_input['flagged']:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": "You are a friendly conversation bot."},
                {"role": "user", "content": voice_out}
                ]
                )
        if language != 'English':
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": f"You are an English to {language} translator."},
                {"role": "user", "content": f"Translate '{reply['choices'][0]['message']['content']}' to {language}"}
                ]
                )
        else:
            myobj = gtts.gTTS(text=reply['choices'][0]['message']['content'], lang=LANG_LOOKUP[language], slow=False)
        play_reply(myobj)


if __name__ == '__main__':
    main()
