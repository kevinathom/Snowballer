# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:50:02 2025
@author: kevinatpenn
Purpose: Ingest seed work IDs
"""

# Read first column of seed_file
seed_ids = pd.read_csv(os.path.join(data_dir, seed_file), sep=',', header=None, usecols=[0])

# Clean work ID values
#Add/remove URL string
#Remove entries that aren't IDs