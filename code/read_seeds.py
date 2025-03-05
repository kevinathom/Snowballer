# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:50:02 2025
@author: kevinatpenn
Purpose: Read in seed work IDs
"""

seed_ids = pd.read_csv(os.path.join(data_dir, seed_file), sep=',', header=None)

# Clean work ID values
#Add/remove URL string
#Remove entries that aren't IDs