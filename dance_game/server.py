import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    """Start sending the video feed to the client when connected"""
    while True:
        success, frame = camera.read()
        if success:
            # Convert the frame to bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Send the frame to the client
            emit('video_feed', {'data': frame_bytes}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
