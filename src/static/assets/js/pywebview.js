function launch_game() {
    let game_path = document.getElementById("game_path").textContent
    let platform = document.getElementById("platform_slug").textContent
    console.log(game_path)
    console.log(platform)
    pywebview.api.launch_game(platform, game_path)
}

function close_window() {
    pywebview.api.close_window()
}

function toggle_fullscreen() {
    pywebview.api.toggle_fullscreen()
}
