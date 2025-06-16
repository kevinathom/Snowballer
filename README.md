# Snowballer

## Description
The Snowballer tool automates snowball literature searches.

Starting from any set of articles you can find in [OpenAlex](https://openalex.org/), give their OpenAlex work IDs plus a few preferences to Snowballer. Snowballer will use OpenAlex to find and return a list of cited and/or citing works.

## Steps
1. Set up your seed works (the starting article or articles for your snowball search)  
	1. [Search OpenAlex](https://openalex.org/) for your seed works.  
	1. Either export OpenAlex search results to a CSV file *or* create your own CSV file with OpenAlex work IDs in the first column.  
1. Download either [Snowballer.exe](https://penno365-my.sharepoint.com/:u:/g/personal/kevinat_upenn_edu/EaXG4DDaKVFMp55Tk-7clPkBSc7_iwOS5_-qY0Mz3ma73w?e=Jf6ht5) or the Python files from [Snowballer's code directory](https://github.com/kevinatpenn/Snowballer/tree/main/code).  
	1. If using the Python files, open `control.py` and update the hard-coded variable `code_dir` to reflect the file path for your local copy of the code files.  
	1. Run either Snowballer.exe (on Windows) or `control.py`. After responding to some prompts, you should receive a new file listing the works Snowballer found.  
