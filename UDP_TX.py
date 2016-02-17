#1/27/16
#serena.chen@students.olin.edu
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import RC4_Demo
import rsa

class UDP_TX(object):
    """ Computer Networks Lab 4: Introduction to Sockets.  UDP Transmit example.
This code only transmits a udp message to a known IP_address ("127.0.0.1") and port_number (5280)
The UDP_RX module recieves and prints messages it is sent.
In this example, the UDP_TX process is the client, because the port number of the server (5280) is known to it.
The server, runing UDP_RX, determines the client's port number from each message it receives.
"""


    def __init__(self,Server_Address=("127.0.0.1",5280)):   # create a socket instance.
                                                            # the "address" is IPv4 address ("127.0.0.1") and port number (5280)
                                                            # "127.0.0.1" is a special IPv4 address indicating that the socket will be communicating
                                                            # over a simulated layer 1 and 2 within a single machine (Laptop or Pi)

        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
        # socket = CN_sockets.socket, which is socket.socket with a slignt modification to allow you to use ctl-c to terminate a test safely
        # CN_sockets.AF_INET is the constant 2, indicating that the address is in IPv4 format
        # CN_sockets.SOCK_DGRAM is the constant 2, indicating that the programmer intends to use the Universal Datagram Protocol of the Transport Layer




        with socket(AF_INET,SOCK_DGRAM) as sock:  # open the socket


            print ("UDP_TX client started for UDP_Server at IP address {} on port {}".format(
                Server_Address[0],Server_Address[1]))

            rsa1 = rsa.RSA()
            rsa1.from_message_bit_length()
            pq = rsa1.public.modpq.MOD
            e = rsa1.public.e.value
            print(type(e))

            pq_bytes = bytearray()
            binStr = bin(pq)[2:]
            if(len(binStr)%8!=0):
              binStr = '0'*(8-len(binStr)%8)+binStr
            for i in range(0,len(binStr),8):
              pq_bytes.append(int(binStr[i:i+8],2))
            e_bytes = bytearray([e])

            bytes_sent = sock.sendto(pq_bytes, Server_Address)
            bytes_sent = sock.sendto(e_bytes, Server_Address)

            while True:
              try:
                  password_bytes, source_address = sock.recvfrom(1024)
                  #source_IP, source_port = source_address
                  break
              except timeout:
                  continue
            password_num = rsa1.private.decrypt(int.from_bytes(password_bytes, byteorder='big',signed=False))

            password = bytearray()
            binStr2 = bin(password_num)[2:]
            if(len(binStr2)%8!=0):
              binStr2 = '0'*(8-len(binStr2)%8)+binStr2
            for i in range(0,len(binStr2),8):
              password.append(int(binStr2[i:i+8],2))

            RC_4_this = RC4_Demo.Olin_RC4(password)

            while True:

                str_message = input("Enter message to send to server:\n")

                if not str_message: # an return with no characters terminates the loop
                    break

                bytearray_message = RC_4_this.crypt(bytearray(str_message,encoding="UTF-8")) # note that sockets can only send 8-bit bytes.
                                                                            # Since Python 3 uses the Unicode character set,
                                                                            # we have to specify this to convert the message typed in by the user
                                                                            # (str_message) to 8-bit ascii

                bytes_sent = sock.sendto(bytearray_message, Server_Address) # this is the command to send the bytes in bytearray to the server at "Server_Address"

                print ("{} bytes sent".format(bytes_sent)) #sock_sendto returns number of bytes send.

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
                except timeout:

                    print (".",end="",flush=True)  # if process times out, just print a "dot" and continue waiting.  The effect is to have the server print  a line of dots
                                                   # so that you can see if it's still working.
                    continue  # go wait again

        print ("UDP_Client ended")





if __name__ == "__main__":
    UDP_TX()
