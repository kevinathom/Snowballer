# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:17:17 2025

@author: kevinatpenn
"""

import os
import time
import requests
import pandas as pd
gc

# Load dependencies

# Initialize
## Work entity ID storage for next degree of separation
next_ids = pd.DataFrame({'cit': [], 'id': []})
## Working file directory
os.makedirs(os.path.join(data_dir, 'working'), exist_ok=True)

# Get works cited/citing
## For current degree of separation's works cited_by and/or cites
for cit in cite_degrees[deg - 1]:  # Adjust index for Python (0-based)
    ## For each work entity ID
    for sid in seed_df.loc[(seed_df['cit'] == 'seed') | (seed_df['cit'] == cit), 'id']:
        # Skip if file exists
        file_path = os.path.join(data_dir, 'working', f'{sid}_{cit}.txt')
        if os.path.exists(file_path):
            continue
        
        # Initialize results storage (to file)
        pd.DataFrame(columns=fields_to_return).to_csv(file_path, sep='|', index=False)
        
        # Get result count
        response = requests.get(f"{oal_domain}works", params={
            'mailto': my_email,
            'per-page': 1,
            'page': 1,
            'select': 'id',
            'filter': f"{cit}:{sid}"
        })
        response_data = response.json()
        cit_count = response_data['meta']['count']
        
        # If there are citations
        if cit_count > 0:
            cursor = '*'  # Starts pagination
            ppg = 200  # Results per page
            
            # While there are results remaining
            while cursor:
                time.sleep(0.1)  # Obey public API rate limit of max 10 requests per second
                response = requests.get(f"{oal_domain}works", params={
                    'mailto': my_email,
                    'per-page': ppg,
                    'cursor': cursor,
                    'select': ','.join(fields_to_return),
                    'filter': f"{cit}:{sid}"
                })
                response_data = response.json()
                cursor = response_data['meta'].get('next_cursor')
                
                # Append latest page of results to the results file
                if 'results' in response_data and response_data['results']:
                    pd.DataFrame(response_data['results']).to_csv(file_path, mode='a', sep='|', index=False, header=False)
                    next_ids = pd.concat([next_ids, pd.DataFrame({'cit': [cit] * len(response_data['results']), 'id': [res['id'] for res in response_data['results']]})], ignore_index=True)

# Prepare for next iteration
next_ids['id'] = next_ids['id'].str.replace('https://openalex.org/', '', regex=True)
seed_df = next_ids

# Clean up temporary objects
del cit, cit_count, cursor, next_ids, response_data, response, ppg, sid
gc.collect()
