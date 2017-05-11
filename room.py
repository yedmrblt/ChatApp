import pickle
import sys

def listChatRooms():
    try:
        read_file = open(r'rooms.pkl', 'rb')
        rooms = pickle.load(read_file)
        read_file.close()
        print '***** Chat Rooms *****'
        for room in rooms:
            print room

    except Exception as e:
        print 'Chat rooms cannot read'
        print e
        sys.exit()


def initRoom():

    try:
        rooms = []
        write_file = open(r'rooms.pkl', 'wb')
        pickle.dump(rooms, write_file)
        write_file.close()
    except Exception as e:
        print 'Room data file cannot opened for write!'
        sys.exit()


def addRoom(roomName):
    try:
        read_file = open(r'rooms.pkl', 'rb')
        rooms = pickle.load(read_file)
        read_file.close()

        for room in rooms:
            if room == roomName:
                return

        rooms.append(roomName)

        write_file = open(r'rooms.pkl', 'wb')
        pickle.dump(rooms, write_file)
        write_file.close()
        return

    except Exception as e:
        print 'Error in addSocketToRoom() func'
        print e
        sys.exit()
