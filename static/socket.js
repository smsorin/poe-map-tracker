function SetupSocket(socket) {
    socket.on('connect', function() {
        socket.emit('my event', {data: 'Im connected!'});
    });
    socket.on('item_update', (data) => {
        UpdateCurrentMap(data);        
    });
    socket.on('summary_update', () => {
        ajax("/maps_summary", UpdateMapsSummary);
    })
}