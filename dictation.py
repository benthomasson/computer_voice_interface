#!/usr/bin/env python -u

"""
Usage:
    dictation [options]

Options:
    -h, --help          Show this page
    --debug             Show debug logging
    --verbose           Show verbose logging
"""
from docopt import docopt
import logging
import sys
import os
import speech_recognition as sr
import pyaudio
import time
import subprocess
import string

logger = logging.getLogger('computer')


def parse_args(args):
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    return parsed_args


def recognize_audio(r, source):
    # read the audio data from the default microphone
    try:
        audio_data = r.listen(source, timeout=5)
        # play(audio_data)
        # convert speech to text
        text = r.recognize_whisper(audio_data)
    except sr.WaitTimeoutError:
        text = ""
    return text


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = parse_args(args)

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=8000) as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Ready", file=sys.stderr)
        while True:
            try:
                text = recognize_audio(r, source)
            except KeyboardInterrupt:
                return
            text = text.strip()
            if text == "":
                continue

            print(text)
            # generate_response(text)
            time.sleep(1)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
