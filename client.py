import socket
import threading

print('"\users" to view a list of online users')
print('r"\e[username] [text]" to send private message')

def read_soket():
    while True:
        data = sock.recv(1024)
        print(data.decode())
server = '', 8000
alias = input('Enter you name: ')
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', 0))
sock.sendto((alias + ' <= join to chat!').encode(), server)
thread_1 = threading.Thread(target = read_soket)
thread_1.start()
while True:
    message = input()
    if r'\users' in message:
        sock.sendto((message).encode(), server)
    elif r'\e' in message:
        sock.sendto(('Message from ' + str(alias) + ': ' 
                      + message).encode(), server)
    else:
        sock.sendto((alias + ': '+message).encode(), server)