import socket
from time import gmtime, strftime

class Server():
    
    def __init__(self,x,y):
        print('Start Server')
        self.x = x
        self.y = y

    def var_func(self):
        self.current_time = strftime('%H:%M:%S', gmtime())
        self.client = {}
    
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    def bind_socket(self):
        self.sock.bind((self.x,self.y))
    
    def get_a_message(self):
        self.data, self.address = self.sock.recvfrom(1024)
        self.data = self.data.decode()

    def print_userinfo(self):
        print(self.address[0], self.address[1])

    def append_clients(self):
        if ' <= join to chat!' in self.data:
            self.name = self.data.split(' <= join to chat!')[0]
        if self.name not in self.client: 
            self.client[self.name] = self.address

    def send_message(self):
        if ' <= join to chat!' in self.data:
            self.users_joined_lists = []
            self.username = self.data.split(' <= join to chat!')[0]
            for self.clients in self.client.keys():
                if self.clients != self.username:
                    self.message_to_joined_list = (self.data.encode(),self.client[self.clients])
                    self.users_joined_lists.append(self.message_to_joined_list)
            for self.user_joined_list in self.users_joined_lists:
                self.sock.sendto(*self.user_joined_list)

        elif r'\users' in self.data:
            self.message_userslist = []
            for self.user in self.client.keys():
                self.message_userslist.append(self.user)
            self.message_to_send = (str(self.message_userslist).encode(), self.address)
            self.sock.sendto(*self.message_to_send)
        
        elif r'\e' in self.data:
            self.username = (self.data.split(r' \e')[1]).split(' ')[0]
            self.message = (self.data.split(r' \e')[0] 
                           + (self.data.split(r'\e' + self.username)[1]))
            if self.username in self.client:
                self.to_this_user = self.client[self.username]
                self.message_to_send = (self.message.encode(), self.to_this_user)
            else:
                self.message_to_send = (('User ' + '"' + str(self.username) + '"' 
                                        + ' not in chat!' 
                                        + ' Enter "\e[username] [text]"' 
                                        + ' to send private message.').encode(), self.address)
            self.sock.sendto(*self.message_to_send)

        else:
            self.users_lists = []
            if self.clients != self.address:
                self.data = (self.data + '   ' + self.current_time)
            for self.clients in self.client.values():
                if self.clients != self.address:
                    self.message_to_list = (self.data.encode(), self.clients)
                    self.users_lists.append(self.message_to_list)
            for self.user_list in self.users_lists:
                self.sock.sendto(*self.user_list)

server = Server('localhost', 8000)
server.var_func()
server.create_socket()
server.bind_socket()

while True:
    try:
        server.get_a_message()
        server.print_userinfo()
        server.append_clients()
        server.send_message()
    except:
        server.sock.close()
 
