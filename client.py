import socket

HOST = socket.gethostname()
PORT = 8012

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = input("Please input msg:")
    s.send(cmd.encode())
    data = s.recv(1024)
    print (data)

    #s.close()



