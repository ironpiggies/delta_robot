#!/usr/bin/env python
#author achuwils

import socket
import time

TCP_IP_ROBO = '10.42.0.1'
#TCP_IP = '127.0.0.1'
TCP_PORT_ROBO = 8888
#BUFFER_SIZE = 1024

def sendRoboCommand(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP_ROBO, TCP_PORT_ROBO))
    s.send(msg)
    time.sleep(0.1)
    #data = s.recv(BUFFER_SIZE)
    s.close()


def main():
<<<<<<< HEAD
    sendRoboCommand("wait")
    sendRoboCommand('start')
    sendRoboCommand("stop")
=======
    sendRoboCommand("1")
    sendRoboCommand('2')
    sendRoboCommand("hello world")
>>>>>>> 121b77317bb25df2d4316143a4c827fc87c64036

if __name__ == '__main__': 
	main()
