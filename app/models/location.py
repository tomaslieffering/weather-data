from models.db import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Location(db.Model):
	""" A data base model for a location.
			Note each discrete location held in Region has three corresponding location database records
			One for each available day (today, tomorrow and the day after)
	"""
  
	__tablename__ = "locations"
  
	id = db.Column(db.Integer, primary_key=True)
	name:str = db.Column(db.String(50), nullable=False)
	day = db.Column(db.Integer, nullable=False)
	weathers = db.relationship("Weather", backref="location")
	updated_at:str = db.Column(db.DateTime, default=func.now(), nullable=False)