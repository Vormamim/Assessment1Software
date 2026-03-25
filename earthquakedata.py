import requests

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query" # URL FOR API


OPEN_MAP = "https://nominatim.openstreetmap.org/search?q={place}&format=json&limit=1"

head = {'User-Agent' : "school"}

closest_info = 0.5

def coords_to_location(place,):

    response = requests.get(
        OPEN_MAP,
        params={"q": place},   
        headers=head
    )
    data = response.json()

    if data == False:
        print("No Location Found")
        return

    
    lat = float(data[0]["lat"]) # Finds Lat and Lon that USGS earthquake can only find via these two terms
    lon = float(data[0]["lon"])  
    return lat, lon



def real_location(lat, lon, date, magnitude, start, end):

    if magnitude == "": # This process Decides if magntiude is filled in by the user, and if it isn't display 10 of the newest earthquakes
       decide = 10
    else:
       decide = 5

    params={"latitude": lat, "longitude": lon,  "format": "geojson" , "limit" : decide, "maxradiuskm" : 500}
    if start:
        params["starttime"] = start
        params["endtime"] = end


    response_2 = requests.get(
        BASE_URL,
        params=params
        
    )
   
    data_2 = response_2.json()

    if not data_2["features_in_data"]: # No results that match user input? Good News this process checks the next closest result
        params.pop("starttime", None)
        params.pop("endtime", None)
        params["limit"] = 10
        params["maxradiuskm"] = 750
        response_2 = requests.get(BASE_URL, params=params)
        data_2 = response_2.json()
        return data_2, True
    




    if not data_2:
        print("Not found")
        return None
   
    return data_2, False




    


    






        




    







