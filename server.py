import socket
import threading
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 1235))
sock.listen()
ALL_CONNECTIONS = []
ALL_ADRESS = []
BROADCAST = []

def broadcast(conn, MESSAGE):
    for Conn in BROADCAST:
        try:
            if Conn != conn:
                Conn.send(MESSAGE.encode())
        except:
            pass

def client(Connection):
    try:
        while True:
            MESSAGE = Connection.recv(1024).decode()
            if '-/PRIVATE CHAT/-' not in MESSAGE and ':' in MESSAGE:
                print(MESSAGE)
                if '-contacts-' in MESSAGE:
                    SHOW_ALL_CONTACTS(Connection)
                elif '-select-' in MESSAGE:
                    TO = MESSAGE.replace('-select- ','')
                    TO = TO.split(':')
                    TO = int(TO[1])
                    sThread = threading.Thread(target=SENDTOTARGET, args=(Connection,TO))
                    sThread.start()
                    sThread.join()
                elif '-exit-' in MESSAGE:
                    pass
                else:
                    #BROADCAST
                    bThread = threading.Thread(target=broadcast, args=(Connection, MESSAGE))
                    bThread.start()
                    bThread.join()
            else:
                for i in range(len(ALL_CONNECTIONS)):
                    if ALL_CONNECTIONS[i][0] == Connection:
                        uname = ALL_CONNECTIONS[i][1]
                        broadcast(Connection,f'--- {uname} CONNECTION HAS BEEN CLOSED --- \n --- ONCE CHECK YOUR CONTACTS AGAIN --- ')
                        print(f'{uname} Connection has been closed ')
                        del ALL_CONNECTIONS[i]
                        del ALL_ADRESS[i]
                        break
                Connection.close()
                break
    except:
        pass

#PRIVATE CHAT
def SENDTOTARGET(Connection,TO):
    while True:
        MESSAGE = Connection.recv(1024).decode()
        if len(MESSAGE) > 0:
            if '-exit-' in MESSAGE:
                break
            MESSAGE = '-/PRIVATE CHAT/- '+MESSAGE
            ALL_CONNECTIONS[TO][0].send(MESSAGE.encode())
        else:
            for i in range(len(ALL_CONNECTIONS)):
                if ALL_CONNECTIONS[i][0] == Connection:
                    uname = ALL_CONNECTIONS[i][1]
                    msg = f'PRIVATE CHAT ENDED BY {uname.capitalize()} AND {uname.capitalize()} CONNECTION HAS BEEN CLOSED '
                    broadcast(Connection,msg)
                    print(f'{uname} Connection has been closed ')
                    del ALL_CONNECTIONS[i]
                    del ALL_ADRESS[i]
                    del BROADCAST[i]
                    break
            break

def SHOW_ALL_CONTACTS(Conn):
    print('sending all adresses ... ')
    for i in range(len(ALL_ADRESS)):
        connection = str(i) + ' '+str(ALL_ADRESS[i][1]) + ' ' + str(ALL_ADRESS[i][0])
        Conn.send(bytes(connection , 'utf-8'))
        time.sleep(0.1)
    client(Conn)

try:
    while True:
        print('waiting for connections ...')
        Connection ,adress = sock.accept()
        username = Connection.recv(1024).decode()
        CONNECTION = [Connection,username]
        ADRESS = [adress,username]
        ALL_CONNECTIONS.append(CONNECTION)
        ALL_ADRESS.append(ADRESS)
        BROADCAST.append(Connection)
        print(f'Connection has benn established with {adress} with port number {adress}')
        cThread = threading.Thread(target=client,args=(Connection,))
        cThread.start()

except:
    print('SERVER STOPPED!')

