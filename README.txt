CS5700 FALL 2021
MIDTERM
WALEED S & TANAY M

** NOTE:
In order to run this program please use:

>$ ./5700ftp COMMAND [ARG 1] [ARG 2]

SUPPORTED COMMANDS:

ls : LIST

rm: DELE

mv: STOR

cp: RETR

mkdir: MKD

rmdir: RMD

quit : QUIT

**

Workflow of project:

1. Set up ssl socket connection with host.
2. Send the initial LOGIN and PASSWORD values to login into FTP server
3. Parse Response ID and info from server reply
4. While user is logged in:
    a. Enter an operation with supporting parameters
    b. Parse the input and send the corresponding COMMAND to ftp server to execute
    c. Parse the response # and info and continue
    d. if user enters exit, send QUIT to server and exit
5. Close the connection

Challenges

For the majority of the project, we could not figure out why commands like
RETR and STOR weren't working. Then we figured out that ftp servers need 2 channels, once for
sending commands and one for transferring actual files and data between the remote server and localhost
After that it was a matter of debugging file permissions, configuring paths on the localhost and
the ftp server and actually being able to traverse directories on the server.

