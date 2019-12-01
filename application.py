import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'replace later'
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    
    app.run(debug=True)
