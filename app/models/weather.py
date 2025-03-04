from models.db import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from typing import List
from dataclasses import dataclass


@dataclass
class Weather(db.Model):
	""" A data base model for a point of weather data.
			Holds time, rainfall, wind speed and wind direction for a location given by the location_id
  """
 
	__tablename__ = "weathers"
  
	id = db.Column(db.Integer, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
	time:int = db.Column(db.Integer, nullable=False)
	rain:int = db.Column(db.String(10), nullable=False)
	speed:int = db.Column(db.Integer, nullable=False)
	direction:str = db.Column(db.String(10), nullable=False)