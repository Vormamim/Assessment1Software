try:
    import truststore
except ImportError:
    truststore = None
else:
    truststore.inject_into_ssl()

import requests

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query" # URL FOR API


OPEN_MAP = "https://nominatim.openstreetmap.org/search"

head = {'User-Agent' : "school"}

closest_info = 0.5

def coords_to_location(place,):

    try:
        response = requests.get(
            OPEN_MAP,
            params={"q": place, "format": "json", "limit": 1},
            headers=head,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    if not data:
        return None

    
    lat = float(data[0]["lat"]) # Finds Lat and Lon that USGS earthquake can only find via these two terms
    lon = float(data[0]["lon"])  
    return lat, lon



def real_location(lat, lon, date, magnitude, start, end):

    params={"latitude": lat, "longitude": lon,  "format": "geojson" , "limit" : 10, "maxradiuskm" : 500}
    if start:
        params["starttime"] = start
    if end:
        params["endtime"] = end
    if magnitude:
        params["minmagnitude"] = magnitude
    
    try:
        response_2_from_USGS = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )
        response_2_from_USGS.raise_for_status()
        data_2 = response_2_from_USGS.json()
    except requests.RequestException:
        return None

    if not data_2:
        return None
   
    return data_2



    


    






        




    







