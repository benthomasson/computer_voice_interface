#!/usr/bin/env python3

"""
Usage:
    summarize [options] <text-file>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from docopt import docopt
import logging
import os
import sys
import openai
import gpt3

logger = logging.getLogger("summarize")

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = os.environ.get("API_KEY")


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args["--debug"]:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args["--verbose"]:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    with open(parsed_args["<text-file>"]) as f:
        text = f.read()

    prompt = "Summarize this text: " + text

    print(gpt3.generate_response(prompt))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
