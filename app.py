from flask import (
  Flask, render_template, request, flash, redirect, url_for, session, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_admin import Admin
from admin import AdminView, TopicView
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Polls, Topics, Options

app = Flask(__name__)

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

@app.route('/api/poll/<poll_name>')
def api_poll(poll_name):
    poll = Topics.query.filter(Topics.title.like(poll_name)).first()   
    return jsonify({'Polls': [poll.to_json()]}) if poll else jsonify({'Message': 'Poll not found'})

@app.route('/api/polls', methods=['GET', 'POST'])
# retrieves/adds polls from/to the database
def api_polls():
    if request.method == 'POST':
        
        # get the poll and save it in the database
        poll = request.get_json()

        # simple validation to check if all values are properly secret
        for key, value in poll.items():
            if not value:
                return jsonify({'error': 'value for {} is empty'.format(key)})

        title = poll['title']
        options_query = lambda option : Options.query.filter(Options.name.like(option))
        options = [Polls(option=Options(name=option))
                    if options_query(option).count() == 0
                    else Polls(option=options_query(option).first()) for option in poll['options']
                ]
        new_topic = Topics(title=title, options=options)
        db.session.add(new_topic)
        db.session.commit()
        return jsonify({'message': 'Poll was created succesfully'})
    else:
        # it's a GET request, return dict representations of the API
        polls = Topics.query.filter_by(status=1).join(Polls).order_by(Topics.id.desc()).all()
        all_polls = {'Polls':  [poll.to_json() for poll in polls]}
        return jsonify(all_polls)

@app.route('/api/polls/options')
def api_polls_options():
    all_options = [option.to_json() for option in Options.query.all()]
    return jsonify(all_options)

@app.route('/api/poll/vote', methods=['PATCH'])
def api_poll_vote():
    poll = request.get_json()  
    poll_title, option = (poll['poll_title'], poll['option'])
    join_tables = Polls.query.join(Topics).join(Options)

    # Get topic and username from database
    topic = Topics.query.filter_by(title=poll_title).first()
    user = Users.query.filter_by(username=session['user']).first()

    # filter options
    option = join_tables.filter(Topics.title.like(poll_title)).filter(Options.name.like(option)).first()

    # Check if the user has voted on this poll
    poll_count = UserPolls.query.filter_by(topic_id=topic.id).filter_by(user_id=user.id).count()  
    if poll_count > 0:
        return jsonify({'message': 'Sorry: multiple voters are not allowed'})  
    
    # increment vote_cout by 1 if the option was found 
    if option:
        # Record the user and poll
        user_oll = UserPolls(topic_di=topic.id, user_id=user.id)
        db.session.add(user_poll)

        # Increment vote_count by 1 if the option was found
        option.vote_count += 1  
        db.session.commit() 
        return jsonify({'message': 'Thank you for voting!'})

    return jsonify({'message': 'Option or Poll was not found please try again!'})
