# https://websockets.readthedocs.io/en/stable/
from websockets.sync.server import serve
from queue import Queue, Empty
from threading import Thread
from time import sleep
# from saki.messages import *
import uuid
import json

class SAKIConnection(object):
    def __init__(self, websocket):
        self.websocket     = websocket
        self.thread        = None
        self.request_queue = Queue()
        self.request_map   = {}
    
    
    def _handle_request(self):
        try:
            (proxy_obj, msg) = self.request_queue.get(block=False)
            msg_id = str(uuid.uuid4())
            self.request_map[msg_id] = proxy_obj

            self.websocket.send(msg.build_message(id=msg_id).encode())
        except Empty:
            pass


    def _handle_response(self):
        try:
            msg = self.websocket.recv(0.025)
            if msg:
                msg_id = json.loads(msg)['id']
                if msg_id in self.request_map:
                    proxy_obj = self.request_map[msg_id]
                    proxy_obj.queue.put(SAKIMessage.decode(msg))
        except TimeoutError:
            pass


    def start(self):
        self.thread = Thread(target=self._loop, daemon=True)
        self.thread.start()




class SAKIServer(object):
    def __init__(self, address: str="0.0.0.0", port: int=8765):
        self.address = address
        self.port    = port
        self.server  = None
        self.thread  = None
        self.connection = None
    

    def handle(self, websocket):
        self.connection = SAKIConnection(websocket)
        while True:
            self.connection._handle_request()
            self.connection._handle_response()
            sleep(0.1)


    def start(self):
        self.server = serve(self.handle, self.address, self.port)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

