# Snowballer

## Description
The Snowballer tool automates snowball literature searches.

Starting from any set of articles you can find in [OpenAlex](https://openalex.org/), give their OpenAlex work IDs plus a few preferences to Snowballer. Snowballer will use OpenAlex to find and return a list of cited and/or citing works.

## Steps
1. Set up your seed works (the starting article or articles for your snowball search)  
	1. [Search OpenAlex](https://openalex.org/) for your seed works.  
	1. Either export OpenAlex search results to a CSV file *or* create your own CSV file with OpenAlex work IDs in the first column.  
1. Download the Python files from (Snowballer's code directory)[https://github.com/kevinatpenn/Snowballer/tree/main/code].  
	1. Open `control.py` and enter your preferences under *Set initial information*.  
	1. Run `control.py`. You should receive a new file listing the works Snowballer found.  
