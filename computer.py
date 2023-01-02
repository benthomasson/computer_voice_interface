#!/usr/bin/env python -u

"""
Usage:
    computer [options]

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from docopt import docopt
import logging
import sys
import os
import json
import speech_recognition as sr
import pyaudio
import time
import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = os.environ.get('API_KEY')


# Set the model and prompt
model_engine = "text-davinci-003"
prompt = "Hello"

# Set the maximum number of tokens to generate in the response
max_tokens = 128


logger = logging.getLogger('computer')

def play(audio_data):

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=8000, output=True)
    stream.write(audio_data.frame_data)
    stream.stop_stream()
    stream.close()
    p.terminate()



def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=8000) as source:
        r.adjust_for_ambient_noise(source, duration=5)
        while True:
            # read the audio data from the default microphone
            print("Recording...")
            audio_data = r.record(source, duration=5)
            #play(audio_data)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_whisper(audio_data)

            # Generate a response
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=text,
                max_tokens=1024,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # Print the response
            print(completion.choices[0].text)
            os.system(f'say "{completion.choices[0].text}"')
            time.sleep(1)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))

