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

    params={"latitude": lat, "longitude": lon,  "format": "geojson" , "limit" : 10, "maxradiuskm" : 500}
    
    response_2_from_USGS = requests.get(
        BASE_URL,
        params=params
        
    )
   
    data_2 = response_2_from_USGS.json()

    if not data_2:
        print("Not found please try again")
        return None
   
    return data_2



    


    






        




    







