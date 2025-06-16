# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:06:24 2025
@author: kevinathom
Purpose: Orchestrate scripts to perform a citation chase / snowball literature search
"""

# Load dependencies
import os
import sys
import pandas as pd
import gc

# Create directory resolver function
def resolve_path(relative_path):
  """Get absolute path to resource, works for dev and for PyInstaller"""
  
  try:
    # PyInstaller creates a temp folder and stores the path in _MEIPASS
    base_path = sys._MEIPASS
    
  except Exception:
    # When developing, set and use the dev path
    os.chdir('C:\\Users\\kevinat\\Documents\\GitHub\\Snowballer\\code') # Repository directory
    base_path = os.path.abspath(".")
    
  return os.path.join(base_path, relative_path)

# Hard-code code directory
code_dir = resolve_path('')

# Collect initializing details from user
exec(open(os.path.join(code_dir, 'user_variables.py')).read())

# Encode degrees of separation
exec(open(os.path.join(code_dir, 'degrees_separation.py')).read())

# Read seed work IDs
exec(open(os.path.join(code_dir, 'read_seeds.py')).read())

# Get works for each degree of separation
# Initialize API domain
oal_domain = 'https://api.openalex.org/'
# Configure work entity IDs for first degree of separation
seed_ids = pd.DataFrame({'cit': ['seed'] * len(seed_ids), 'id': seed_ids})

# For each degree of separation
for deg in range(len(cite_degrees)):
    exec(open(os.path.join(code_dir, 'get_works.py')).read())

# Clean up temporary objects
del cite_degrees, deg, fields_to_return, my_email, oal_domain, seed_ids

# De-duplicate results
exec(open(os.path.join(code_dir, 'dedup_works.py')).read())

# Clean up temporary objects
del code_dir, data_dir
gc.collect()

# Show completion message
show_completion_message(your_message = "The process is complete.")
