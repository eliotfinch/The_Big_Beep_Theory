import datetime

# The date of the first beep entry
ref_date = datetime.datetime(2022, 5, 9)

def read_data(data_path, absolute_dates=False, absolute_times=False):    
    """
    Read the CSV beep data into a dictionary. Keys are the dates. Entries are
    a list of (time, observer) tuples. Notes are currently ignored.

    Parameters
    ----------
    data_path : path-like object
        The path to the data .csv.
    absolute_dates : bool, optional
        If True, dates are expressed as a number of days since the first entry. 
        The default is False.
    absolute_times : bool, optional
        If True, times are expressed as a number of seconds past midnight. The 
        default is False.

    Returns
    -------
    data : dict
        The beep data, with date, time and observer information.
    """
    data = {}
    with open(data_path, 'r') as f:
        for i, line in enumerate(f):
            
            # Ignore the first two lines
            if i in [0, 1]:
                pass
            
            else:
                entry = [item for item in line.strip().split(',')]
                
                # Ignore lines with no entry
                date = entry[0]
                if len(date) == 0:
                    continue
                
                time = entry[1]
                
                # Parse the observer information if available. We have to deal
                # with the special cases.
                if len(entry[2]) == 2:
                    observer = entry[2].upper()
                elif entry[2] == 'DR**2':
                    observer = 'DR'
                elif entry[2] == 'CC and DR :) (30-70 split)':
                    observer = 'DR'
                elif entry[2] == 'LT hello':
                    observer = 'LT'
                elif entry[2] == 'DG/(LT maybe)':
                    observer = 'DG'
                else:
                    observer = 'unknown'
                
                # Some dates have different formatting
                if 'May' in date:
                    if 'th' in date:
                        day = date[:date.index('th')]
                    elif 'st' in date:
                        day = date[:date.index('st')]
                    elif 'rd' in date:
                        day = date[:date.index('rd')]
                    date = f'{day}/5/22'
                
                # Add to the dictionary
                if date in data.keys():
                    data[date].append((time, observer))
                else:
                    data[date] = [(time, observer)]
                    
    if absolute_dates:
        
        # Convert all dates to a number of days from the first date
        data_abs_date = {}
        
        for date, entry in data.items():
            
            # Format date information
            day, month, year = date.split('/')
            year = int(year) + 2000
            month = int(month)
            day = int(day)
                
            # Find the number of days between the current date and the 
            # reference date
            abs_date = (datetime.datetime(year, month, day) - ref_date).days
                
            # Store to dictionary
            data_abs_date[abs_date] = entry
            
        data = data_abs_date
        
    if absolute_times:
        
        # Convert all times to a number of seconds past midnight
        data_abs_times = {}
        
        for date, entry in data.items():
            
            # Initialize entry
            data_abs_times[date] = []
            
            for time, observer in entry:
                
                # Split the time into hours and minutes
                hour, minute = time.split(':')
                
                # Convert the time to a Python datetime object
                t = datetime.time(hour=int(hour), minute=int(minute))
                
                # We can then convert the time to a number of seconds past 
                # midnight
                dt = datetime.timedelta(hours=t.hour, minutes=t.minute).total_seconds()
                
                # Store to dictionary
                data_abs_times[date].append((dt, observer))
                
        data = data_abs_times
                        
    return data
     