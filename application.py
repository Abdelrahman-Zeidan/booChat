import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


from wtform_fields import *


#Configure app
app = Flask(__name__)

app.secret_key = 'replace later'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Greate success!"

    return render_template("index.html", form=reg_form)



if __name__ == "__main__":
    
    app.run(debug=True)
