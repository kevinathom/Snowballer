# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:17:17 2025
@author: kevinatpenn
Purpose: Retrieve works at a given degree of separation
"""

# Load dependencies
import time
import requests

"""
Set initial information
"""

# Work entity ID storage for next degree of separation
next_ids = pd.DataFrame({'cit': [], 'id': []})
# Working file directory
os.makedirs(os.path.join(data_dir, 'working'), exist_ok=True)

"""
Get works cited by and/or citing
    the current degree of separation's works
"""
# For each preference in cite_degrees
for cit in cite_degrees[deg]:
    # For each work entity ID
    for sid in seed_ids.loc[(seed_ids['cit'] == 'seed') | (seed_ids['cit'] == cit), 'id']:
        # Skip if file exists
        file_path = os.path.join(data_dir, 'working', f'{sid}_{cit}.txt')
        while os.path.exists(file_path):
            continue
        
        # Initialize results storage (to file)
        pd.DataFrame(columns=fields_to_return).to_csv(file_path, sep='|', index=False)
        
        # Get result count
        response = requests.get(f'{oal_domain}works?mailto={my_email}&per-page=1&page=1&select=id&filter={cit}:{sid}')
        response_data = response.json()
        cit_count = response_data['meta']['count']
        
        # If there are citations
        if cit_count > 0:
            cursor = '*'  # Starts pagination
            ppg = 200  # Results per page
            
            # While there are results remaining
            while cursor:
                time.sleep(0.1)  # Obey public API rate limit of max 10 requests per second
                response = requests.get(f'{oal_domain}works?mailto={my_email}&per-page={ppg}&cursor={cursor}&select={",".join(fields_to_return)}&filter={cit}:{sid}')
                response_data = response.json()
                cursor = response_data['meta'].get('next_cursor')
                
                # Append latest page of results to the results file
                if len(response_data['results']) > 0:
                    pd.DataFrame(response_data['results']).to_csv(file_path, mode='a', sep='|', index=False, header=False)
                    next_ids = pd.concat([next_ids, pd.DataFrame({'cit': [cit] * len(response_data['results']), 'id': [res['id'] for res in response_data['results']]})], ignore_index=True)

# Prepare for next iteration
next_ids['id'] = next_ids['id'].str.replace('https://openalex.org/', '', regex=True)
seed_df = next_ids

# Clean up temporary objects
del cit, cit_count, cursor, next_ids, response_data, response, ppg, sid
gc.collect()
