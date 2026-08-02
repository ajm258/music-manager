#!/usr/bin/env python3

import argparse

from app.database import Database
from app.ingest import find_audio_files
from app.pipeline import process


def ingest(path):

    db = Database()

    processed = 0
    failed = 0

    for file in find_audio_files(path):

        print(f"Processing: {file}")

        try:

            track = process(file)

            db.save_track(track)

            processed += 1

        except Exception as e:

            failed += 1

            print(e)

    db.close()

    print()
    print("Finished")
    print(f"Processed : {processed}")
    print(f"Failed    : {failed}")


def main():

    parser = argparse.ArgumentParser(
        prog="musicctl"
    )

    sub = parser.add_subparsers(dest="command")

    ingest_cmd = sub.add_parser("ingest")

    ingest_cmd.add_argument("path")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
