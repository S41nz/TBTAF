import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DevHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return
        print(f"Changes detected in {event.src_path}. Reloading...")
        subprocess.run([sys.executable, "./tbtaf/ide/ide.py"])

if __name__ == "__main__":
    event_handler = DevHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        subprocess.run([sys.executable, "./tbtaf/ide/ide.py"], check=True)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
