function SetupSocket(socket) {
    socket.on('connect', function() {
        socket.emit('my event', {data: 'Im connected!'});
    });
    socket.on('item_update', (data) => {
        UpdateCurrentMap(data);        
    });
}