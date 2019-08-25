from flask import Flask, render_template, copy_current_request_context, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from twython_stream import TwitterStream
from eventlet.green import threading
import os
import eventlet
import uuid

#eventlet.monkey_patch(socket=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
socketio = SocketIO(app=app,async_mode='eventlet')

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
token = os.environ['TWITTER_TOKEN']
token_secret = os.environ['TWITTER_TOKEN_SECRET']        

def consume_tweet(t):
    if 'place' in t and t['place'] is not None:
        print('Sending tweet')
        socketio.emit('tweet', t['place'], room='tweets')

stream = TwitterStream(consumer_key, consumer_secret, token, token_secret, consume_tweet)

threading.Thread(target=stream.statuses.sample, daemon=True).start()    

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    join_room('tweets')
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    leave_room('tweets')
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)