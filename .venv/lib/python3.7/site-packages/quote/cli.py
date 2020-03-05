import argparse
import itertools
import random
import threading
import time

from .quote import quote
from .spinner import Spinner


def random_search(search):
    """Return one random quote result from a search

    Params:

    - search (str): Search term
    """
    results = quote(search)
    random_quote = random.choice(results)["quote"]
    return random_quote


def colour(string):
    """Paint it red!"""
    string = f"\033[31m{string}\033[0m"
    return string


def cli():
    """Retrieve a random quote from Goodreads

    Examples:

    ```
    >>> max@mbp$ quote 'alain de botton'
    People only get really interesting when they start to rattle the bars of their cages.

    >>> max@mbp$ quote shakespeare
    Though she be but little, she is fierce!
    ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("search", nargs="?")
    args = parser.parse_args()
    spinner = Spinner()
    spinner.start()
    random_quote = colour(random_search(args.search))
    spinner.stop()
    return random_quote


if __name__ == "__main__":
    cli()
