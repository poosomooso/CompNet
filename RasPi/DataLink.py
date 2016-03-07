
def transmit(msg, blink, recipient,source):
	blink.blinkTX(MorseTX(recipient+' '+source+' '+msg))

if __name__ == "__main__":

	while True:
		msg = input("RECIEVE (r) OR TRANSMIT (t) :")
	    if msg.lower() == 'r':
	        break
	    elif msg.lower() == 't':
	        break



