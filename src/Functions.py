from datetime import datetime as dt

# A function to return different time components in the form of a formatted string, based on the input parameter
def time_responser(selector):
    date = dt.now().strftime('%d-%m-%Y')
    time = dt.now().strftime('%H:%M')

    output={
        'date' : date,
        'time' : time,
        'datetime' : f"{date} {time}"
    }

    try:
        return output.get(selector)
    except: 
        if selector not in output:
            raise ValueError(f"Error: {selector} is NOT a valid parameter. Time_responser only takes 'date', 'time' and 'datetime' as parameters")

# A function to check for file format
def is_test(filename):
    return filename.lower().endswith(('.mp4','.mov')) 
