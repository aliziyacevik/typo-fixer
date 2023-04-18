#!/usr/bin/env python3

import sys
import os
import argparse
from textblob import TextBlob
from difflib import unified_diff

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def correct_text(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)

def show_diff(original, corrected):
    diff = list(unified_diff(original.splitlines(), corrected.splitlines()))
    for line in diff[2:]:
        print(line)

def process_file(file_path, endsw=None, force=False):
    if endsw is None or file_path.endswith(endsw):
        text = read_file(file_path)
        corrected_text = correct_text(text)
        print(f"Typo corrections for file: {file_path}")
        show_diff(text, corrected_text)

        if force:
            save_changes = True
        else:
            save_changes = input("Save changes? (y/n): ").lower() == "y"

        if save_changes:
            write_file(file_path, corrected_text)
            print(f"Changes saved for file: {file_path}")
        else:
            print(f"Changes discarded for file: {file_path}")

def process_directory(directory_path, recursive=False, endsw=None, force=False):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, endsw, force)
        if not recursive:
            break

def main(args):
    if args.file:
        process_file(args.file, args.endsw, args.force)
    elif args.dir:
        process_directory(args.dir, args.rec, args.endsw, args.force)
    else:
        print("Please provide either --file or --dir flag.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Typo fixer for files and directories")
    parser.add_argument("--file", type=str, help="File to fix typos in")
    parser.add_argument("--dir", type=str, help="Directory containing files to fix typos in")
    parser.add_argument("-rec", action="store_true", help="Recursively process files in subdirectories")
    parser.add_argument("--endsw", type=str, help="File extension filter")
    parser.add_argument("-force", action="store_true", help="Automatically save changes without asking")
    args = parser.parse_args()

    main(args)

