import tkinter as tk
from tkcalendar import DateEntry
import earthquakedata
from tkinter import messagebox
from datetime import datetime, timezone, timedelta
from textblob import TextBlob # Checks spelling of user
import pandas as pd

root = tk.Tk()
root.title("Earthquake lookup")
root.geometry("600x400")

# Function: call backend and API from earthquakedata.py, as that is where the API calling process happens


results_history = pd.DataFrame(columns=["location", "magnitude", "place", "time"])







def call_data_search(): # For the project I chose a single day for the limit of a searching filter, about 1 day

    
    global results_history
    listbox.delete(0, tk.END)

    before_cleaned_out_search = entry_1.get() # Runs a spell check using textblob, and asks user if thats what they meant for the input 

    if before_cleaned_out_search:
        run_spell_check = TextBlob(before_cleaned_out_search)
        corrected = str(run_spell_check.correct())

        if corrected.lower() != before_cleaned_out_search.lower():
            answer = messagebox.askyesno("Spell Check Just in Case", f"Did you mean '{corrected}'") # Pop up to ask
            if answer:
                location_area = corrected
            else:
                location_area = before_cleaned_out_search
        else:
            location_area = before_cleaned_out_search

    if any(character.isdigit() for character in before_cleaned_out_search): # Does the first input have numeric digits? It shouldn't this process stops it
        messagebox.showerror("Invaild Characters here!", f"You can only put characters in this box")
        return


    entry_1.delete(0, tk.END)
    entry_1.insert(0, location_area)

    user_date_earth_chosen = entry_2.get()
    magnitude = entry_3.get()

    
    
    if magnitude and not magnitude.replace(".", "").isdigit():
        messagebox.showerror("Invaild input dude", "You can only put numbers in this section!")
        return


    if not location_area:
        messagebox.showwarning("Missing information", "Please add location for a vaild search") # If even location is missing, will not continue
        return

    coords = earthquakedata.coords_to_location(location_area)
    if coords is None:
        messagebox.showerror("Error", "Could not find location try again with a vaild input ") # Failed to procceed if location is not found
        return
    
    if user_date_earth_chosen:
       date_important = datetime.strptime(user_date_earth_chosen, "%d-%m-%Y").replace(tzinfo=timezone.utc).timestamp() * 1000
       start = datetime.strptime(user_date_earth_chosen, "%d-%m-%Y").strftime("%Y-%m-%d") 
       end = (datetime.strptime(user_date_earth_chosen, "%d-%m-%Y") + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
       date_important = None
       start = None
       end = None

       

    lat, lon = coords 
    result = earthquakedata.real_location(lat, lon, user_date_earth_chosen, magnitude, start, end)


    features = result["features"]
    if not features:
        listbox.insert(tk.END, "No earthquakes found for this search")
        return
    
    for exact in features:
        place =  exact["properties"]["place"]
        mag = exact["properties"]["mag"]
        time = exact["properties"]["time"]
        new_result = pd.DataFrame([{"location": location_area, "magnitude": mag, "place": place, "time": time}])
        if magnitude and float(magnitude) == mag:
            listbox.insert(tk.END, f"M{mag} - {place} (exact match)")
        else:
            listbox.insert(tk.END, f"M{mag} - {place}")
        results_history = pd.concat([results_history, new_result], ignore_index=True)
       
        
    


    results_history.to_csv("results_history.csv", index=False)

# Below are Visual Widgets 
label_0 = tk.Label(root, text="To search earthquakes on this directory, fill out the location, other inputs such as \n the date and magnitude are optional but recommended for more accurate searches. Leave Date with NO characters if unknown", font=("helvetica", 12))
label_0.place(x=600, y=50)

label_1 = tk.Label(root, text="Welcome to the EarthQUAKE Directory", font=("impact", 32))
label_1.place(x=590, y=-10)


label_2 = tk.Label(root, text="Location of the earthquake?:" ,font=("Arial", 14))
label_2.place(x=750, y=90)


 

entry_1 = tk.Entry(root, width=30, bg=("white"))
entry_1.place(x=750, y=120)

button_1 = tk.Button(root, text="Search for this earthquake",  command=call_data_search)
button_1.place(x=750, y=540)

label_2 = tk.Label(root, text="Date of the earthquake." ,font=("Arial", 14))
label_2.place(x=750, y=150)

entry_2 = DateEntry(root, date_pattern='dd-mm-yyyy')
entry_2.place(x=750, y=180)

label_3 = tk.Label(root, text="Magnitude of the earthquake? Up to 1 decimal point.")
label_3.place(x=750, y=220)

entry_3 = tk.Entry(root, width=30, bg=("white"))
entry_3.place(x=750, y=260)

listbox = tk.Listbox(root, width=50,height=10)
listbox.place(x=750, y=340)


root.mainloop()



