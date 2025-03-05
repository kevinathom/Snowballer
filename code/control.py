# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:06:24 2025

@author: kevinatpenn
"""

import os
import pandas as pd
gc

# Set initial information

# Set user email
my_email = 'kevinat@wharton.upenn.edu'

# Set directories
## Data
data_dir = os.path.expanduser('~/Documents/GitHub/Snowballer/data/')
## Code
code_dir = os.path.expanduser('~/Documents/GitHub/Snowballer/code/')

# Set degrees of separation
cited_by = 1
cites = 1

# Set seed work entity ID(s)
seed_ids = ['W3125944002', 'W2762606399']  # hard-coded example

# Set fields to request for works
fields_to_return = ['id', 'doi', 'title', 'publication_year', 'language', 'type', 'is_retracted']


### Run Process ###

# Encode degrees of separation
exec(open(os.path.join(code_dir, 'degrees_separation.py')).read())

# Get works for each degree of separation
## Initialize API domain
oal_domain = 'https://api.openalex.org/'
## Configure work entity IDs for first degree of separation
seed_df = pd.DataFrame({'cit': ['seed'] * len(seed_ids), 'id': seed_ids})

## For each degree of separation
for deg in range(len(cite_degrees)):
    exec(open(os.path.join(code_dir, 'get_works.py')).read())

## Clean up temporary objects
del cite_degrees, deg, fields_to_return, my_email, oal_domain, seed_ids

# De-duplicate results
exec(open(os.path.join(code_dir, 'dedup_works.py')).read())

## Clean up temporary objects
del code_dir, data_dir
gc.collect()
