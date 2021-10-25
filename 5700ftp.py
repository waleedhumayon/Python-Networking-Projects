#!/usr/bin/env python3

import socket
import sys

HOSTNAME = "ftp.5700.network"
PORT = 21
USERNAME = "USER saeedw\r\n"
PASSWORD = 'PASS QbuPFIpHnwBlaZSMyY6U\r\n'


def connect_ftp():
    control_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_channel.connect((HOSTNAME, PORT))
    print("Socket connected!")
    return control_channel


def get_ftp_response(control_channel):
    response = ''
    while "\r\n" not in response:
        message = control_channel.recv(1024)
        response += message.decode()

    print(response)
    return response


def do_login(control_channel):
    try:
        control_channel.sendall(USERNAME.encode())
        res = get_ftp_response(control_channel)
        if res[0] == '3':
            control_channel.sendall(PASSWORD.encode())
            res2 = get_ftp_response(control_channel)
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


def send_command(control_channel, parsed_input):
    if parsed_input['operation'] == 'TYPE':
        msg = "TYPE I\r\n"
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
    elif parsed_input['operation'] == 'MODE':
        msg = "MODE S\r\n"
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
    elif parsed_input['operation'] == 'STRU':
        msg = "STRU F\r\n"
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
    elif parsed_input['operation'] == 'LIST':
        msg = "LIST\r\n"
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
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
        path_to_file = parsed_input['param1']
        msg = "RETR {}\r\n".format(path_to_file)
        control_channel.send(msg.encode())
        file_name = path_to_file[-1:path_to_file.find('\\')]
        print(file_name)
        response = get_ftp_response(control_channel)
        host_file = open(file_name, 'w+')
        host_file.write(response)
        host_file.close()
        '''pass'''  # TODO: This is where a function call is made to download a file from the sever at the path
    elif parsed_input['operation'] == 'QUIT':
        msg = 'QUIT\r\n'
        control_channel.send(msg.encode())
        # return parse_response(get_ftp_response(sock))
        get_ftp_response(control_channel)
    elif parsed_input['operation'] == 'PASV':
        msg = "PASV\r\n"
        control_channel.send(msg.encode())
        response = get_ftp_response(control_channel)
        response = response.split(" ")
        port, ip, code = get_pasv_port_ip(response)
        if code == "227":
            data_channel = get_data_channel(ip, port)
            print(data_channel.getpeername())  # Second port/data channel now open
            data_channel.close()  # Closing as we aren't doing anything with it.


def get_pasv_port_ip(response):
    code = response[0]
    path = response[4].replace('.\r\n', '').replace("(", '').replace(")", "").split(",")
    port_string = "(" + path[4] + "<<" + "8)" + "+" + path[5]
    port = eval(port_string)
    ip_address = path[0] + "." + path[1] + "." + path[2] + "." + path[3]
    return port, ip_address, code


def get_data_channel(ip, port):
    data_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_channel.connect((ip, port))
    print("Data channel formed")
    return data_channel



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
