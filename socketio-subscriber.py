from socketIO_client import SocketIO, ConnectionError

from config import broker_address as HOST
from config import device as CREDENTIALS

def ready(args):
    print "Listening to Gateway {}\n".format(CREDENTIALS['uuid'])

def event(event):
    if isinstance(event, dict):
        print "Payload: {} \nSent from device (uuid): {}\n".format(event['payload'], event['fromUuid'])

def main():
    try:
        socket = SocketIO(HOST, 9180) # port = see socketio config in docker-compose.yml
    except ConnectionError:
        print "Couldn't connect to Meshblu"
        exit(1)

    socket.emit('identity', CREDENTIALS)
    socket.on('ready', ready)
    socket.on('message', event)
    socket.wait()

main()
