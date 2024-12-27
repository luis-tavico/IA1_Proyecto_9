import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class MyHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
        print(f"Reiniciando: {self.script}")
        self.process = subprocess.Popen(["python3.8", self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            self.restart_script()

if __name__ == "__main__":
    script_to_watch = "../app/app.py"  # Cambia esto por tu archivo tkinter
    event_handler = MyHandler(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()