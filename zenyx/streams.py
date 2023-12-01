

import json
import threading
import time
import zenyx.pyon as pyon

class object_stream:
    """
    ## Constant data-streaming from a json file.\n
    This can help reduce refresh/compilation times when modifying objects.\n
    To start the `watcher` just do: 
    ```py
    x = object_stream("file.json")
    x.start()
    ```
    To stop streaming data:
    ```py
    x.stop()
    ```
    To read the objects:
    ```py
    x.get_objects()
    ```
    """
    def __init__(self, path: str, debug: bool = True, refresh_time: int = 0.25):
        self.debug = debug
        self.refresh_time = refresh_time
        self.__path = path
        self.__watch_thread = threading.Thread(target=self.__compare_and_execute)
        self.__watch_thread.setDaemon(True)
        self.__on_change_callbacks: list[callable] = []
        self.__run = True
        self.string_cache = self.__read_string_cache()
        self.__object_cache = object()
        self.__set_object_cache(self.string_cache)
        
        
    def __read_string_cache(self):
        with open(self.__path, "r") as read_file:
            return read_file.read()
    
    def __set_object_cache(self, new_cache: str):
        try:
            self.__object_cache = pyon.loads(new_cache)
            self.__call_change_callbacks()
        except json.decoder.JSONDecodeError:
            if (self.debug):
                print("Invalid JSON data... Retrying...")
    
    def __compare_and_execute(self):
        while self.__run:
            new_cache = self.__read_string_cache()
                
            if (self.string_cache != new_cache):
                self.string_cache = new_cache
                self.__set_object_cache(new_cache)
                        
            time.sleep(self.refresh_time)
    
    def __call_change_callbacks(self):
        for callback in self.__on_change_callbacks:
            callback()
    
    def get_objects(self):
        return self.__object_cache
    
    def on_change(self, callback: callable):
        self.__on_change_callbacks.append(callback)
    
    def start(self):
        """Starts running the object_stream thread
        """
        self.__run = True
        self.__watch_thread.start()
    
    def stop(self):
        """Stops the object_stream thread
        """
        self.__run = False


