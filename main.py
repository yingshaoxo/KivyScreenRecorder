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
        #orientation: 'vertical'
        Button: 
            id: my_button
            text: 'Record' 
            on_release: root.record_button() 
            font_size: 46 
        Button: 
            id: pause_or_resume
            text: 'Pause' 
            on_release: root.pause_or_resume_button() 
            font_size: 46 
''')


class OneScreen(Screen):

    def __init__(self, **kwargs):
        self.author = 'yingshaoxo'
        super(OneScreen, self).__init__(**kwargs)

    def record_button(self):
        if self.ids['my_button'].text in "Record":
            self.record()
        elif self.ids['my_button'].text in "Stop":
            self.stop()

    def pause_or_resume_button(self):
        if self.ids['my_button'].text in "Stop":
            if self.ids['pause_or_resume'].text in "Pause":
                self.pause()
            elif self.ids['pause_or_resume'].text in "Resume":
                self.resume()

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
            if self.ids['pause_or_resume'].text in "Resume":
                self.resume()
            t.kill("ffmpeg")
            print("Stoped!")
            self.ids['my_button'].text = "Record"

            """
            while (t.is_running("ffmpeg")):
                time.sleep(1)
            """

    def pause(self):
        if t.is_running("ffmpeg"):
            pids = t._get_pids("ffmpeg")
            [t.run_command(
                "sudo kill -s SIGSTOP {pid}".format(pid=pid)) for pid in pids]
            print("Paused!")
            self.ids['pause_or_resume'].text = "Resume"

    def resume(self):
        if t.is_running("ffmpeg"):
            pids = t._get_pids("ffmpeg")
            [t.run_command(
                "sudo kill -s SIGCONT {pid}".format(pid=pid)) for pid in pids]
            print("resumed!")
            self.ids['pause_or_resume'].text = "Pause"


class ScreenRecorder(App):
    def build(self):
        return OneScreen()

    def on_stop(self):
        from pprint import pprint
        self.get_running_app().root.stop()


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '100')
ScreenRecorder().run()
