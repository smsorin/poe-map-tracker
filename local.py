import maps_db
import item_parser
import map
import fragment
import contract
import config

import datetime
import re
import time
import threading
import win32clipboard
import os


def _GetClipBoard():
    try:
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()    
    except:
        print("Can't get the clipboard, trying again later")   
        return ""
    return text

def _ParseTime(text):
    return int(datetime.datetime.strptime(entered.group[1], '%Y/%m/%d %H:%M:%s').timestamp())

class LocalLoop():    
    def __init__(self, socketio):
        self.mapsDB = maps_db.MapsDB(config.MAPS_DB)
        self.mapsDB.Load()
        self.on_update = None
        self.current_item = None
        self.last_clipboard_text = ""
        self.current_fragments = []
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        
        socketio.on_event('start_map', self.StartMap)
        socketio.on_event('stop_map', self.StopMap)
        socketio.on_event('save_map', self.SaveMap)
        socketio.on_event('died', self.Died)
        socketio.on_event('undo_death', self.UndoDeath)
        socketio.on_event('map_fail', self.MapFail)
        socketio.on_event('remove_map', self.RemoveMap)

        self.poe_log = open(config.POE_CLIENT_LOG, 'r')
        self.poe_log.seek(0, os.SEEK_END)

    def RemoveMap(self, map_id):
        if not self.mapsDB.remove(map_id):
            print("Error. Removing the map failed.")
        
    def UpdateCurrentItem(self, new_item):
        self.current_item = new_item
        for f in self.current_fragments:
            self.current_item.AddFragment(f)

    def UpdateFrament(self, new_fragment):
        is_new = True
        for i in range(len(self.current_fragments)):
            if self.current_fragments[i].name == new_fragment.name:
                self.current_fragments[i] = new_fragment
                is_new = False
        if is_new:
            self.current_fragments.append(new_fragment)        
            if self.current_item:
                self.current_item.AddFragment(new_fragment)

    def Died(self):
        if self.current_item is None: return
        self.current_item.deaths += 1
        if self.current_item.deaths > 6:
            self.current_item.deaths = 6
        if self.on_update: self.on_update()
    
    def UndoDeath(self):
        if self.current_item is None: return
        self.current_item.deaths -= 1
        if self.current_item.deaths < 0:
            self.current_item.deaths = 0
        if self.on_update: self.on_update()
    
    def MapFail(self):
        if self.current_item is None: return
        self.current_item.deaths = 6        
        if self.on_update: self.on_update()

    def StartMap(self):
        if self.current_item is None: return
        # Maybe remove fragments
        new_fragments = []
        for f in self.current_fragments:
            f.stack -= 1
            if f.stack > 1:
                new_fragments.append(f)

        self.current_fragments = new_fragments
        self.current_item.map_start = int(time.time())
        if self.on_update: self.on_update()

    def StopMap(self):
        if self.current_item is None: return
        self.current_item.map_stop = int(time.time())
        if not self.current_item.map_start:
            self.current_item.map_start = int(time.mktime(self.current_item.time))
        if self.on_update: self.on_update()
        
    def SaveMap(self):
        if not self.current_item.map_stop:
            self.StopMap()
        self.mapsDB.Save(self.current_item)
        self.current_item = None
        if self.on_update: self.on_update()

    def doLogUpdate(self):     
        while line := self.poe_log.readline():
             entered = re.match(line, r'([\d/]+ [\d:]+) .* : You have entered (.*)\.')
             if entered:
                t = _ParseTime(entered.group[1])
                location = entered.group[2]
                if location == "Cartographer's Hideout":
                    # Entered the hideout, possible map end event.
                    if self.current_item and self.current_item.map_start and not self.current_item.map_stop:
                        self.current_item.map_stop = t
                        print(t, int(time.time()))  # DEBUG
                        if self.on_update: self.on_update()
                elif self.current_item and location + ' Map' == self.current_item.name:
                    # Entered the map, possible map start event
                    print(t, int(time.time()))  # DEBUG
                    if not self.current_item.map_start:
                        self.current_item.map_start = t
                    # Remove the map stop since we're back in the map.
                    if self.current_item.map_stop:
                        self.current_item.map_stop = 0
                    if self.on_update: self.on_update()
                else:
                    print('Player went somewhere I don\'t know about:', location)
                    if self.current_item:
                        print('Waiting for player to go to:', self.current_item.name)
                continue   
             slain = re.match(line, r'([\d/]+ [\d:]+) .* has been slain\.')
             if slain:
                self.Died()             

    def loop(self):
        last_text = None
        while True:
            time.sleep(0.3)
            text = _GetClipBoard()        
            if text != last_text:     
                last_text = text
                print('New text in clipboard: ', text)
                item = item_parser.ParseItem(text)
                if isinstance(item, map.Map) or isinstance(item, contract.Contract):
                    self.UpdateCurrentItem(item)
                elif isinstance(item, fragment.Fragment):
                    self.UpdateFrament(item)                
                
                if self.on_update: self.on_update()
            self.doLogUpdate()
    
