import os

from time import localtime, strftime

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room


from wtform_fields import *
from models import *


#Configure app
app = Flask(__name__)

app.secret_key = 'replace later'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


#Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ywfswkkvelnjjo:c0e02d3ca9a527673dee4e990ec814023ae9b932c0d0b0d65c2277bf7e802a3d@ec2-23-21-248-1.compute-1.amazonaws.com:5432/ddn24ofdllas71'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Initialize Flask-SockIO
socketio = SocketIO(app)
ROOMS = ["longue", "news", "games", "coding"]


# Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))




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

        flash('Registered successfully, Please login.', 'success')

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)



@app.route("/login", methods=["GET", "POST"])
def login():
    
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)

        # el tare2a el 2ola w hnshlha law 3yzen n3ml el tare2a el tanya
        return redirect(url_for('chat'))

        # el tare2a eltanya w Bnst5dm el tare2a de ma3 @login_required ba3d el @app.route("/chat")
        # if current_user.is_authenticated:
        #     return "Logged in with flask-login!"



    
    return render_template("login.html", form=login_form)




@app.route("/chat", methods=["GET", "POST"])
def chat():

    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)



# El tare2a el tanya
# @app.route("/chat", methods=["GET", "POST"])
# @login_required
# def chat():

#     return "Chat with me"




@app.route("/logout", methods=["GET"])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))





@socketio.on("message")
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'timeStamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])

    

@socketio.on("join")
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room"}, room=data['room'])


@socketio.on("leave")
def leave(data):

    leave_room(data["room"])
    send({'msg': data['username'] + " has left the " + data['room'] + " room"}, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)