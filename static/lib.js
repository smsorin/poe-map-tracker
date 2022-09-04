function ajax(url, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onload = (e) => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(xhr.responseText);
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.onerror = (e) => {
        console.error(xhr.statusText);
    }
    xhr.send(null);
}

function UpdateMapsSummary(summary) {
    div = document.getElementById("maps_summary");
    if (div === null) {
        console.error("Can't find map_summary on the page.");
        return;
    }
    div.innerHTML = summary;
}

function UpdateCurrentMap(data) {
    div = document.getElementById("current_map");
    if (div === null) {
        console.error("Can't find the current_map on the page.");
    }
    div.innerHTML = data
}