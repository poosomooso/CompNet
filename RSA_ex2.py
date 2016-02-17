#import pdb; pdb.set_trace()

p = 61
q = 53
n = p*q
totient = (p-1)*(q-1)
m = input('Message to send: ')
m_ints = []
for ch in m:
	m_ints.append(int.from_bytes(ch.encode(encoding='UTF-8'), byteorder='big', signed=False))
print(m_ints)
e = 17
d = 2753 #modular multiplicative inverse of e
c = [(i**e)%n for i in m_ints]
print(c)
dec = [(i**d)%n for i in c]
print(dec)
b = bytes(dec)
print(b.decode(encoding='UTF-8'))