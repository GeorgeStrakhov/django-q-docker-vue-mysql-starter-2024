import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class MyHandler(FileSystemEventHandler):
    def __init__(self, qcluster_process):
        super().__init__()
        self.qcluster_process = qcluster_process

    def on_modified(self, event):
        print(f'File {event.src_path} has been modified. Restarting qcluster...')
        self.qcluster_process.terminate()
        self.qcluster_process = subprocess.Popen(['python', 'manage.py', 'qcluster'])

def run_qcluster_with_watchdog():
    qcluster_process = subprocess.Popen(['python', 'manage.py', 'qcluster'])

    event_handler = MyHandler(qcluster_process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        qcluster_process.terminate()

    observer.join()

if __name__ == "__main__":
    run_qcluster_with_watchdog()
