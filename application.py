import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


from wtform_fields import *
from models import *


#Configure app
app = Flask(__name__)

app.secret_key = 'replace later'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


#Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ywfswkkvelnjjo:c0e02d3ca9a527673dee4e990ec814023ae9b932c0d0b0d65c2277bf7e802a3d@ec2-23-21-248-1.compute-1.amazonaws.com:5432/ddn24ofdllas71'
db = SQLAlchemy(app)

socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Sorry this name already exits, Try another name"
        
        # Add user to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into the Database"

    return render_template("index.html", form=reg_form)



if __name__ == "__main__":
    
    app.run(debug=True)
