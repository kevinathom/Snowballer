# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:50:02 2025
@author: kevinatpenn
Purpose: Ingest seed work IDs
"""

# Read first column of seed_file
seed_ids = pd.read_csv(os.path.join(data_dir, seed_file), sep=',', header=None, usecols=[0])

# Clean work ID values
seed_ids = seed_ids[0].tolist()
seed_ids = [s.replace('https://openalex.org/', '') for s in seed_ids] # Remove web address
seed_ids = [x for x in seed_ids if re.search(r'^[Ww]\d*', x)] # Filter for work ID format
seed_ids = list(set(seed_ids)) # Remove duplicates
