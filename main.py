from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import Config

from auto_everything.base import Terminal
t = Terminal()

import os
import time


Builder.load_string('''
<OneScreen> 
    BoxLayout: 
        Button: 
            id: my_button
            text: 'Record' 
            on_release: root.record_button() 
            font_size: 46 
''')


class OneScreen(Screen):

    def __init__(self, **kwargs):
        self.author = 'yingshaoxo'
        super(OneScreen, self).__init__(**kwargs)

    def record_button(self):
        if not t.is_running("ffmpeg"):
            self.record()
        else:
            self.stop()

    def record(self):
        if t.system_type == "linux":
            if "not found" in t.run_command("ffmpeg"):
                t.run("sudo apt install ffmpeg -y")

            path = t.fix_path("~/Videos")
            if not t.exists(path):
                os.mkdir(path)
            path = os.path.join(path, 'doing')
            if not t.exists(path):
                os.mkdir(path)

            index = str(len(os.listdir(path)) + 1)

            if not t.is_running("ffmpeg"):
                t.run("ffmpeg -y -f alsa -i hw:0 -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0+0,0 -c:v libx264 -pix_fmt yuv420p -qp 0 -preset ultrafast {path}/{index}.mp4".format(
                    path=path, index=index), wait=False)
                self.get_root_window().minimize()
                print("Recording...")
                self.ids['my_button'].text = "Stop"

    def stop(self):
        if t.is_running("ffmpeg"):
            t.kill("ffmpeg", force=False, wait=True)
            print("Stoped!")
            self.ids['my_button'].text = "Record"


class ScreenRecorder(App):
    def build(self):
        return OneScreen()

    def on_stop(self):
        from pprint import pprint
        self.get_running_app().root.stop()


Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '100')
ScreenRecorder().run()
