from flask import Flask, request, jsonify
import requests
import pandas
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="MyApp")
app = Flask(__name__)
df=pandas.read_csv('./Outfits.csv').values
temp=[]
outfits=[]
for i in range(len(df)):
    temp.append([int(t) for t in df[i][0].split(' ')])
    outfits.append(df[i][1])

@app.route('/')
def get_outfits():
   city=request.args.get("city")
   location = geolocator.geocode(city)
   weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m').json()
   temperature=weather['current_weather']['temperature']
   clothes=""
   for i in range(len(temp)):
      if(temperature>=temp[i][0] and temperature<temp[i][1]):
         clothes=outfits[i]
         break
   #return {'outfit':clothes, 'temperature':temperature, 'city':city}
   
   response = jsonify({'outfit':clothes, 'temperature':temperature})
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response
   
if __name__ == '__main__':
   app.run()