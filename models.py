from db_database import db
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

class Img(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    # img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable= True)