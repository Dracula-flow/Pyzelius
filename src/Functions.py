import os
from datetime import datetime as dt


def time_responser(selector):
    """
    A function to return different time components in the form of a formatted string, based on the input parameter.

    Parameters:
        date = returns today's date in European format.
        time = returns current time of the day.
        datetime = returns today's date and time.
    """
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


def format_checker(filename: str, *formats: str) -> bool:
    """
    Checks if the file has one of the specified formats.
    
    Parameters:
        filename (str): The name of the file to check.
        *formats (str): The formats to check for, passed as variable arguments.
        
    Returns:
        bool: True if the filename ends with any of the provided formats, False otherwise.
    """
    return filename.lower().endswith(tuple(formats))

def truncate_path(path: str):
    # Check if the path length exceeds the limit
    if len(path) > 40:
        # Split the path into directory and filename
        dir_path, file_name = os.path.split(path)
        
        # Truncate the file name if needed (preserve extension)
        base_name, ext = os.path.splitext(file_name)
        
        # Calculate the maximum length for the base name
        max_base_name_length = 260 - len(dir_path) - len(ext) - 1  # For the separator
        
        if len(base_name) > max_base_name_length:
            base_name = base_name[:max_base_name_length]  # Truncate the base name
            
        # Reconstruct the full path with the truncated filename
        truncated_path = os.path.join(dir_path, base_name + ext)
        
        return truncated_path
    return path  # Return the original path if no truncation is needed