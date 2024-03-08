// LIBRARY FUNCTIONS

function launch_game(platform_slug, filename) {
    fetch(`/launch/game/${platform_slug}/${filename}`)
}

function search_query() {
    let query = document.getElementById("query").value.valueOf();
    url_base = "/library/search?query="
    window.location.href = url_base+query;
}


// WINDOW FUNCTIONS

function close_window() {
    pywebview.api.close_window()
}

function toggle_fullscreen() {
    pywebview.api.toggle_fullscreen()
}