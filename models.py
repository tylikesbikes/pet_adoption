from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, NumberRange

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Main pet model for adoption agency"""

    __tablename__ = 'pets'

    id = db.Column(db.Integer, auto_increment=True, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    species = db.Column(db.Text, nullable = False)
    photo_url = db.Column(db.Text, nullable = True, default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg')
    age = db.Column(db.Integer, nullable= True)
    notes = db.Column(db.Text, nullable = True)
    available = db.Column(db.Boolean, nullable = False, default = True)

class AddPetForm(FlaskForm):
    """Generic form for adding a new pet"""
    name = StringField("Pet's Name", validators=[DataRequired()])
    # species = StringField("Pet Species", validators = [DataRequired(), AnyOf(['cat','dog','porcupine'])])
    species = SelectField("Species", choices = [('cat','Cat'),('dog','Dog'),('porcupine','Porcupine')])
    photo_url = StringField("Pet Photo URL", validators = [URL(), Optional()])
    age = IntegerField("Pet's Age", validators=[NumberRange(0,30,message="Acceptable pets are between 0 and 30 years old")])
    notes = StringField("Notes")
    available = BooleanField("Available?")

class EditPetForm(FlaskForm):
    """Form for editing just a few details about a pet"""

    photo_url = StringField("Pet Photo URL", validators= [Optional(), URL()])
    notes = StringField("Notes about this pet", validators=[Optional()])
    available = BooleanField("Available?", validators=[Optional()])