from datetime import datetime as dt


def time_responser(selector):
    """
    A function to return different time components in the form of a formatted string, based on the input parameter
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


def is_test(filename):
    """
    Checks for video file format
    """
    return filename.lower().endswith(('.mp4','.mov')) 

def is_screenshot(filename):
    """
    Checks for image file format
    """
    return filename.lower().endswith(('.jpg','.png'))
