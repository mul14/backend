import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Beacon(db.Model, BaseModel):
	# table name
	__tablename__ = 'beacons'
	# displayed fields
	visible = ['id', 'code', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
