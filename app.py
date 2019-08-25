from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
from twython_stream import TwitterStream
from threading import Thread
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    @copy_current_request_context
    def stream_tweets():
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        token = os.environ['TWITTER_TOKEN']
        token_secret = os.environ['TWITTER_TOKEN_SECRET']
        stream = TwitterStream(consumer_key, consumer_secret, token, token_secret, consume_tweet)
        stream.statuses.sample()
    
    def consume_tweet(t):
        if 'place' in t and t['place'] is not None:
            print('Sending tweet')
            emit('tweet', t['place'])

    print('Client connected')
    emit('my response', {'data': 'Connected'})
    Thread(target=stream_tweets, daemon=True).start()    

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)