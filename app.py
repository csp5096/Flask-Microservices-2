from flask import Flask
from models import db

app = Flask(__name__)

# Load config.py from the config file we created earlier
app.config.from_object('config')

# Initialize and create the database
db.init_app(app)
db.create_all(app=app)

@app.route('/')
def home():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()