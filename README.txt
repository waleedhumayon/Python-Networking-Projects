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

Another key challenge was not being able to get responses via the data channel. Ultimately we resolved this
by treating the data channel socket considerably differently than the control channel. It was only used to collect data
regarding files and the ls command.

Finally, a major challenge was understanding the requirements. Specifically, we only realized that the mv anc cp
commands are meant to work both ways, FTP->Local and Local->FTP. Luckily, the implementation of functions such as:
download_command and upload_command made it easy to rewire and build the logic for the two way connection. Had
that not already been created, we would likely not be able to submit a working project.

Both team members worked equally on the code and the overall project. Specific focus was:
Waleed: Command execution, data channel creation and the final logic for mv and cp
Tanay: Command parsing, server response parsing and user input parsing as well as Command execution.

