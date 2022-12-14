from flask import Flask, render_template, request
from flask_socketio import SocketIO

import local
import maps_summary

# Pickle imports
from map import Map
from fragment import Fragment
from contract import Contract


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
local_loop = None


@app.route("/")
def index():
    user_agent = request.headers.get('User-Agent').lower()
    is_mobile = 'android' in user_agent
    return render_template('home.html', is_mobile=is_mobile)


@socketio.on('trigger_item_update')
def handle_custom_event():
    sendUpdate()


@app.route("/maps_summary")
def handle_maps_summary():
    return maps_summary.BuildSummary(local_loop.mapsDB)


@app.route("/edit_maps")
def handle_edit_maps():
    maps = local_loop.mapsDB.GetMapsContext()    
    return render_template('edit_maps.html', maps=maps)


@socketio.on_error_default
def default_socket_error(e):
    print('Socket IO Error:', e)


def sendUpdate():
    if not local_loop.current_item: 
        socketio.emit("item_update", "", namespace='/')    
        socketio.emit("summary_update", namespace='/')
        return
    print('Writing to sockeio.')
    socketio.emit("item_update", local_loop.current_item.html(local_loop.mapsDB), namespace='/')


if __name__ == '__main__':
    local_loop = local.LocalLoop(socketio)
    local_loop.on_update = sendUpdate
    socketio.run(app, host="0.0.0.0")