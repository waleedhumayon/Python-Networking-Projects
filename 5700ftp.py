#!/usr/bin/env python3

import socket
import sys

HOSTNAME = "ftp.5700.network"
PORT = 21
USERNAME = "USER saeedw\r\n"
PASSWORD = 'PASS QbuPFIpHnwBlaZSMyY6U\r\n'


# TODO ADD CORRECT FUNCTION IN COMMAND LINE: EX ls, cp, mkdir etc
# TODO ADD SUPPORT FOR 'anonymous' as username

def connect_ftp(host, port):
    control_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_channel.connect((host, port))
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

    if len(text) == 2:
        response['operation'] = text[1]
        return response
    elif len(text) == 3:
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


def send_command_control_channel(control_channel, parsed_input):
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
    elif parsed_input['operation'] == 'MKD':
        msg = "MKD {}\r\n".format(parsed_input['param1'])
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
    elif parsed_input['operation'] == 'RMD':
        msg = "RMD {}\r\n".format(parsed_input['param1'])
        control_channel.send(msg.encode())
        get_ftp_response(control_channel)
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
            data_channel = connect_ftp(ip, port)
            return data_channel
        else:
            print("Could not connect to data channel\n")


def send_command_data_channel(sock, parsed_input):
    if parsed_input['operation'] == 'LIST':
        data_channel = send_command_control_channel(sock, {'operation': 'PASV'})
        msg = "LIST {}\r\n".format(parsed_input['param1'])
        sock.send(msg.encode())
        get_ftp_response(sock)
        get_ftp_response(data_channel)
        get_ftp_response(sock)
    elif parsed_input['operation'] == 'DELE':
        data_channel = send_command_control_channel(sock, {'operation': 'PASV'})
        msg = "DELE {}\r\n".format(parsed_input['param1'])
        sock.send(msg.encode())
        get_ftp_response(sock)
        data_channel.close()
    elif parsed_input['operation'] == 'STOR':
        print("Trying to STOR")
        data_channel = send_command_control_channel(sock, {'operation': 'PASV'})
        path_to_file = parsed_input['param1']
        path_level = path_to_file.split("/")
        file_name = path_level[len(path_level) - 1]
        msg = "STOR {}\r\n".format(path_to_file)
        sock.send(msg.encode())
        response = get_ftp_response(sock)
        if response[0] == "1":
            with open(file_name, "rb") as file:
                while bytes1 := file.read(1):
                    data_channel.sendall(bytes1)
            file.close()
            data_channel.close()
            get_ftp_response(sock)
            print("File: " + file_name + " has been uploaded to the server")
    elif parsed_input['operation'] == 'RETR':  # TODO Needs fix: Gets stuck retrieving data from the data channel!!!!
        data_channel = send_command_control_channel(sock, {'operation': 'PASV'})
        path_to_file = parsed_input['param1']
        path_level = path_to_file.split("/")
        msg = "RETR {}\r\n".format(path_to_file)
        file_name = path_level[len(path_level) - 1]
        print(file_name)
        sock.send(msg.encode())
        response = get_ftp_response(sock)
        if response[0] == "1":
            print("Getting response from data")
            response_data = get_ftp_response(data_channel)  # TODO GETS STUCK HERE!
            print('Got response from data!')
            host_file = open(file_name, 'w+')
            host_file.write(response_data)
            host_file.close()
            data_channel.close()
            get_ftp_response(sock)


def get_pasv_port_ip(response):
    code = response[0]
    path = response[4].replace('.\r\n', '').replace("(", '').replace(")", "").split(",")
    port_string = "(" + path[4] + "<<" + "8)" + "+" + path[5]
    port = eval(port_string)
    print(port)
    ip_address = path[0] + "." + path[1] + "." + path[2] + "." + path[3]
    return port, ip_address, code


def main():
    sock = connect_ftp(HOSTNAME, PORT)
    get_ftp_response(sock)
    logged_in = do_login(sock)

    while logged_in:
        user_input = input().split(" ")
        parsed_input = parse_command(user_input)

        if parsed_input:
            if parsed_input['operation'] == 'QUIT':
                send_command_control_channel(sock, parsed_input)
                sock.close()
                sys.exit()
            elif parsed_input['operation'] == 'PASV':
                data_channel = send_command_control_channel(sock, parsed_input)
                print(data_channel.getpeername(), data_channel.getsockname())
            elif parsed_input['operation'] == 'STOR':
                send_command_data_channel(sock, parsed_input)
            elif parsed_input['operation'] == 'LIST':
                send_command_data_channel(sock, parsed_input)
            elif parsed_input['operation'] == 'RETR':
                send_command_data_channel(sock, parsed_input)
            elif parsed_input['operation'] == 'DELE':
                send_command_data_channel(sock, parsed_input)
            else:
                send_command_control_channel(sock, parsed_input)


main()
