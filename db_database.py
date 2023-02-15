from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# function that initialises the db creates the tables 
def db_init(app):
    db.init_app(app)

    # creates the tables if the db doesnt already exist
    with app.app_context():
        db.create_all()
