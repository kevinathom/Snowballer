# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:19:43 2025
@author: kevinathom
Purpose: Remove duplicate works and consolidate files
"""

# List unique direction-degree values
#import re
#dirdegs = set([re.findall(r'W\d+_(cite[a-z_]+_\d+)\.txt', f) for f in fls]) #not a flat list

def list_files(directory, file_extension = ''):
  """
  Lists files in a given directory. Limits results to files that match a file
  extension (case insensitive) if provided or all files if not. Not recursive.
  
  Args:
    directory (str): Directory to search for files
    file_extension (str): 
  
  """
  files = [f for f in os.listdir(directory) if f.lower().endswith(file_extension)]
  return files

# List TXT files in data directory
fls = list_files(directory=working_dir, file_extension='.txt')

# De-duplicate results
if fls:
    # Load and de-duplicate first file
    fl = 0
    works = pd.read_csv(os.path.join(working_dir, fls[fl]), sep='|')
    works = works.drop_duplicates()
    
    # Handle remaining files
    while fl < len(fls) - 1:
        fl += 1
        next_df = pd.read_csv(os.path.join(working_dir, fls[fl]), sep='|')
        works = pd.concat([works, next_df], ignore_index=True).drop_duplicates()
    
    # Save results (to consolidated file)
    works.to_csv(os.path.join(working_dir, f'works_snowball_{direction}_{degree}.csv'), sep=',', index=False)

# Clean up temporary directory
for file in fls:
    os.remove(os.path.join(working_dir, file))

gc.collect()
