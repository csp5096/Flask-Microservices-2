from flask import (
  Flask, 
  render_template, 
  request, flash, 
  redirect, 
  url_for, 
  session, 
  jsonify, 
  session
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_admin import Admin
from admin import AdminView, TopicView
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Polls, Topics, Options, UserPolls

# Blueprints 
from api.api import api

app = Flask(__name__)

app.register_blueprint(api)

# Load config.py from the config file we created earlier
app.config.from_object('config')

# Initialize and create the database
db.init_app(app)
#db.create_all(app=app)
migrate = Migrate(app, db, render_as_batch=True)

# Create the app admin 
admin = Admin(app, 
              name="Dashboard", 
              index_view=TopicView(Topics, 
                                  db.session, 
                                  url='/admin', 
                                  endpoint='admin'
                                )
            )
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Polls, db.session))
admin.add_view(ModelView(Options, db.session))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        # Get the user details from the form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        password = generate_password_hash(password)
        user = Users(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up please login')
        return redirect(url_for('home'))

    # It's a GET request, now render the template
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    # we don't need to check the request type as flask will raise a bad request
    # error if a request aside from POST is made to this url

    username = request.form['username']
    password = request.form['password']

    # Search the database for the User
    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            # The has matches the password in the database log the user in
            session['user'] = username 
            flash('Login was successful')
    else:
        # user wan't found in the database
        flash('Username or password is incorrect please try again', 'error')

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if 'user' is session:
        session.pop('user')

        flash('We hope to see you again')

    return redirect(url_for('home'))

@app.route('/polls', methods=['GET'])
def polls():
    return render_template('polls.html')

@app.route('/polls/<poll_name>')
def poll(poll_name):
    return render_template('index.html')


