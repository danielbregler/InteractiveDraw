import datetime
from time import sleep
from flask import render_template
from flask import Flask
from flask_socketio import SocketIO, send
from threading import Thread, Event
from random import random

app = Flask(__name__, template_folder='',)
app.config['SECRET_KEY']= 'topsecret!'

# turn flask into a socketIO app
socketio = SocketIO(app)

# signal emitter thread for the monitoring
thread = Thread()
thread_stop_event = Event()

class Monitoring(Thread):
    def __init__(self):
        self.delay =5
        super(Monitoring,self).__init__()
    def runcheck(self):
        print("Checking...")
        while not thread_stop_event.isSet():
            number = round(random()*10, 3)
            print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)    
    def run(self):
        self.runcheck()


@app.route("/data/<id>")
def servexml(id):

    graphxml = '<mxGraphModel dx="896" dy="524" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" background="#ffffff" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="NO DATA" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;" vertex="1" parent="1"><mxGeometry x="334" y="130" width="80" height="80" as="geometry"/></mxCell></root></mxGraphModel>'

       
#        graphxml = open(id+'.xml', 'r').read()
    return graphxml

@app.route('/monitor/<id>')
def monitor(id):
    return render_template('monitor.html', id=id)

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@socketio.on('connect')       
def connect():
    global thread
    print('Connect ')   

    if not thread.isAlive():
        print("Starting Monitoring Thread")
        thread = Monitoring()
        thread.daemon = True
        thread.start()
        

@socketio.on('disconnect')
def disconnect():
    print('Disconnected')


if __name__ == '__main__':
    print('STARTING SERVER')
    socketio.run(app)

    
