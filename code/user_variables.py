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
import sys

# Define functions
def get_string_input(your_title="String Input", your_message="Please enter your text:", initial_value="", validate=""):
  """
  Open a simple dialog box to get email-formatted input from the user.
  
  Args:
    your_title (str): The title of the dialog box
    your_message (str): The message displayed to the user
    initial_value (str): The initial value in the text field
      
  Returns:
    str or None: The user's input, or None if canceled or invalid
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
  
  if validate.lower() == ""
    return None
  elif validate.lower() == "email":
    # Confirm email format
    if user_input == "user@domain.com":
      return None
    elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_input) is None:
      return None
  else:
    return user_input

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


"""
Prompt user for variables
"""
# Set user email
my_email = get_string_input(your_title="Email", your_message="Enter your email address for the OpenAlex API.", initial_value="user@domain.com", validate="email")
if not ('my_email' in locals() or 'my_email' in globals()) or my_email == None:
  my_email = ""

# Set user API key
my_key = get_string_input(your_title="API key", your_message="Enter your API key for the OpenAlex API.", initial_value="YOUR_KEY")
if not ('my_key' in locals() or 'my_key' in globals()) or my_key == None:
  my_key = ""

# Set seed work entity ID(s)
seed_file = open_file_dialog(your_title = "Select a CSV file containing the work entity ID(s) to use as a starting point.")
if not ('seed_file' in locals() or 'seed_file' in globals()) or seed_file == None or seed_file == '':
  show_completion_message(your_title="Process Cancelled", your_message="Did not receive a work entity ID file.")
  sys.exit(1) # Terminate with code 1, no valid seed file

# Set degrees of separation
dirdegs_dict = {
  'cited_by': get_integer_input(your_title="'Cited By' Degrees", your_message="This tool will identify works cited by the work(s) you specify.\n" + \
                                "How many degrees of separation do you want to retrieve?\n" + \
                                "(e.g.: Enter 2 to find works cited by the work(s) you provide\n" + \
                                "plus works cited by those works.)", initial_value="1"),
  'cites': get_integer_input(your_title="'Cites' Degrees", your_message="This tool will identify works that cite the work(s) you specify.\n" + \
                             "How many degrees of separation do you want to retrieve?\n" + \
                             "(e.g.: Enter 2 to find works that cite the work(s) you provide\n" + \
                             "plus works that cite those works.)", initial_value="1")
}
if (
  not ('dirdegs_dict' in locals() or 'dirdegs_dict' in globals())
  or ((dirdegs_dict.get('cited_by') is None or dirdegs_dict['cited_by'] == '' or dirdegs_dict['cited_by'] == 0)
      and (dirdegs_dict.get('cites') is None or dirdegs_dict['cites'] == '' or dirdegs_dict['cites'] == 0)
  )
):
  show_completion_message(your_title="Process Cancelled", your_message="No degrees of separation were set.")
  sys.exit(4) # Terminate with code 4, no degrees of separation
for key in dirdegs_dict.copy(): # Copy avoids a RuntimeError after changing the dictionary while iterating
  if dirdegs_dict[key] < 1:
    dirdegs_dict.pop(key)
  else:
    dirdegs_dict[key] = list(range(1, dirdegs_dict[key]+1))

## Set directories
data_dir = open_directory_dialog(your_title = "Select a directory to hold working and results files.")
if not ('data_dir' in locals() or 'data_dir' in globals()) or data_dir == None or data_dir == '':
  show_completion_message(your_title="Process Cancelled", your_message="Did not receive a directory for data.")
  sys.exit(2) # Terminate with code 2, no valid data directory

#code_dir = open_directory_dialog(your_title = "Select the directory that holds your copy of Snowballer's code files.")

## Set fields to request for works
fields_to_return = ['id', 'doi', 'title', 'publication_year', 'language', 'type', 'is_retracted']


# Clean up
gc.collect()
