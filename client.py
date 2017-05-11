import sys
import string
import socket
import select
import json
from user import addNewUser, login
from room import listChatRooms

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def run(current_room, username):
    print 'Connected to remote host.'
    prompt()
    while 1:
        #in this case, the read_sockets array will contain either the server socket, or stdin or both
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                message = {'Type' : 'message', 'Room' : current_room, 'Username' : username, 'Message' : msg }
                a = json.dumps(message)
                s.send(a)
                prompt()


def ShowLogInMenu():
    username = raw_input('Username: ')
    password = raw_input('Password: ')
    loginReturnValue = login(username, password)
    if loginReturnValue == True:
        print 'login success'
        ShowChatRoomMenu(username)
    else:
        print '\nUsername or password is not correct!\n'
        ShowLogInMenu()

def ShowCreateAccountMenu():
    username = raw_input('Username: ')
    password = raw_input('Password: ')
    addNewUser(username, password)
    ShowChatRoomMenu(username)


def ShowChatRoomMenu(username):
    roomMenuInput = raw_input('List Chat Rooms, Enter 1 - Join A Chat Room, Enter 2 : ')
    if roomMenuInput == '1':
        # List Chat Rooms
        listChatRooms()
        ShowChatRoomMenu(username)
    elif roomMenuInput == '2':
        # Join Chat Room
        roomName = raw_input('Enter room name : ')
        s.connect((host, port))
        joinMessage = {'Type' : 'room', 'Message' : roomName }
        a = json.dumps(joinMessage)
        s.send(a)
        run(roomName, username)
    else:
        print '\nInvalid Input!\n'
        sys.exit()


# MAIN
if __name__ == '__main__':

    if(len(sys.argv) < 3):
        print 'Usage : python client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    current_room = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'socket created'
    s.settimeout(2)

    # connect to host
    try:

        # MENU - Log In / Create Account
        menuInput = raw_input('Log In, Enter 1 - Create Account, Enter 2 : ')
        if menuInput == '1':
            # Log In
            ShowLogInMenu()
        elif menuInput == '2':
            # Create Account
            ShowCreateAccountMenu()
        else:
            print '\nInavalit Input!\n'
            sys.exit()

    except Exception as e:
        print 'Unable to connect given host'
        print e
        sys.exit()
