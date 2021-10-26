#!/usr/bin/env python3

import socket
import sys
import re

HOSTNAME = "ftp.5700.network"
PORT = 21
USERNAME = "USER saeedw\r\n"
PASSWORD = 'PASS QbuPFIpHnwBlaZSMyY6U\r\n'
PATH = 'ftp://saeedw:QbuPFIpHnwBlaZSMyY6U@ftp.5700.network/'


# TODO ADD SUPPORT FOR 'anonymous' as username
# TODO ADD SUPPORT FOR MULTIPLE FILE-PATHS IN cp and mv commands

def connect_ftp(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # control_channel.settimeout(10)
    print("Socket connected!")
    return sock


def get_ftp_response(sock):
    sock.settimeout(5)
    try:
        response = ''
        while "\r\n" not in response:
            message = sock.recv(1024)
            response += message.decode()

        print(response)
        return response
    except TimeoutError:
        print("No response from server!")


def do_login(control_channel):
    username, password = get_user_pass(sys.argv[2])
    try:
        #control_channel.sendall(USERNAME.encode())
        control_channel.sendall(username.encode())
        res = get_ftp_response(control_channel)
        if res[0] == '3':
            #control_channel.sendall(PASSWORD.encode())
            control_channel.sendall(password.encode())
            res2 = get_ftp_response(control_channel)
            if res2[0] == '2':
                return True
    except:
        print("Could not login, try again!")


def set_transfer_mode(control_channel):
    msg = "TYPE I\r\n"
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)

    msg = "MODE S\r\n"
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)

    msg = "STRU F\r\n"
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)


def get_passive_mode(control_channel):
    msg = "PASV\r\n"
    control_channel.send(msg.encode())
    response = get_ftp_response(control_channel)
    response = response.split(" ")
    port, ip, code = get_pasv_port_ip(response)
    return port, ip, code
    # if code == "227":
    #     data_channel = connect_ftp(ip, port)
    #     return data_channel
    # else:
    #     print("Could not connect to data channel\n")


def get_pasv_port_ip(response):
    code = response[0]
    path = response[4].replace('.\r\n', '').replace("(", '').replace(")", "").split(",")
    port_string = "(" + path[4] + "<<" + "8)" + "+" + path[5]
    port = eval(port_string)
    ip_address = path[0] + "." + path[1] + "." + path[2] + "." + path[3]
    return port, ip_address, code


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


# def parse_response(text):
#     text = text.split(" ")
#     print(text)
#     server_response = {'code': 0, 'message': 0, 'param': 0}
#
#     if len(text) == 2:
#         server_response['code'] = text[0]
#         server_response['message'] = text[1]
#         return server_response
#     elif len(text) == 3:
#         server_response['code'] = text[0]
#         server_response['message'] = text[1]
#         server_response['param'] = text[2]
#         return server_response
#     else:
#         print("Could not parse server response")

def get_path(url):
    url_split = url.split(".network")
    if (url_split[1].startswith(":")):
        url_split2 = re.split(r':[0-9]+', url_split[1])
        directory = url_split2[1]
    else:
        directory = url_split[1]
    print(directory)
    return directory

def get_user_pass(url):
    user = url[6:url.find(":", 7)]
    passw = url[url.find(":", 5)+1:(url.find('@'))]
    return user , passw

def get_hostname(url):
    hostn = url[url.find("@")+1:url.find("/", url.find("@"))]
    return hostn

def make_directory(control_channel, parsed_input):
    msg = "MKD {}\r\n".format(parsed_input['param1'])
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)


def remove_directory(control_channel, parsed_input):
    msg = "RMD {}\r\n".format(parsed_input['param1'])
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)


def quit_command(control_channel):
    msg = 'QUIT\r\n'
    control_channel.send(msg.encode())
    get_ftp_response(control_channel)
    control_channel.close()
    sys.exit()


def list_command(control_channel, parsed_input):
    if parsed_input['param1'] == 0:
        print("Please give a URL to list the directory from. Try again\n")
        return

    port, ip, code = get_passive_mode(control_channel)
    if code[0] == "2":
        set_transfer_mode(control_channel)
        data_channel = connect_ftp(ip, port)
        data_channel.settimeout(5)
        msg = "LIST {}\r\n".format(parsed_input['param1'])
        control_channel.send(msg.encode())
        # print("Sent LIST")
        get_ftp_response(control_channel)
        # print(data_channel.gettimeout())
        # print("GOT MESSAGE FROM CONTROL")
        get_ftp_response(data_channel)
        # print("GOT MESSAGE FROM DATA")
        get_ftp_response(control_channel)
        # print("GOT MESSAGE FROM CONTROL")
    else:
        print("Could not open data channel")


def download_command(control_channel, parsed_input):
    # if parsed_input['param1'] == 0 or parsed_input['param2'] == 0:
    #     print("Please give the local and remote URL for download to work. Try again\n")
    #     return

    port, ip, code = get_passive_mode(control_channel)
    if code[0] == "2":
        set_transfer_mode(control_channel)
        data_channel = connect_ftp(ip, port)
        path_to_file = parsed_input['param1']
        path_level = path_to_file.split("/")
        msg = "RETR {}\r\n".format(path_to_file)
        file_name = path_level[len(path_level) - 1]
        print(file_name)
        control_channel.send(msg.encode())
        response = get_ftp_response(control_channel)
        if response[0] == "1":
            try:
                bytes_buffer = int(response[response.find("(") + 1: response.find(")")].replace(" bytes", ""))
            except:
                print("Could not calculate total number of bytes being sent, try again")
                return
            with open(file_name, "wb") as file:
                while bytes_buffer != 0:
                    response1 = data_channel.recv(1)
                    file.write(response1)
                    bytes_buffer -= 1
                file.close()
                data_channel.close()
                get_ftp_response(control_channel)


def upload_command(control_channel, parsed_input):
    # if parsed_input['param1'] == 0 or parsed_input['param2'] == 0:
    #     print("Please give the remote and local URL for upload to work. Try again\n")
    #     return

    port, ip, code = get_passive_mode(control_channel)
    if code[0] == "2":
        set_transfer_mode(control_channel)
        data_channel = connect_ftp(ip, port)
        path_to_file = parsed_input['param1']
        path_level = path_to_file.split("/")
        file_name = path_level[len(path_level) - 1]
        msg = "STOR {}\r\n".format(path_to_file)
        control_channel.send(msg.encode())
        response = get_ftp_response(control_channel)
        if response[0] == "1":
            with open(file_name, "rb") as file:
                while bytes1 := file.read(1):
                    data_channel.sendall(bytes1)
            file.close()
            data_channel.close()
            get_ftp_response(control_channel)
            print("File: " + file_name + " has been uploaded to the server")


def delete_command(sock, parsed_input):
    if parsed_input['param1'] == 0:
        print("Please give a URL to delete the file from. Try again\n")
        return

    port, ip, code = get_passive_mode(sock)
    if code[0] == '2':
        set_transfer_mode(sock)
        data_channel = connect_ftp(ip, port)
        msg = "DELE {}\r\n".format(parsed_input['param1'])
        sock.send(msg.encode())
        get_ftp_response(sock)
        data_channel.close()


def main():
    if (len(sys.argv) < 2):
        print("Check usage:\n .5700ftp COMMAND <arg1> <arg2 optional>")
    sock = connect_ftp(HOSTNAME, PORT)
    get_ftp_response(sock)
    logged_in = do_login(sock)

    while logged_in:
        user_input = input().split(" ")
        if len(user_input) > 4:
            print("All input to the client must take the form: COMMAND <param1> <param2>")
        else:
            parsed_input = parse_command(user_input)

            if parsed_input:
                if parsed_input['operation'] == 'quit':
                    quit_command(sock)
                elif parsed_input['operation'] == 'mv':
                    upload_command(sock, parsed_input)
                elif parsed_input['operation'] == 'ls':
                    list_command(sock, parsed_input)
                elif parsed_input['operation'] == 'cp':
                    download_command(sock, parsed_input)
                elif parsed_input['operation'] == 'rm':
                    delete_command(sock, parsed_input)
                elif parsed_input['operation'] == 'mkd':
                    make_directory(sock, parsed_input)
                elif parsed_input['operation'] == 'rmd':
                    remove_directory(sock, parsed_input)



main()
