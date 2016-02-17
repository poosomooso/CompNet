#Serena Chen
#Lab 1
import unicodedata
#upperbound: 0x110000
def printCharSet():
	letters = set()
	for x in range(1, 0x110000):
		try:
			for c in unicodedata.name(chr(x)):
				letters.add(c)
		except ValueError:
			pass
	return letters
#bytes([int])
def UTF8_encode(x):
	"""
	y = bin(ord(x))[2:]
	if len(y)<8:
		y = '0'*(8-len(y))+y
	elif len(y)<12:
		y = '0'*(11-len(y))+y
		sub1 = '110'+y[0:5]
		sub2 = '10'+y[5:]
		y = sub1+sub2
	elif len(y)<17:
		y = '0'*(16-len(y))+y
		sub1 = '1110'+y[0:4]
		sub2 = '10'+y[4:10]
		sub3 = '10'+y[10:]
		y = sub1+sub2+sub3
	elif(len(y)<22):
		y = '0'*(21-len(y))+y
		sub1 = '11110'+y[0:3]
		sub2 = '10'+y[3:9]
		sub3 = '10'+y[9:15]
		sub4 = '10'+y[15:]
		y = sub1+sub2+sub3+sub4
	b = bytearray()
	for i in range(0,len(y),8):
		b.append(int(y[i:i+8],2))
	return bytes(b)
	"""
	y = bin(ord(x))[2:]
	b = bytearray()
	if len(y)<8:
		y = '0'*(8-len(y))+y
		b.append(int(y,2))
	else:
		print(y)
		firstByte = len(y)%6
		numBytes = int(len(y)/6)
		if(numBytes+1!=(6-firstByte)):
			numBytes+=1
			y= '0'*(numBytes*5+6-len(y))+y
			firstByte = 6-numBytes
		b.append(int('1'*(numBytes+1)+'0'+y[0:6-numBytes], 2))
		for i in range(0,numBytes):
			print(y[firstByte+(i*6):firstByte+((i+1)*6)])
			b.append(int('10'+y[firstByte+(i*6):firstByte+((i+1)*6)],2))
	return bytes(b)



def UTF8_decode(b):
	#print(b[1])
	stringByte = bin(b[0])[2:]
	if(len(stringByte)<8):
		return chr(int(stringByte,2))
	else:
		numBytes = 0
		while stringByte[numBytes:numBytes+1] != '0':
			print(stringByte[numBytes:numBytes+1])
			numBytes+=1
		s = ''
		s+=stringByte[numBytes:]
		for i in range(1,numBytes):
			x = bin(b[i])
			s+=x[4:]
		return chr(int(s,2))
