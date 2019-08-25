from twython import TwythonStreamer
import eventlet
from eventlet.green import threading
import socketio

class TwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, token, token_secret, callback):
        self.callback = callback
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, token, token_secret)

    def on_success(self, t):
        self.callback(t)
        eventlet.sleep(0.1)
    
    def on_error(self, status_code, data):
        print(status_code)
        if status_code==420:
            eventlet.sleep(1)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()