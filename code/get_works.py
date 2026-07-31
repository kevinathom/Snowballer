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

def show_countdown_timer(your_title="Countdown Timer", your_message="Resuming in:", hours=0, minutes=0, seconds=0):
    """
    Open a dialog window displaying a countdown timer in hours, minutes, and seconds.
    Closes automatically when the countdown reaches zero.

    Args:
        your_title (str): The title of the dialog box
        your_message (str): The message displayed above the countdown
        hours (int): Hours to count down from
        minutes (int): Minutes to count down from
        seconds (int): Seconds to count down from

    Returns:
        bool: True if the timer completed naturally, False if the user cancelled
    """
    # Initialize then hide tkinter root
    root = tk.Tk()
    root.withdraw()

    # Convert input to total seconds
    total = int(hours * 3600 + minutes * 60 + seconds)

    # Use mutable containers to track state across inner functions
    remaining = [total]
    result = [True]  # True = completed naturally, False = cancelled

    # Create the dialog window
    dialog = tk.Toplevel(root)
    dialog.title(your_title)
    dialog.resizable(False, False)
    dialog.wait_visibility()
    dialog.grab_set()  # Make modal

    # Add the prompt message
    tk.Label(
        dialog,
        text=your_message,
        wraplength=320,
        justify="center"
    ).pack(padx=20, pady=(20, 5))

    # Add the countdown display label
    time_label = tk.Label(
        dialog,
        text="",
        font=("Courier", 36, "bold")  # Monospaced so digits don't shift as they change
    )
    time_label.pack(padx=20, pady=(5, 20))

    # Add a Cancel button
    button_frame = tk.Frame(dialog, pady=10)
    button_frame.pack()

    def on_cancel():
        result[0] = False
        dialog.destroy()

    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).pack()

    # Handle the X button — treated as cancel
    dialog.protocol("WM_DELETE_WINDOW", on_cancel)

    # Format seconds into HH:MM:SS
    def format_time(secs):
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # Tick function — updates the label and reschedules itself every 1 second
    def tick():
        time_label.config(text=format_time(remaining[0]))
        if remaining[0] > 0:
            remaining[0] -= 1
            dialog.after(1000, tick)
        else:
            # Briefly show 00:00:00 before closing so it doesn't feel abrupt
            dialog.after(500, dialog.destroy)

    # Center the dialog on the screen
    dialog.update_idletasks()
    win_width  = dialog.winfo_width()
    win_height = dialog.winfo_height()
    scr_x = (dialog.winfo_screenwidth()  // 2) - (win_width  // 2)
    scr_y = (dialog.winfo_screenheight() // 2) - (win_height // 2)
    dialog.geometry(f"+{scr_x}+{scr_y}")

    # Start the countdown
    tick()

    # Block here until the dialog closes
    root.wait_window(dialog)

    # Clean up the tkinter instance
    root.destroy()
    return result[0]

def call_api(request_string):
  """
  Call the OpenAlex API and return the response in JSON format.
  Handle any error response.
  
  Args:
    request_string (str): OpenAlex web address with API call parameters
  
  Returns:
    json: OpenAlex API response, converted to JSON
  """
  response_data = requests.get(request_string).json()
  if 'error' in response_data:
    logger.error(f"API error | sid={sid} | page={page_num} | error={response_data['error']}")
    wait_permission = get_wait_permission(your_title=response_data['error'], your_message="Do you want to wait until your API credits refresh?\n" + \
                                                  "Select Yes and keep this process running to resume after midnight UTC.\n" + \
                                                  "Select No to end this process and collect any data you've extracted so far.")
    if wait_permission:
      # Wait until 1 minute after midnight, UTC
      time_now = datetime.now(timezone.utc)
      time_until_reset = ((time_now + timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0) - time_now).total_seconds()
      logger.info(f"Waiting for reset | seconds={time_until_reset:.0f}")
      show_countdown_timer(your_title="Waiting", seconds=time_until_reset)
      response_data = call_api(request_string)
    else:
      # Cancel the process
      logger.warning("User cancelled process during API error wait.")
      show_completion_message(your_title="Process Cancelled", your_message=response_data['error'])
      sys.exit(3) # Terminate with code 3, API error
  return response_data

"""
Temporary: Logger for troubleshooting
"""
import logging
import os

# Only configure the logger once (since get_works.py is exec()'d in a loop)
if not logging.getLogger('snowballer').handlers:
    log_path = os.path.join(data_dir, 'snowballer_debug.log')
    handler = logging.FileHandler(log_path, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger = logging.getLogger('snowballer')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
else:
    logger = logging.getLogger('snowballer')

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
    
    # Clean and count cit value
    if not isinstance(cit, str):
        cit = cit[0]
    if 'cited_by' in cit:
        degct = cited_by_degct
    elif 'cites' in cit:
        degct = cites_degct
    
    # For each work entity ID
    for sid in seed_ids.loc[(seed_ids['cit'] == 'seed') | (seed_ids['cit'] == cit), 'id']:
        
        # Temporary: for logger
        logger.info(f"Processing | direction={cit} | degree={deg} | seed_id={sid}")
        
        # Skip if file exists
        file_path = os.path.normpath(os.path.join(data_dir, 'working', f'{sid}_{cit}_{degct}.txt'))
        if os.path.exists(file_path):
            logger.warning(f"SKIPPED (file exists) | sid={sid} | path={file_path}")
            continue
        
        # Initialize results storage (to file)
        pd.DataFrame(columns=fields_to_return+['direction','degrees']).to_csv(file_path, sep='|', index=False)
        
        # Get result count
        response_data = call_api(request_string=f'{oal_domain}works?mailto={my_email}&per-page=1&page=1&select=id&filter={cit}:{sid}')
        cit_count = response_data['meta']['count']
        logger.info(f"Result count | sid={sid} | direction={cit} | count={cit_count}")
        
        # If there are citations
        if cit_count > 0:
            cursor = '*'  # Starts pagination
            ppg = 200  # Results per page
            # For logger
            page_num = 0
            total_fetched = 0
            
            # While there are results remaining
            while cursor is not None:
                time.sleep(0.1)  # Obey public API rate limit of max 10 requests per second
                page_num += 1 # For logger
                logger.debug(f"Fetching page | sid={sid} | direction={cit} | page={page_num} | cursor={cursor}")
                
                response_data = call_api(request_string=f'{oal_domain}works?mailto={my_email}&per-page={ppg}&cursor={cursor}&select={",".join(fields_to_return)}&filter={cit}:{sid}')
                cursor = response_data['meta'].get('next_cursor')
                
                # Append latest page of results to the results file
                res_count = len(response_data['results'])
                
                # For logger
                total_fetched += res_count
                logger.debug(
                    f"Page result | sid={sid} | direction={cit} | page={page_num} "
                    f"| results_this_page={res_count} | total_so_far={total_fetched} "
                    f"| next_cursor={'None' if cursor is None else 'present'}"
                )
                
                if res_count > 0:
                    pd.DataFrame(response_data['results']).assign(direction=[cit]*res_count, degrees=[degct]*res_count).to_csv(file_path, mode='a', sep='|', index=False, header=False)
                    next_ids = pd.concat([next_ids, pd.DataFrame({'cit': [cit]*res_count, 'id': [res['id'] for res in response_data['results']]})], ignore_index=True)

            logger.info(
              f"Completed | sid={sid} | direction={cit} | pages={page_num} "
              f"| total_fetched={total_fetched} | expected={cit_count}"
            )
            if total_fetched != cit_count:
                logger.warning(
                    f"COUNT MISMATCH | sid={sid} | direction={cit} "
                    f"| expected={cit_count} | actual={total_fetched}"
                )
            else:
                logger.info(f"No results | sid={sid} | direction={cit}")

# Prepare for next iteration
next_ids['id'] = next_ids['id'].str.replace('https://openalex.org/', '', regex=True)
seed_ids = next_ids

# Clean up temporary objects
#for var in [cit, cit_count, cursor, degct, next_ids, res_count, response_data, ppg, sid, time_until_reset, wait_permission]:
#  if var in dir():
#    del var
gc.collect()
