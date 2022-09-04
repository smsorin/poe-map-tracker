import time
import threading
import win32clipboard

import maps_db
import item_parser
import map
import fragment

def _GetClipBoard():
    try:
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()    
    except:
        print("Can't get the clipboard, trying again later")   
        return ""
    return text

class LocalLoop():    
    def __init__(self):
        self.mapsDB = maps_db.MapsDB()
        self.mapsDB.LoadFrom("maps.pickle")
        self.on_update = None
        self.current_item = None
        self.last_clipboard_text = ""
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        
    def UpdateCurrentItem(self, new_item):
        self.current_item = new_item

    def UpdateFrament(self, new_fragment):
        pass

    def loop(self):
        last_text = None
        while True:
            time.sleep(0.3)
            text = _GetClipBoard()        
            if text == last_text: continue
            
            last_text = text
            item = item_parser.ParseItem(text)
            if isinstance(item, map.Map):
                self.UpdateCurrentItem(item)
            elif isinstance(item, fragment.Fragment):
                self.UpdateFrament(item)                
            
            if self.on_update: self.on_update()
    
