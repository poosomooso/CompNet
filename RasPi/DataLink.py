import threading
import queue
import PhysicalLayer
import MorseCode

ID = 'A'
PROTOCOL = 'A'

def transmit():
	recipient = input('ADDRESS OF RECIPIENT: ')
	message = input('MESSAGE TO SEND: ')
	#how to know the morse code length
	splitMessages = []
	currentLen = 0
	currentStr = ''
	#calculating length of message
	for c in message.upper():
		currentStr+=c
		if c == ' ':
			currentLen += 1
		else:
			morse = MorseCode.MorseCode[c]
			for d in morse:
				if d=='.':
					currentLen+=.5
				else:
					d+=1
			currentLen+=.5
		if currentLen>71: #longest letter is 4 seconds long
			splitMessages.append((currentStr,currentLen))
			currentLen = 0
			currentStr = ''
	splitMessages.append((currentStr,currentLen))

	for tup in len(splitMessages):
		PhysicalLayer.physicalTransmit(recipient+' '+ID+' '+PROTOCOL+' '+str(len(splitMessages)-tup)+' '+str(splitMessages[tup][1])+' '+splitMessages[tup][0])

def readMessage(q):
	def extractHeader(m):
		splitmsg = m.split()
		recip = splitmsg[0]
		src = splitmsg[1]
		prot = splitmsg[2]
		remainingMsgs = splitmsg[3]
		dataLen = splitmsg[4]

		spacesbtwn = 5
		headerlen = len(recip+src+prot+remainingMsgs+dataLen)+spacesbtwn

		message = m[headerlen:headerlen+int(dataLen)]

		return {'recipient': recip, 'source':src, 'protocol':prot, 'messagenum':remainingMsgs, 'length':dataLen, 'message':message}
	while(True):
		msg=Q.get()
		data = extractHeader(msg)
		if data['recipient']==ID:
			if int(data['messagenum'])>1:
				message = data['message']
				for i in range(int(data['messagenum']), 1, -1):
					pass #iterate through the next messages and concat string
			else:
				print data['message']



if __name__ == "__main__":
	tx=threading.Thread(target=transmit,name="TRANSMIT")
	tx.start()
	q = queue.Queue
	PhysicalLayer.reciever(q)

	#how to pull from physical layer's strings?
	tx.join()

		


