import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000
        return round(temp, 1)
    except:
        return 0.0

@app.route('/')
def index():
    return render_template('index.html')

def background_thread():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        temp = get_cpu_temp()
        
        processes = []
        for proc in sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)[:3]:
            processes.append({
                'name': proc.info['name'],
                'cpu': proc.info['cpu_percent']
            })

        socketio.emit('stats', {
            'cpu': cpu,
            'mem': mem,
            'temp': temp,
            'procs': processes
        })
        socketio.sleep(1) 

if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    print("Server started on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)