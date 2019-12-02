import os

from flask import Flask, render_template, redirect, url_for
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

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data


        # Hash the password
        hashed_pswd = pbkdf2_sha256.hash(password)
                    # pbkdf2_sha256.using(rounds=29000, salt_size=16).hash(password)        de el default values  w bnst5dm eltare2a de 3shan law 3ayzen n3`yar el number bta3 el iteration and size


        
        # Add user to the database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)



@app.route("/login", methods=["GET", "POST"])
def login():
    
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        return "Logged in, finally!"
    
    return render_template("login.html", form=login_form)




if __name__ == "__main__":
    
    app.run(debug=True)
