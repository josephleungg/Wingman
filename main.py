from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send, emit
import socket

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_local_ip')
def get_local_ip():
    local_ip = get_local_ip()
    return jsonify({'local_ip': local_ip})

@socketio.on('connect')
def handle_connect():
    local_ip = get_local_ip()
    emit('local_ip', local_ip)

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send(msg, broadcast=True)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return local_ip

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
