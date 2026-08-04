# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:11:53 2025
@author: kevinathom
Purpose: Create lists of direction and degree of separation
  for compatibility with legacy get_works.py process
"""

# Initialize objects
cite_degrees = []

# Create vectors
#try this?: dirdegs_dict.get('cited_by') is not None
#might have an issue with the pop process too
while (('cited_by' in dirdegs_dict and dirdegs_dict['cited_by'] is not None)
       or ('cites' in dirdegs_dict and dirdegs_dict['cites'] is not None)):
  
  cb_multiplier = 'cited_by' in dirdegs_dict or dirdegs_dict['cited_by'] is not None
  if cb_multiplier:
    dirdegs_dict.pop('cited_by')
  
  c_multiplier = 'cites' in dirdegs_dict or dirdegs_dict['cites'] is not None
  if c_multiplier:
    dirdegs_dict.pop('cites')
    
  # Create a vector for the current degree of separation
  cite_degrees.append(['cited_by'] * cb_multiplier + ['cites'] * c_multiplier)

# Clean up
gc.collect()
