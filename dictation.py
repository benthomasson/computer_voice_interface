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
import speech_recognition as sr
import time
from threading import Thread
from queue import Queue

logger = logging.getLogger("computer")


# background recognizer thread
def recognize_audio_thread(r, queue):
    while True:
        audio_data = queue.get()
        try:
            print("Recognizing...", file=sys.stderr)
            start = time.time()
            text = r.recognize_whisper(audio_data)
            print("Took ", time.time() - start, file=sys.stderr)
        except KeyboardInterrupt:
            return
        text = text.strip()
        if text == "":
            continue

        print(text)


def parse_args(args):
    parsed_args = docopt(__doc__, args)
    if parsed_args["--debug"]:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args["--verbose"]:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    return parsed_args


def listen_for_audio(r, source, queue):
    # read the audio data from the default microphone
    while True:
        try:
            print("Listening...", file=sys.stderr)
            audio_data = r.listen(source, timeout=5)
            queue.put(audio_data)
        except sr.WaitTimeoutError:
            pass


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parse_args(args)

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=8000) as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Ready", file=sys.stderr)
        audio_queue = Queue()
        listener_thread = Thread(target=listen_for_audio,
                                 args=(r, source, audio_queue))
        listener_thread.start()
        recognizer_thread = Thread(target=recognize_audio_thread,
                                   args=(r, audio_queue))
        recognizer_thread.start()

        listener_thread.join()
        recognizer_thread.join()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))