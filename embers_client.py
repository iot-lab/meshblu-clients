from constants import HOST, PORT, CREDENTIALS
from socketIO_client import SocketIO, ConnectionError

def ready(args):
    print "Listening to Gateway {}\n".format(CREDENTIALS['uuid'])

def event(event):
    if isinstance(event, dict):
        print "Payload: {} \nSent from device (uuid): {}\n".format(event['payload'], event['fromUuid'])

def main():
    try:
        socket = SocketIO(HOST) #socket = SocketIO(HOST, PORT)
    except ConnectionError:
        print "Couldn't connect to Meshblu"
        exit(1)

    socket.emit('identity', CREDENTIALS)
    socket.on('ready', ready)
    socket.on('message', event)
    socket.wait()

main()
