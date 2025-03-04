from flask import Flask
from flask import request
from flask import jsonify
from utils.scraper import Scraper
from utils.region import Region
from models.db import db
from models.weather import Weather
from models.location import Location
from datetime import timedelta, datetime
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@db:3306/weatherscraper"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start(paused=True)  
  
def start_schedule():
  scheduler.resume()
  
def stop_schedule():
  scheduler.pause()

@app.shell_context_processor
def make_shell_context():
  """ Make necessary methods available in the Flask shell """
  return {
    'app': app, 
    'init_database': init_database, 
    'start_schedule': start_schedule, 
    'stop_schedule': stop_schedule,
  }

@app.route('/weather')
def get_weather():
  """ For a given request to /weather return the weather for the requested day based on the 
      lat, lng and day query parameters

  Returns:
      A JSON object containing the requested weather data
  """
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  day = request.args.get('day')
  
  if day and lat and lng:
    lat = float(lat)
    lng = float(lng)
    
    region = Region()
    name = region.compute_closest((lat, lng))
    location = Location.query.filter_by(name = name["name"], day = day).first()
    updated = location.updated_at
    
    # If the location data is less than we can call it up to date and return it from the database
    if datetime.now() -  updated < timedelta(minutes=1):
      return jsonify({
        "location": location, 
        "weather": location.weathers
      })
    # Else, we want to fetch new data for that location, then return it
    else:
      fetch_single_location_weather(location)
      return jsonify({
        "location": location, 
        "weather": location.weathers
      })

  else:
    output = "Missing request query parameters. "
    output += "" if lat else "Missing \"lat\" parameter. "
    output += "" if lng else "Missing \"lng\" parameter. "
    output += "" if day else "Missing \"day\" parameter. "
    
    return output
    
def fetch_single_location_weather(location):
  scraper = Scraper()
  
  weather = scraper.get_weather(Region.locations[location.name])
  days = [dict(list(weather.items())[i:i + 24]) for i in range(0, len(weather), 24)]
  
  for index, day in enumerate(days):
    location = Location.query.filter_by(name = location.name, day = index).first()
    for id, weather in day.items():
      Weather.query.filter_by(location_id = location.id, time = convert_to_24h(weather["time"])).update({
        'rain': weather["rain"],
        'speed': weather["speed"],
        'direction': weather["direction"] 
      })
    location.updated_at = datetime.now()
      
  db.session.commit()

@scheduler.task('interval', id='do_job_1', seconds=3000, misfire_grace_time=900)
def fetch_all_location_weather():
  with scheduler.app.app_context():
    print("argh me hearty")
    scraper = Scraper()
    
    for name, position in Region.locations.items():
      weather = scraper.get_weather(position)
      days = [dict(list(weather.items())[i:i + 24]) for i in range(0, len(weather), 24)]
      
      for index, day in enumerate(days):
        location = Location.query.filter_by(name = name, day = index).first()
        for id, weather in day.items():
          print(weather)
          Weather.query.filter_by(location_id = location.id, time = convert_to_24h(weather["time"])).update({
            'rain': weather["rain"],
            'speed': weather["speed"],
            'direction': weather["direction"] 
          })    
        Location.query.filter_by(name = name, day = index).update({'updated_at': datetime.now()})
    db.session.commit()
  
def populate_weather():    
  session = db.session
  scraper = Scraper()
  
  for name, position in Region.locations.items():
    weather = scraper.get_weather(position)
    days = [dict(list(weather.items())[i:i + 24]) for i in range(0, len(weather), 24)]
    
    for index, day in enumerate(days):
      location = Location.query.filter_by(name = name, day = index).first()
      for id, weather in day.items():
        record = Weather(location_id = location.id, time = convert_to_24h(weather["time"]), rain = weather["rain"], speed = weather["speed"], direction = weather["direction"])
        session.add(record)
        
  session.commit()
  session.close()

def populate_locations():
  session = db.session
  
  for name, position in Region.locations.items():
    for day in range(0, 3):
      location = Location(name = name, day = day)
      session.add(location)
      
  session.commit()
  session.close()
  
def convert_to_24h(time):
    time_object = datetime.strptime(time, '%I%p')
    time_24h = time_object.strftime('%H')

    return int(time_24h)
  
def init_database():
  db.create_all()
  populate_locations()
  populate_weather()
     
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
