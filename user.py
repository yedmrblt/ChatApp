import pickle
import sys

def addNewUser(username, password):
    try:
        read_file = open(r'users.pkl', 'rb')
        users = pickle.load(read_file)
        read_file.close()

        new_user = {}
        new_user['username'] = username
        new_user['password'] = password

        write_file = open(r'users.pkl', 'wb')
        users.append(new_user)
        pickle.dump(users, write_file)
        write_file.close()

    except Exception as e:
        print 'User cannot added into users.pkl'
        sys.exit()


def login(username, password):
    try:
        read_file = open(r'users.pkl', 'rb')
        users = pickle.load(read_file)
        read_file.close()

        for user in users:
            if user['username'] == username:
                if user['password'] == password:
                    return True
                else:
                    return False
        return False
    except Exception as e:
        print 'Login failed'
        sys.exit()


def printUsers():
    for value in users:
        print value['username']

def initData():
    users = []
    try:
        user_file = open(r'users.pkl', 'wb')
        pickle.dump(users, user_file)
        user_file.close()
    except Exception as e:
        print 'User data file cannot opened for write!'
        sys.exit()
