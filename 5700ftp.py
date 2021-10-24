#!/usr/bin/env python3

import sys


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


def send_command(command):
    if command == 'USER':
        pass  # TODO: This is where a function call is made to create the socket with the username
    elif command == 'PASS':
        pass  # TODO: This is where a function call is made to enter password for the user to the server
    elif command == 'TYPE':
        pass  # TODO: This is where a function call is made to set connection to 8-bit binary mode
    elif command == 'MODE':
        pass  # TODO: This is where a function call is made to set connection to stream mode
    elif command == 'STRU':
        pass  # TODO: This is where a function call is made to set connection to file oriented mode - make new socket
    elif command == 'LIST':
        pass  # TODO: This is where a function call is made to list contents of a directory on the server
    elif command == 'DELE':
        pass  # TODO: This is where a function call is made to delete file on the server
    elif command == 'MKD':
        pass  # TODO: This is where a function call is made to make directory on the server
    elif command == 'RMD':
        pass  # TODO: This is where a function call is made to delete directory on path to the server
    elif command == 'STOR':
        pass  # TODO: This is where a function call is made to upload a file to the server at a directory
    elif command == 'RETR':
        pass  # TODO: This is where a function call is made to download a file from the sever at the path
    elif command == 'QUIT':
        pass  # TODO: This is where a function call is made to ask the server to close the connection
    elif command == 'PASV':
        pass  # TODO: This is where a function call is made to ask the server to open a data channel


def main():
    print(sys.argv)
    res = parse_command(sys.argv)
    send_command(res['operation'])


main()
