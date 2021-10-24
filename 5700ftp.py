#!/usr/bin/env python3

import socket
import sys

HOSTNAME = "ftp.5700.network"
PORT = 21
USERNAME = "USER saeedw\r\n"
PASSWORD = 'PASS QbuPFIpHnwBlaZSMyY6U\r\n'


def connect_ftp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOSTNAME, PORT))
    print("Socket connected!")
    return sock


def get_ftp_response(sock):
    response = ''
    while "\r\n" not in response:
        message = sock.recv(1024)
        response += message.decode()

    print(response)
    return response


def do_login(sock):
    try:
        sock.sendall(USERNAME.encode())
        res = get_ftp_response(sock)
        if res[0] == '3':
            sock.sendall(PASSWORD.encode())
            res2 = get_ftp_response(sock)
            if res2[0] == '2':
                return True
    except:
        print("Could not login, try again!")


def parse_command(text):
    response = {'operation': 0, 'param1': 0, 'param2': 0}

    if len(text) == 3:
        response['operation'] = text[1]
        response['param1'] = text[2]
        return response
    elif len(text) == 4:
        response['operation'] = text[1]
        response['param1'] = text[2]
        response['param2'] = text[3]
        return response
    else:
        print("Invalid number of arguments to FTP client, try again!\n")


def parse_response(text):
    text = text.split(" ")
    print(text)
    server_response = {'code': 0, 'message': 0, 'param': 0}

    if len(text) == 2:
        server_response['code'] = text[0]
        server_response['message'] = text[1]
        return server_response
    elif len(text) == 3:
        server_response['code'] = text[0]
        server_response['message'] = text[1]
        server_response['param'] = text[2]
        return server_response
    else:
        print("Could not parse server response")


def send_command(sock, parsed_input):
    if parsed_input['operation'] == 'TYPE':
        msg = "TYPE I\r\n"
        sock.send(msg.encode())
        get_ftp_response(sock)
    elif parsed_input['operation'] == 'MODE':
        msg = "MODE S\r\n"
        sock.send(msg.encode())
        get_ftp_response(sock)
    elif parsed_input['operation'] == 'STRU':
        msg = "STRU F\r\n"
        sock.send(msg.encode())
        get_ftp_response(sock)
    elif parsed_input['operation'] == 'LIST':
        msg = "LIST\r\n"
        sock.send(msg.encode())
        get_ftp_response(sock)
        # return parse_response(get_ftp_response(sock))
    elif parsed_input['operation'] == 'DELE':
        pass  # TODO: This is where a function call is made to delete file on the server
    elif parsed_input['operation'] == 'MKD':
        pass  # TODO: This is where a function call is made to make directory on the server
    elif parsed_input['operation'] == 'RMD':
        pass  # TODO: This is where a function call is made to delete directory on path to the server
    elif parsed_input['operation'] == 'STOR':
        pass  # TODO: This is where a function call is made to upload a file to the server at a directory
    elif parsed_input['operation'] == 'RETR':
        pass  # TODO: This is where a function call is made to download a file from the sever at the path
    elif parsed_input['operation'] == 'QUIT':
        msg = 'QUIT\r\n'
        sock.send(msg.encode())
        # return parse_response(get_ftp_response(sock))
        get_ftp_response(sock)
    elif parsed_input['operation'] == 'PASV':
        msg = "PASV\r\n"
        sock.send(msg.encode())
        # return parse_response(get_ftp_response(sock))
        get_ftp_response(sock)


def main():
    sock = connect_ftp()
    get_ftp_response(sock)
    logged_in = do_login(sock)

    while logged_in:
        user_input = input().split(" ")
        parsed_input = parse_command(user_input)

        if parsed_input:
            if parsed_input['operation'] == 'QUIT':
                send_command(sock, parsed_input)
                sock.close()
                sys.exit()
            else:
                send_command(sock, parsed_input)


main()
