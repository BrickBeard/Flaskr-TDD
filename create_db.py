from app import db
from models import Flaskr


# Create the database and the db table
db.create_all()

# Commit the changes
db.session.commit()
