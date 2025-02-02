from datetime import datetime as dt
import pyperclip

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

# Funzione per copiare le stringhe sulla clipboard
def copia_su_clipboard(entry_vars,input_fields):

    combine=[]
    
    for entry,key in zip(entry_vars,input_fields):
        try:
            input_value= entry.get()
            combine.append(f"{key} {input_value}")
        except TypeError:
            print (f"Errore: {key}")

    combine.append(f"{'DATA E ORA'} {time_responser('datetime')}")

    # Uniamo le stringhe con un salto di linea
    testo_da_copiare = "\n".join(combine)

    # Copiamo sulla clipboard
    pyperclip.copy(testo_da_copiare)

    # Mostriamo un messaggio di conferma
    
