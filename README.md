# openai-voicechat
 
Chat with chatgpt!

##Installation (local only):

$ python -m pip install openai-voicechat

Make sure that python's binary dir is on your sytem path.

You can check this with

$ pip show --files speech-to-gpt

##Usage:

You will need to set your openai api key.  This can be done with

$ chat-with-gpt config --api-key

Or via export per the official openai instructions.

Launch the tool with

$ chat-with-gpt converse

Converse has alternate language options which can be accessed with '--lang'
