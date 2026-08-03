# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:50:02 2025
@author: kevinathom
Purpose: Ingest seed work IDs
"""

# Define functions
def clean_work_ids(ids_list):
  """
  Clean, standardize, and deduplicate OpenAlex work IDs
  
  Args:
    ids (list): Work IDs, potentially mixed with other content
  
  Returns:
    list: Clean work IDs
  """
  # Remove web address prefix that appears in OpenAlex extracts
  ids_list = [i.replace('https://openalex.org/', '') for i in ids_list]
  # Keep only items formatted like work IDs
  ids_list = [x for x in ids_list if re.match(r'[Ww]\d+', x)]
  # Remove duplicates
  ids_list = list(set(ids_list))
  
  return ids_list

# Read first column of seed_file
seed_ids = pd.read_csv(seed_file, sep=',', header=None, usecols=[0])

# Clean and standardize work ID values
seed_ids = clean_work_ids(seed_ids[0].tolist())
