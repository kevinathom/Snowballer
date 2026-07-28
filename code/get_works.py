# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:17:17 2025
@author: kevinatpenn
Purpose: Retrieve works at a given degree of separation
"""

# Load dependencies
import time
from datetime import datetime, timezone, timedelta
import requests

# Define functions
## Show text entry window
def get_wait_permission(your_title="Process Paused", your_message="Do you want to wait?"):
    """
    Open a dialog window prompting asking the user whether to wait.

    Args:
        your_title (str): The title of the dialog box
        your_message (str): The yes/no question displayed to the user

    Returns:
        bool: True if the user clicks Yes (wait), False if the user clicks No (end process)
    """
    # Initialize then hide tkinter
    root = tk.Tk()
    root.withdraw()
    # Show the yes/no dialog and get the user's response
    result = messagebox.askyesno(
        title=your_title,
        message=your_message
    )
    # Clean up the tkinter instance
    root.destroy()
    return result  # True = Yes (wait), False = No (end process)

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
    
    # Clean cit value
    if not isinstance(cit, str):
        cit = cit[0]
    
    # For each work entity ID
    for sid in seed_ids.loc[(seed_ids['cit'] == 'seed') | (seed_ids['cit'] == cit), 'id']:
        
        # Skip if file exists
        file_path = os.path.normpath(os.path.join(data_dir, 'working', f'{sid}_{cit}.txt'))
        while os.path.exists(file_path):
            continue
        
        # Initialize results storage (to file)
        pd.DataFrame(columns=fields_to_return+['direction','degrees']).to_csv(file_path, sep='|', index=False)
        
        # Get result count
        response = requests.get(f'{oal_domain}works?mailto={my_email}&per-page=1&page=1&select=id&filter={cit}:{sid}')
        response_data = response.json()
        if 'error' in response_data:
            if get_wait_permission(your_title=response_data['error'], your_message="Do you want to wait until your API credits refresh?\n" + \
                                    "Select Yes and keep this process running to resume after midnight UTC.\n" + \
                                    "Select No to end this process and keep any data you've collected so far."):
                # Wait until 1 second after midnight, UTC
                time.sleep(((datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=0, minute=0, second=1, microsecond=0) - datetime.now(timezone.utc)).total_seconds())
            else:
                show_completion_message(your_title="Process Cancelled", your_message=response_data['error'])
                sys.exit(3) # Terminate with code 3, API error
        cit_count = response_data['meta']['count']
        
        # If there are citations
        if cit_count > 0:
            cursor = '*'  # Starts pagination
            ppg = 200  # Results per page
            
            # While there are results remaining
            while not cursor is None:
                time.sleep(0.1)  # Obey public API rate limit of max 10 requests per second
                response = requests.get(f'{oal_domain}works?mailto={my_email}&per-page={ppg}&cursor={cursor}&select={",".join(fields_to_return)}&filter={cit}:{sid}')
                response_data = response.json()
                if 'error' in response_data:
                    if get_wait_permission(your_title=response_data['error'], your_message="Do you want to wait until your API credits refresh?\n" + \
                                            "Select Yes and keep this process running to resume after midnight UTC.\n" + \
                                            "Select No to end this process and keep any data you've collected so far."):
                        # Wait until 1 second after midnight, UTC
                        time.sleep(((datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=0, minute=0, second=1, microsecond=0) - datetime.now(timezone.utc)).total_seconds())
                    else:
                        show_completion_message(your_title="Process Cancelled", your_message=response_data['error'])
                        sys.exit(3) # Terminate with code 3, API error
                cursor = response_data['meta'].get('next_cursor')
                
                # Append latest page of results to the results file
                if 'cited_by' in cit:
                    degct = cited_by_degct
                elif 'cites' in cit:
                    degct = cites_degct
                res_count = len(response_data['results'])
                if res_count > 0:
                    pd.DataFrame(response_data['results']).assign(direction=[cit]*res_count, degrees=[degct]*res_count).to_csv(file_path, mode='a', sep='|', index=False, header=False)
                    next_ids = pd.concat([next_ids, pd.DataFrame({'cit': [cit]*res_count, 'id': [res['id'] for res in response_data['results']]})], ignore_index=True)

# Prepare for next iteration
next_ids['id'] = next_ids['id'].str.replace('https://openalex.org/', '', regex=True)
seed_ids = next_ids

# Clean up temporary objects
del cit, cit_count, cursor, degct, next_ids, res_count, response_data, response, ppg, sid
gc.collect()
