import os
import webview

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def launch_game(self, platform, slug):
        print("HI!")
        ic(platform)
        ic(slug)
        subprocess.run(["game-launcher", platform, slug])


    def close_window(self):
        app_window.destroy()

    def toggle_fullscreen(self):
        app_window.toggle_fullscreen()
        

# api = Api()
# app_window = webview.create_window(os.getenv('APP_TITLE'), app, draggable=True, min_size=(1280,720), text_select=True, js_api=api) 