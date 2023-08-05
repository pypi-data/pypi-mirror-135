#!/usr/bin/env python3
from .config import CONFIG
from .runner import process_file
from argparse import ArgumentParser
from itertools import chain
from pathlib import Path
import argparse


__doc__ = """
Possible invocations:

    fix-my-functions
    python -m fix_my_functions
    poetry run fix-my-functions
    poetry run python -m fix_my_functions
"""


def make_argparser(parser = None) -> ArgumentParser:
    if parser is None:
        parser = ArgumentParser()

    parser_input = parser.add_argument_group("input")
    parser_input.add_argument("files", type=str, nargs="+",
        help="Files to format.")
    parser_input.add_argument("-r", "--recursive", action="store_true",
        help="Recursively format .py files in folders")
    parser_input_mutex = parser_input.add_mutually_exclusive_group(required=True)
    parser_input_mutex.add_argument("-a", "--accept", action="store_true",
        help="Accept and apply all changes.")
    parser_input_mutex.add_argument("-i", "--interactive", action="store_true",
        help="Ask to apply each change.")
    parser_input_mutex.add_argument("-d", "--dry", action="store_true",
        help="Only show unified diff.")

    parser_input.add_argument("--no-diff", action="store_true",
        help="Only show raw output instead of unififed diff, requires --dry.")

    parser = CONFIG.make_argparser(parser)

    class CustomFormatter(
        argparse.RawDescriptionHelpFormatter,
        argparse.ArgumentDefaultsHelpFormatter,
        ): pass
    parser.formatter_class = CustomFormatter
    parser.description = __doc__

    return parser

def main(parser = make_argparser()):
    args = parser.parse_args() # may terminate on --help and such
    if args.no_diff and not args.dry:
        print("ERROR: --no-diff requires --dry")
        return 1

    CONFIG.parse_args(args)

    files = [*map(Path, args.files)]

    if args.recursive:
        files = sorted(set(chain(*(
            file.rglob("*.py")
            if file.is_dir() else
            [file]
            for file in files
        ))))

    for file in files:
        if file.is_dir():
            print(f"Skipping {file}, because it is a directory")
            continue

        if len(files) > 1:
            print(file)

        process_file(file,
            dry         = args.dry,
            interactive = args.interactive,
            accept      = args.accept,
            no_diff     = args.no_diff,
        )

if __name__ == "__main__":
    exit(main() or 0)
