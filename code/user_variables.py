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

# Define functions
## Show text entry window
def get_text_input(your_title="Input Dialog", your_message="Please enter your response:", initial_value=""):
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
my_email = get_text_input(your_title="Email", your_message="Enter your email address for the OpenAlex API:", initial_value="user@domain.com")

## Set directories
data_dir = open_directory_dialog(your_title = "Select the directory that holds your data files.")
code_dir = open_directory_dialog(your_title = "Select the directory that holds your copy of Snowballer's code files.")

## Set degrees of separation
#Fix prompts for user free text
cited_by = get_text_input(your_title="'Cited By' Degrees", your_message="Enter the degrees of separation for ___:", initial_value="1")
cites = get_text_input(your_title="'Cites' Degrees", your_message="Enter the degrees of separation for ___:", initial_value="1")

## Set seed work entity ID(s)
seed_file = open_file_dialog(your_title = "Select a CSV file containing the work entity ID(s) to use as a starting point.")

## Set fields to request for works
fields_to_return = ['id', 'doi', 'title', 'publication_year', 'language', 'type', 'is_retracted']


# Clean up
gc.collect()