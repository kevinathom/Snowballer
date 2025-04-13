# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 17:36:06 2025
@author: kevinathom
Purpose: Collect initializing details from user
"""

# Load dependencies
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import re

# Define functions
## Show text entry window
def get_email_input(your_title="Email Input", your_message="Please enter your email address:", initial_value="user@domain.com"):
    """
    Open a simple dialog box to get text input from the user.
    
    Args:
        your_title (str): The title of the dialog box
        your_message (str): The message displayed to the user
        initial_value (str): The initial value in the text field
        
    Returns:
        str or None: The user's input, or None if canceled
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the input dialog and get the user's response
    user_input = simpledialog.askstring(
        title=your_title,
        prompt=your_message,
        initialvalue=initial_value
    )
    # Clean up the tkinter instance
    root.destroy()
    
    # Confirm email format
    if user_input == "user@domain.com":
        return None
    elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_input) is None:
        return None
    else:
        return user_input

## Show integer entry window
def get_integer_input(your_title="Integer Input", your_message="Please enter a number:", initial_value="1", min_value=0, max_value=None):
    """
    Open a dialog box to get an integer input from the user.
    
    Args:
        your_title (str): The title of the dialog box
        your_message (str): The message displayed to the user
        initial_value (int, optional): Initial value in the field
        min_value (int, optional): Minimum acceptable value
        max_value (int, optional): Maximum acceptable value
        
    Returns:
        str or None: The user's input, or None if canceled or invalid
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the input dialog and get the user's response
    user_input = simpledialog.askinteger(
        title=your_title,
        prompt=your_message,
        minvalue=min_value,
        maxvalue=max_value,
        initialvalue=initial_value
    )
    # Clean up the tkinter instance
    root.destroy()
    return user_input

## Show file/directory selection window
def open_file_dialog(your_title="Select a file"):
    """
    Open a file dialog box to get a file path from the user.
    
    Args:
        your_title (str): The title of the dialog box
        
    Returns:
        str or None: The user's input, or None if canceled
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the file dialog and get the selected file path
    file_path = filedialog.askopenfilename(
        title=your_title,
        filetypes=(
            ("Comma-separated values", "*.csv"),
        )
    )
    # Clean up the tkinter instance
    root.destroy()
    return file_path

def open_directory_dialog(your_title="Select a directory"):
    """
    Open a directory dialog box to get a directory path from the user.
    
    Args:
        your_title (str): The title of the dialog box
        
    Returns:
        str or None: The user's input, or None if canceled
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the directory dialog and get the selected directory path
    directory_path = filedialog.askdirectory(
        title = your_title,
        mustexist = True
    )# + "/"
    # Clean up the tkinter instance
    root.destroy()
    return directory_path

## Show completion message window
def show_completion_message(your_title="Process Complete", your_message="The process is complete."):
    """
    Open a window to show a message.
    
    Args:
        your_title (str): The title of the dialog box
        your_message (str): The message displayed inside the dialog box
        
    Returns:
        Not applicable
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the message
    messagebox.showinfo(your_title, your_message)
    # Clean up the tkinter instance
    root.destroy()


# Prompt user for variables
## Set user email
my_email = get_email_input(your_title="Email", your_message="Enter your email address for the OpenAlex API:")

## Set directories
data_dir = open_directory_dialog(your_title = "Select the directory that holds your data files.")
code_dir = open_directory_dialog(your_title = "Select the directory that holds your copy of Snowballer's code files.")

## Set degrees of separation
cited_by = get_integer_input(your_title="'Cited By' Degrees", your_message="This tool will identify works cited by the work(s) you specify. How many degrees of separation do you want to retrieve? (e.g.: Enter 2 to find works cited by the work(s) you provide plus works sited by those works.)", initial_value="1")
cites = get_integer_input(your_title="'Cites' Degrees", your_message="This tool will identify works that cited the work(s) you specify. How many degrees of separation do you want to retrieve? (e.g.: Enter 2 to find works that cite the work(s) you provide plus works that site those works.)", initial_value="1")

## Set seed work entity ID(s)
seed_file = open_file_dialog(your_title = "Select a CSV file containing the work entity ID(s) to use as a starting point.")

## Set fields to request for works
fields_to_return = ['id', 'doi', 'title', 'publication_year', 'language', 'type', 'is_retracted']


# Clean up
gc.collect()