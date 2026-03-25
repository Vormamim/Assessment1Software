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

closest_result = 0.3

# Function: call backend and API from earthquakedata.py

search_history = pd.DataFrame(columns=["location", "date", "magnitude"])
results_history = pd.DataFrame(columns=["location", "magnitude", "place", "time"])







def call_data_search(closest_result = 0.3, time_closest = 86400000): # For the project I chose a single day for the limit of a searching filter, about 1 day

    global search_history
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
        messagebox.showerror("Invaild Characters here!", f"You can only put characters in this box!")
        return


    entry_1.delete(0, tk.END)
    entry_1.insert(0, location_area)

    user_date_earth_chosen = entry_2.get()
    magnitude = entry_3.get()

    
    
    if magnitude and not magnitude.replace(".", "", 1).isdigit():
        messagebox.showerror("Invaild input dude", "You can only put numbers in this section!")
        return

   
    new_row = pd.DataFrame([{"location": location_area, "date": user_date_earth_chosen, "magnitude": magnitude}]) # Panda main frame    
    search_history = pd.concat([search_history, new_row], ignore_index=True)
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
    result, fallback = earthquakedata.real_location(lat, lon, user_date_earth_chosen, magnitude, start, end)

    
    


    

    
    
    

    features_in_data = result["features_in_data"]
    if not features_in_data:
        listbox.insert(tk.END, "No earthquakes found for this search")
        return
    exact_area = any(location_area.lower() in ed ["properties"]["place"].lower() for ed in features_in_data)
    found_match = False
    for exact in features_in_data:
        place =  exact["properties"]["place"]
        mag = exact["properties"]["mag"]
        time = exact["properties"]["time"]
        new_result = pd.DataFrame([{"location": location_area, "magnitude": mag, "place": place, "time": time}])
        results_history = pd.concat([results_history, new_result], ignore_index=True)
        if date_important and abs(time - date_important) < time_closest:
           found_match = True
           listbox.insert(tk.END, f"M{mag} - {place} (closest result)") # It found an exact location
        elif magnitude and abs(float(magnitude) - float(mag)) < closest_result:
             found_match = True
             listbox.insert(tk.END, f"M{mag} - {place} (magnitude match)")
        else:
            listbox.insert(tk.END, f"M{mag} - {place}")
        
    

    if fallback: # API Retry Call with the case of User not filling out "Date of Earthquake"
        listbox.insert(0, "Could not find earthquake in exact location ")
        listbox.insert(1, "here are the closest ones")


    

    search_history.to_csv("search_history.csv", index=False)
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

label_2 = tk.Label(root, text="Date of the earthquake. DELETE all numbers if unknown" ,font=("Arial", 14))
label_2.place(x=750, y=150)

entry_2 = DateEntry(root, date_pattern='dd-mm-yyyy')
entry_2.place(x=750, y=180)

label_3 = tk.Label(root, text="Magnitude of the earthquake? Up to 1 decimal point. The process will call any earthquake result within 0.3 of a magnitude")
label_3.place(x=750, y=220)

entry_3 = tk.Entry(root, width=30, bg=("white"))
entry_3.place(x=750, y=260)

listbox = tk.Listbox(root, width=50,height=10)
listbox.place(x=750, y=340)


root.mainloop()



