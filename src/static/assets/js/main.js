function launch_game() {
    let game_path = document.getElementById("game_path").textContent
    let platform = document.getElementById("platform_slug").textContent
    pywebview.api.launch_game(platform, game_path)
}

function close_window() {
    pywebview.api.close_window()
}

function toggle_fullscreen() {
    pywebview.api.toggle_fullscreen()
}

function search_query() {
    let query = document.getElementById("query").value.valueOf();
    url_base = "/library/search?query="
    window.location.href = url_base+query;
}