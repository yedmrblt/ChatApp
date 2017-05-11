import socket
import sys
import select
import json
from user import initData
from room import initRoom, addRoom

#global ROOMS

def addSocketToRoom(roomName, socket):
    try:

        for room in ROOMS:
            if room['name'] == roomName:
                socketsInRoom = room['sockets']
                socketsInRoom.append(socket)
                return
        newRoom = {'name' : roomName, 'sockets': [socket]}
        ROOMS.append(newRoom)
        return
    except Exception as e:
        print 'Error in addSocketToRoom() func'
        print e
        sys.exit()


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message, roomName):
    # Do not send the message to master socket and the client who has send us the message
    for room in ROOMS:
        if room['name'] == roomName:
            socket_list = room['sockets']
            for socket in socket_list:
                if socket != server_socket and socket != sock:
                    try:
                        socket.send(message)
                    except:
                        # broken socket connection may be, chat client pressed ctrl+c for example
                        socket.close()
                        socket_list.remove(socket)

ROOMS = []

# MAIN
if __name__ == '__main__':

    initData()
    initRoom()



    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 3000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", PORT))
    server_socket.listen(10)

    print 'server socket created'

    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        #The select function monitors all the client sockets and the master socket for readable activity.
        # If any of the client socket is readable then it means that one of the chat client has send a message.
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    jsonData = json.loads(data)
                    if jsonData['Type'] == 'room':
                        addSocketToRoom(jsonData['Message'], sock)
                        addRoom(jsonData['Message'])
                    elif jsonData['Type'] == 'message':
                        broadcast_data(sock, "\r" + '<' + jsonData['Username'] + '> ' + jsonData['Message'], jsonData['Room'])


                except:

                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
