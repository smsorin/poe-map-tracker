from flask import Flask
from flask_socketio import SocketIO

from map import Map
import local

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
local_loop = None

@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"

if __name__ == '__main__':
    local_loop = local.LocalLoop()
    socketio.run(app)