from flask import Flask, render_template, redirect, flash
from models import db, connect_db, Pet, AddPetForm, EditPetForm
from flask_debugtoolbar import DebugToolbarExtension
from wtforms import StringField, IntegerField

debug = DebugToolbarExtension()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'keeta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.app_context().push()

@app.route('/')
def home_page():
    """Display all pets in db"""
    pets = Pet.query.all()

    return render_template('home.html', pets = pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Show form to add a new pet, handle adding to db"""

    form = AddPetForm()
    
    if form.validate_on_submit():
        new_pet = Pet(name = form.name.data,
                      species = form.species.data,
                      photo_url =  None if form.photo_url.data == '' else form.photo_url.data,
                      age = form.age.data,
                      notes = form.age.data,
                      available = form.available.data
        )
        

        
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
        
    else:
        return render_template('add_pet_form.html', form=form)
    
@app.route('/<int:pet_id>',methods=['GET','POST'])
def view_pet(pet_id):
    """View basic pet info and include a form for editing URL, notes, and available status"""

    this_pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=this_pet)

    if form.validate_on_submit():
        updated = False
        if (this_pet.photo_url != form.photo_url.data) or (this_pet.notes != form.notes.data) or (this_pet.available != form.available.data):
            updated = True

        this_pet.photo_url = form.photo_url.data
        this_pet.notes = form.notes.data
        this_pet.available = form.available.data

        db.session.add(this_pet)
        db.session.commit()
        
        if updated:
            flash(f'{this_pet.name} was updated!')
        return redirect(f'/{pet_id}')

    else:
        return render_template('pet_detail.html', pet = this_pet, form = form)