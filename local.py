import time
import threading
import win32clipboard

import maps_db

class LocalLoop():    
    def __init__(self):
        self.mapsDB = maps_db.MapsDB()
        self.mapsDB.LoadFrom("maps.pickle")
        self.current_item = None
        self.last_clipboard_text = ""
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def loop(self):
        while True:
            time.sleep(0.3)
            print('.', end='', flush=True)
    
