# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:19:43 2025

@author: kevinatpenn
"""

import os
import pandas as pd
gc

# List TXT files in data directory
working_dir = os.path.join(data_dir, 'working')
fls = [f for f in os.listdir(working_dir) if f.lower().endswith('.txt')]

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
    
    # Save results (to file)
    works.to_csv(os.path.join(data_dir, 'all_works.txt'), sep='|', index=False)

# Clean up temporary objects
for file in fls:
    os.remove(os.path.join(working_dir, file))
os.rmdir(working_dir)

del fl, fls, works
gc.collect()
