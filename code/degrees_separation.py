# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:11:53 2025

@author: kevinatpenn
"""

import gc

# Encode degrees of separation
## Initialize objects
cite_degrees = []
deg = 1

## Create vectors for get_works
while cited_by > 0 or cites > 0:
    # Check for 0 or more degrees
    cited_by_deg = min(cited_by, 1)
    cites_deg = min(cites, 1)
    # Create a vector for the current degree of separation
    cite_degrees.append(['cited_by'] * cited_by_deg + ['cites'] * cites_deg)
    # Increment/Decrement counts
    deg += 1
    cited_by -= cited_by_deg
    cites -= cites_deg

# Clean up temporary objects
del cited_by, cited_by_deg, cites, cites_deg, deg
gc.collect()
