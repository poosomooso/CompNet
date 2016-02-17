#1/27/16
#serena.chen@students.olin.edu
import CN_Sockets
import RC4_Demo
import rsa

class UDP_RX(object):
    """1. READ the UDP_TX module before reading or using this one.

This module demonstrates receiving a transmission sent by the UDP_TX module
on a SOCK_DGRAM (UDP) socket.  This module must be started first, so that it
can publish its port address (5280).

2. Run this module before starting UDP_TX.

UDP_TX and UDP_RX will be started on separate (laptop OS) processes.
UDP_TX will prompt for a message, then transmit it to the UDP_RX module over the
loopback IP address ("127.0.0.1").

UDP_RX will receive the message and print it.
While waiting for a message UDP_RX to be started or to send another message, UDP_TX will print a line of "."s one every 2 seonds.





    """


    def __init__(self,IP="127.0.0.1",port=5280):
        

        socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
        #                                      the socket class    the IPv4 address model    The UDP layer 4 protocol    The event name for a socket timout
        #           IPv4       send packets around
        with socket(AF_INET, SOCK_DGRAM) as sock:
            

            sock.bind((IP,port))  # bind sets up a relationship in the linux
                                  # kernel between the process running
                                  # UCP_RX and the port number (5280 by default)
                                  # 5280 is an arbitrary port number.
                                  # It is possible to register a protocol
                                  # with the IANA.  Such registered ports
                                  # are lower than 5000. e.g. HTTP (
                                  # for browser clients and web servers)
                                  # is registered by IANA as port 80
                                  #

            sock.settimeout(2.0) # create a 2 second timeout so that we
                                 # can use ctrl-c to stop a blocked server
                                 # if, for example, the client doesn't work.

            print ("UDP Server started on IP Address {}, port {}".format(IP,port))
            while True:
              try:
                  pq_bytes, source_address = sock.recvfrom(1024)
                  source_IP, source_port = source_address
                  break
              except timeout:
                  continue
              
            while True:
              try:
                  e_bytes, source_address = sock.recvfrom(1024)
                  #source_IP, source_port = source_address
                  break
              except timeout:
                  continue
            pubRSA = rsa.RSA_public(int.from_bytes(pq_bytes,byteorder='big',signed=False), int.from_bytes(e_bytes,byteorder='big',signed=False))


            password = input("What is your password?")
            pass_encoded = bytearray()
            for ch in password:
              print(type(int.from_bytes(ch.encode(encoding='UTF-8'), byteorder='big', signed=False)))
              pass_encoded.append(int.from_bytes(ch.encode(encoding='UTF-8'), byteorder='big', signed=False))
            RC_4_this = RC4_Demo.Olin_RC4(pass_encoded)

            passMessage = bytearray()
            encrypted = pubRSA.encrypt(int.from_bytes(pass_encoded,byteorder='big',signed=False))
            binStr = bin(encrypted)[2:]
            if(len(binStr)%8!=0):
              binStr = '0'*(8-len(binStr)%8)+binStr
            for i in range(0,len(binStr),8):
              passMessage.append(int(binStr[i:i+8],2))

            bytes_sent = sock.sendto(passMessage, (source_IP,source_port))

            while True:
                try:
                    bytearray_msg, source_address = sock.recvfrom(1024) # 1024 is the buffer length
                                                                 # allocated for receiving the
                                                                 # datagram (i.e., the packet)

                    source_IP, source_port = source_address    # the source iaddress is ("127.0.0.1",client port number)
                                                               # where client port number is allocated to the TX process
                                                               # by the Linux kernel as part of the TX network stack))

                    print ("\nMessage received from ip address {}, port {}:".format(
                        source_IP,source_port))
                    print (RC_4_this.crypt(bytearray_msg).decode("UTF-8")) # print the message sent by the user of the  UDP_TX module.

                    bytes_sent = sock.sendto(bytearray_msg, (source_IP, source_port)) # this is the command to send the bytes in bytearray to the server at "Server_Address"
                    print ("{} bytes sent".format(bytes_sent)) #sock_sendto returns number of bytes send.
                except timeout:

                    print (".",end="",flush=True)  # if process times out, just print a "dot" and continue waiting.  The effect is to have the server print  a line of dots
                                                   # so that you can see if it's still working.
                    continue  # go wait again

if __name__ == "__main__":
    UDP_RX()
