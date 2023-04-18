# Typo Fixer

Typo Fixer is a command-line tool that corrects typos in text files and directories. It supports various options such as recursive correction, file extension filters, and automatic saving of changes.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/typo-fixer.git
cd typo-fixer


2. Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

3. Install the required packages

pip3 install -r requirements.txt

Usage
Here are some examples of how to use Typo Fixer:

Fix typos in a single file:

./typo_fixer.py --file input.txt

Fix typos in all files in a directory (non-recursive):

./typo_fixer.py --dir path/to/directory


Fix typos in all files in a directory and its subdirectories (recursive):

./typo_fixer.py --dir path/to/directory -rec


Fix typos only in files with a specific extension in a directory (non-recursive):

./typo_fixer.py --dir path/to/directory --endsw .extension

Fix typos only in files with a specific extension in a directory and its subdirectories (recursive):

./typo_fixer.py --dir path/to/directory -rec --endsw .extension

Automatically save changes without asking for confirmation:

./typo_fixer.py --file input.txt -force

Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

