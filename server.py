import socket
import threading

clientsockets = []


def send_message_to_all(nickname, message):
    for csocket in clientsockets:
        try:
            csocket.send(nickname + b': ' + message)
        except:
            pass


def listen_connect(nickname, clientsocket, address):
    clientsockets.append(clientsocket)
    while True:
        message = clientsocket.recv(1024)
        if message == b'':
            break

        print(message.decode('utf-8'))
        threading.Thread(target=send_message_to_all, args=(nickname, message)).start()
    clientsockets.remove(clientsocket)
    print('clientsocket end')


def main():
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    # serversocket.bind((host, 23016))
    serversocket.bind(('172.24.30.107', 23014))
    # become a server socket
    serversocket.listen(5)

    while True:
        (clientsocket, address) = serversocket.accept()

        # clientsocket.settimeout(10)
        nickname = clientsocket.recv(1024)
        clientsocket.send(str.encode('歡迎來到聊天室. '))

        threading.Thread(target=listen_connect, args=(nickname, clientsocket, address)).start()


if __name__ == '__main__':
    main()