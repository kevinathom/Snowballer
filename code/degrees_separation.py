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
while (
  (dirdegs_dict.get('cited_by') is not None and dirdegs_dict.get('cited_by') != [])
  or (dirdegs_dict.get('cites') is not None and dirdegs_dict.get('cites') != [])
):
  
  cb_multiplier = dirdegs_dict.get('cited_by') is not None and dirdegs_dict.get('cited_by') != []
  if cb_multiplier:
    dirdegs_dict.get('cited_by').pop()
  
  c_multiplier = dirdegs_dict.get('cites') is not None and dirdegs_dict.get('cites') != []
  if c_multiplier:
    dirdegs_dict.get('cites').pop()
    
  # Create a vector for the current degree of separation
  cite_degrees.append(['cited_by'] * cb_multiplier + ['cites'] * c_multiplier)

# Clean up
gc.collect()
