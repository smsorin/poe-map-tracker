from flask import Flask, render_template, request
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
def index():
    user_agent = request.headers.get('User-Agent').lower()
    is_mobile = 'android' in user_agent
    print(user_agent)
    print(is_mobile)
    return render_template('home.html', is_mobile=is_mobile)

@socketio.on('trigger_item_update')
def handle_custom_event():
    sendUpdate()

@app.route("/maps_summary")
def handle_maps_summary():
    return maps_summary.BuildSummary(local_loop.mapsDB)

def sendUpdate():
    if not local_loop.current_item: 
        socketio.emit("item_update", "")    
        socketio.emit("summary_update")
        return
    socketio.emit("item_update", local_loop.current_item.html(local_loop.mapsDB))

if __name__ == '__main__':
    local_loop = local.LocalLoop(socketio)
    local_loop.on_update = sendUpdate
    socketio.run(app, host="0.0.0.0")