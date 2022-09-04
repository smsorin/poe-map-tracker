var socket = io();

function remove_map(map_id) {
    socket.emit("remove_map", map_id)
}