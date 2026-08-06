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
    file_extension (str): Any string to match at the end of a file
  
  Returns:
    list: File names as strings
  """
  files = [f for f in os.listdir(directory) if f.lower().endswith(file_extension)]
  return files

def join_file_content(files_to_join, input_directory=os.getcwd(), to_join_delimiter='|', file_to_output='joined.csv', output_directory=os.getcwd(), output_delimiter=',', clean_up=False):
  """
  Joins delimited files and deduplicates rows.
  
  Args:
    files_to_join (list): Strings containing the names of each file to join
    input_directory (str): File path that holds each file in files_to_join
    to_join_delimiter (str): Separater to use in delimited input files
    file_to_output (str): Name, including file extension, to give the joined output file
    output_directory (str): File path to hold the joined output file
    output_delimiter (str): Separater to use in delimited output file
    
  Returns:
    None, but it outputs a delimited file
  """
  if files_to_join:
    # Load and de-duplicate first file
    file = 0
    content = pd.read_csv(os.path.join(input_directory, files_to_join[file]), sep=to_join_delimiter)
    
    # Load and de-duplicate remaining files
    while file < len(files_to_join) - 1:
      file += 1
      next_df = pd.read_csv(os.path.join(input_directory, files_to_join[file]), sep=to_join_delimiter)
      content = pd.concat([content, next_df], ignore_index=True).drop_duplicates()
    
    # Save results to file
    works.to_csv(os.path.join(output_directory, file_to_output), sep=output_delimiter, index=False)
  
  if clean_up:
    for file in files_to_join:
      os.remove(os.path.join(input_directory, file))

# List TXT files in data directory (legacy)
fls = list_files(directory=working_dir, file_extension='.txt')

# De-duplicate results (legacy)
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

# Clean up temporary directory (legacy)
for file in fls:
    os.remove(os.path.join(working_dir, file))

gc.collect()
