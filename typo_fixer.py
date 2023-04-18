#!/usr/bin/env python3

import sys
import os
import argparse
import json
import csv
import re
from textblob import TextBlob
from difflib import unified_diff
from chardet.universaldetector import UniversalDetector

correction_engines = {
    "textblob": TextBlob
}

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def detect_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def correct_text(text, engine="textblob"):
    if engine not in correction_engines:
        raise ValueError(f"Unsupported correction engine: {engine}")

    blob = correction_engines[engine](text)
    corrected_text = blob.correct()
    return str(corrected_text)

def show_diff(original, corrected):
    diff = list(unified_diff(original.splitlines(), corrected.splitlines()))
    typos = []

    for line in diff[2:]:
        if line.startswith("+ "):
            typo = line[2:]
            typos.append(typo)

    return typos

def exclude_text(text, regex):
    if regex:
        return re.sub(regex, "", text)
    return text

def process_file(file_path, endsw=None, force=False, engine="textblob", export=None, regex=None):
    if endsw is None or file_path.endswith(endsw):
        text = read_file(file_path)
        text = exclude_text(text, regex)
        corrected_text = correct_text(text, engine)

        typos = show_diff(text, corrected_text)
        print(f"Typo corrections for file: {file_path}")
        print("\n".join(typos))

        if export:
            export_data = {
                "file": file_path,
                "typos": typos
            }

            if export.lower().endswith(".json"):
                with open(export, "a") as f:
                    json.dump(export_data, f)
                    f.write("\n")

            elif export.lower().endswith(".csv"):
                fieldnames = ["file", "typo"]
                with open(export, "a", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for typo in typos:
                        writer.writerow({"file": file_path, "typo": typo})

        if force:
            save_changes = True
        else:
            save_changes = input("Save changes? (y/n): ").lower() == "y"

        if save_changes:
            write_file(file_path, corrected_text)
            print(f"Changes saved for file: {file_path}")
        else:
            print(f"Changes discarded for file: {file_path}")

def process_directory(directory_path, recursive=False, endsw=None, force=False, engine="textblob", export=None, regex=None):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, endsw, force, engine, export, regex)
        if not recursive:
            break

def main():
    parser = argparse.ArgumentParser(description="Fix typos in text files.")
    parser.add_argument("--file", help="Path to a single file.")
    parser.add_argument("--dir", help="Path to a directory containing files.")
    parser.add_argument("-rec", action="store_true", help="Recursively process subdirectories.")
    parser.add_argument("--endsw", help="Process only files with the specified extension.")
    parser.add_argument("-force", action="store_true", help="Automatically save changes without prompting.")
    parser.add_argument("--engine", default="textblob", choices=list(correction_engines.keys()), help="Choose a typo correction engine.")
    parser.add_argument("--export", help="Export typo report in JSON or CSV format.")
    parser.add_argument("--regex", help="Regular expression pattern to exclude text from typo correction.")
    args = parser.parse_args()

    if args.file:
        process_file(args.file, args.endsw, args.force, args.engine, args.export, args.regex)

    if args.dir:
        process_directory(args.dir, args.rec, args.endsw, args.force, args.engine, args.export, args.regex)

if __name__ == "__main__":
    main()

