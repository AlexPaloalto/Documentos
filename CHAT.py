from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    client_ip = request.remote_addr
    print(f'Message from {client_ip}: {msg}')
    send(f'{client_ip}: {msg}', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='192.168.28.23', port=5000)
