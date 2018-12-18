###############################
####### SETUP (OVERALL) #######
###############################

import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, PasswordField, DateField, IntegerField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, InputRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import requests
import simplejson as json

#login
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'yikes'
## Statements for db setup (and manager setup if using Manager)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/final364"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#app setup
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#login configurations
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

########################
### Helper functions ###
########################
def get_brewery_by_id(id):
    g = Brewery.query.filter_by(user_id=id).first()
    return g

def get_or_create_brewery(db_session, brew_name, current_user):
    brew = db_session.query(Brewery).filter_by(brewery = brew_name, user_id = current_user.id).first()
    if brew:
        return brew
    else:
        brew = Brewery(brewery = brew_name, user_id = current_user.id)
        db_session.add(brew)
        db_session.commit()
        return brew

def get_or_create_collection(db_session, user_name, current_user, brewery_list = []):
    collection = db_session.query(BrewCollection).filter_by(name = user_name, user_id = current_user.id).first()
    if collection:
        return collection
    else:
        collection = BrewCollection(name= user_name, user_id = current_user.id, brew = [])

        for x in brewery_list:
            collection.brew.append(x)
        db_session.add(collection)
        db_session.commit()
        return collection

def get_or_create_advice(db_session, new_brew, new_type, new_loc):
    g = db_session.query.filter_by(newbrew = new_brew).first()
    if g:
        return g
    else:
        g = Advice(newbrew= new_brew, newbrewtype = new_type, newbrewloc= new_loc)
        db_session.add(g)
        db_session.commit()
        return g

##################
##### MODELS #####
##################
#association tables
brew_group = db.Table('brew_group',db.Column('brewery_id', db.Integer, db.ForeignKey('brewery.id')),db.Column('collection_id',db.Integer, db.ForeignKey('collection.id')))

# Special model for users to log in
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    collection = db.relationship('BrewCollection', backref = "User")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#DB load function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Brewery(db.Model):
    __tablename__ = "brewery"
    id = db.Column(db.Integer,primary_key=True)
    brewery = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class BrewCollection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(964))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    brew = db.relationship("Brewery", secondary="brew_group", backref=db.backref("collection", lazy="dynamic"), lazy="dynamic")

class Advice(db.Model):
    __tablename__ = "advice"
    id = db.Column(db.Integer,primary_key=True)
    newbrew = db.Column(db.String(64))
    newbrewtype = db.Column(db.String(64))
    newbrewloc = db.Column(db.String(65))
    newreason = db.Column(db.String(1000))

###################
###### FORMS ######
###################

class BrewForm(FlaskForm):
    #name = StringField("Please enter your name")
    brewery = StringField('Please enter a brewery', validators = [InputRequired()])
    def validate_brewery(self, field):
        if field.data[0].islower():
            raise ValidationError('First letter cannot be lowercase')
        if field.data[0] == " ":
            raise ValidationError('Cannot start with space')
    submit = SubmitField("Submit")

class NameForm(FlaskForm):
    brew = StringField("Please suggest a brewery",validators=[InputRequired()])
    submit = SubmitField("Submit")

class TypeForm(FlaskForm):
    type = StringField("Please input brewery type",validators=[InputRequired()])
    state = StringField("Please input the State the brewery is in",validators=[InputRequired()])
    def validate_state(self, field):
        if field.data[0].islower():
            raise ValidationError('First letter cannot be lowercase')
    submit = SubmitField("Submit")

class CollectionForm(FlaskForm):
    user_name = StringField("Enter name of user and make sure it is the same as the login username: ", validators = [InputRequired()])
    submit = SubmitField("Submit")

class AdviceForm(FlaskForm):
    brew = StringField("Please suggest a brewery",validators=[InputRequired()])
    type = StringField("Please input brewery type",validators=[InputRequired()])
    state = StringField("Please input the State the brewery is in",validators=[InputRequired()])
    def validate_state(self, field):
        if len(field.data) == 2:
            raise ValidationError('Cannot use state abbreviation')
    reason = StringField("Please input why you want to add this brewery", validators=[InputRequired()])
    submit = SubmitField("Submit")

#Registration
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class UpdateButtonForm(FlaskForm):
    submit = SubmitField("Update and spice up all collection names")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class DeleteButtonForm(FlaskForm):
    submit = SubmitField("Delete All Tips")

#######################
###### VIEW FXNS ######
#######################

#login related
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('add'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."

#other
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/addNew', methods = ['GET','POST'])
@login_required
def add():
    form = BrewForm()
    brew = form.brewery.data
    return render_template('addNew.html',form=form)

@app.route('/getBrew', methods = ['GET','POST'])
@login_required
def brew():
    form = BrewForm(request.form)
    if form.validate_on_submit():
        brewery_name = form.brewery.data
        res = requests.get('https://api.openbrewerydb.org/breweries?by_name={}'.format(brewery_name))
        dic = json.loads(res.text)
        if len(dic) == 0:
            return redirect(url_for('nonexist'))
        get_or_create_brewery(db.session, brewery_name, current_user)
        return render_template('brew.html', brewname = brewery_name, state = dic[0]['state'], type = dic[0]['brewery_type'], phone = dic[0]['phone'])

    flash(form.errors)
    return redirect(url_for('add'))

@app.route('/nonExist')
def nonexist():
    return render_template('nonexist.html')

@app.route('/showAll')
def showAll():
    form = DeleteButtonForm()
    breweries = Brewery.query.all()
    final = []
    for x in breweries:
        if x.brewery not in final:
            final.append(x.brewery)
    suggest = Advice.query.all()
    sug = []
    for x in suggest:
        tup = (x.newbrew, x.newbrewtype, x.newbrewloc, x.newreason)
        sug.append(tup)
    return render_template('name.html',full_list = final, suggest_list = sug, form = form)

@app.route('/giveAdvice')
def advice():
    form = AdviceForm()
    brew = form.brew.data
    type = form.type.data
    state = form.state.data
    reason = form.reason.data
    return render_template('advice.html',form=form)

@app.route('/delete',methods=["GET","POST"])
def delete():
    form = DeleteButtonForm()
    if request.method == "POST":
        temp = Advice.query.all()
        for x in temp:
            print(x)
            db.session.delete(x)
            db.session.commit()
        return redirect(url_for("showAll"))

@app.route('/adviceDB', methods = ['GET','POST'])
def advicedb():
    form = AdviceForm(request.form)
    if form.validate_on_submit():
        brew = form.brew.data
        type = form.type.data
        state = form.state.data
        reason = form.reason.data
        advice = Advice(newbrew = brew, newbrewtype = type, newbrewloc = state, newreason = reason)
        db.session.add(advice)
        db.session.commit()
    return redirect(url_for('advice'))

@app.route('/create_c', methods = ['GET', 'POST'])
@login_required
def create_c():
    form=CollectionForm()
    return render_template('create_c.html', form = form)

@app.route('/collections',methods=["GET","POST"])
@login_required
def collections():
    final =[]
    form = CollectionForm()
    brew = Brewery.query.all()
    items = [(x.user_id, x.brewery) for x in brew]
    if form.validate_on_submit:
        for x in items:
            final.append(get_brewery_by_id(x[0]))
        get_or_create_collection(db.session, form.user_name.data, current_user, final)
    collections = User.query.all()
    form = UpdateButtonForm()
    return render_template('ind_collection.html', collections = collections, form = form)

@app.route('/collection/<id_num>')
def one(id_num):
    id = int(id_num)
    collect = BrewCollection.query.filter_by(id=id).first()
    temp = Brewery.query.filter_by(user_id = id).all()
    return render_template('single.html', collect = collect, brew = temp)

@app.route('/update',methods=["GET","POST"])
def update():
    form = UpdateButtonForm()
    if request.method == "POST":
        temp = BrewCollection.query.all()
        print(temp)
        for x in temp:
            if type(x.name) is str:
                x.name = x.name + "(That's you)"
                db.session.commit()
        return redirect(url_for("collections"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
