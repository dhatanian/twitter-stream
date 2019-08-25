from twython import TwythonStreamer
import eventlet
from eventlet.green import threading

class TwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self.callbacks = dict()
        self.lock = threading.Lock()
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, token, token_secret)

    def on_success(self, t):
        if 'place' in t and t['place'] is not None:
            print('Sending tweet')
            with self.lock:
                for callback in self.callbacks.values():
                    callback(t)
            eventlet.sleep(0.5)
        eventlet.sleep(0.1)
    
    def add_callback(self, id, callback):
        with self.lock:
            self.callbacks[id] = callback

    def remove_callback(self, id):
        with self.lock:
            del self.callbacks[id]

    def on_error(self, status_code, data):
        print(status_code)
        if status_code==420:
            eventlet.sleep(1)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()