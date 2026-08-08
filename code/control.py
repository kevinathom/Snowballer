# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:06:24 2025
@author: kevinathom
Purpose: Orchestrate scripts to perform a citation chase / snowball literature search
"""

# Load dependencies
import gc
import os
import pandas as pd
import shutil
import sys
import time

# Create functions
def resolve_path(relative_path):
  """
  Get the absolute path for a given resource.
  Works for dev and for PyInstaller.
  
  Args:
    relative_path (str): The relative path to the resource
  
  Returns:
    str: The absolute path to the resource
  """
  
  try:
    # PyInstaller creates a temp folder and stores the path in _MEIPASS
    base_path = sys._MEIPASS
    
  except Exception:
    # When developing, set and use the dev path
    os.chdir('C:\\Users\\kevinat\\Documents\\GitHub\\Snowballer\\code') # Repository directory
    base_path = os.path.abspath(".")
    
  return os.path.join(base_path, relative_path)

"""
Run process
"""
# Hard-code code directory
code_dir = resolve_path('')

# Collect initializing details from user
exec(open(os.path.join(code_dir, 'user_variables.py')).read())

# Read seed work IDs
exec(open(os.path.join(code_dir, 'read_seeds.py')).read())

# Get and deduplicate works
oal_domain = 'https://api.openalex.org/' # API domain
working_dir = os.path.join(data_dir, f'snowball_results_{time.strftime("%Y%m%d-%H%M%S")}') # Working file directory
os.makedirs(working_dir, exist_ok=True)
exec(open(os.path.join(code_dir, 'dedup_works.py')).read()) # Load dedup functions
for direction in dirdegs_dict.keys():
  # Initialize work entity IDs for first degree of separation
  next_ids = seed_ids
  for degree in dirdegs_dict.get(direction):
    # Initialize work entity IDs for next degree of separation
    if degree > 1:
      next_ids = future_ids
    future_ids = []
    exec(open(os.path.join(code_dir, 'get_works.py')).read())
    # Concatenate results from each work
    files = list_files(directory=working_dir, file_extension = '.txt')
    join_file_content(
      files_to_join=files,
      input_directory=working_dir,
      file_to_output=f'works_snowball_{direction}_{degree}.csv',
      output_directory=working_dir,
      clean_up=True
    )
    gc.collect()

# Concatenate incremental files and remove the working directory
files = list_files(directory=working_dir, file_extension = '.csv')
join_file_content(
  files_to_join=files,
  input_directory=working_dir,
  to_join_delimiter=',',
  file_to_output=f'{working_dir.replace(data_dir, '').replace('\\', '').replace('/', '')}.csv',
  output_directory=data_dir
)
shutil.rmtree(working_dir, ignore_errors=True)
gc.collect()

# Show completion message
show_completion_message(your_message = "The process is complete.")
