from flask import Flask, render_template
from flask_socketio import SocketIO

import local
import maps_summary

# Pickle imports
from map import Map
from fragment import Fragment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
local_loop = None

@app.route("/")
def hello_world():    
    return render_template('home.html')

@socketio.on('my event')
def handle_custom_event(data):
    print('Custom event')
    print('Data:', data)    

@app.route("/maps_summary")
def handle_maps_summary():
    return maps_summary.BuildSummary(local_loop.mapsDB)

def sendUpdate():
    print('New item to update.')
    socketio.emit("item_update", local_loop.current_item.html(local_loop.mapsDB))

if __name__ == '__main__':
    local_loop = local.LocalLoop()
    local_loop.on_update = sendUpdate
    socketio.run(app)