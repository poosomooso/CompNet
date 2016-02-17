import random

class RSA:
	def __init__(self):
		def modular_multiplicative_inverse(a,n):
			t = 0
			nt = 1
			r = n
			nr = a%n
			if(n<0):
				n = -n
			if a<0:
				a = n-((-a)%n)
			while(nr!=0):
				quot = round(r/nr)

				tmp = nt
				nt = t-quot*nt
				t = tmp

				tmp2 = nr
				nr = r-quot*nr
				r = tmp2
			if r>1:
				return -1
			if t<0:
				t+=n
			return t

		def random_prime(min,max):
			list = sieve(min,max)
			return random.choice(list)

		def sieve(min,max):
			arr = list(range(2,max))
			index = 0
			while(index<=len(arr)/2):
				prime = arr[index]
				for i in range(len(arr)-1, index, -1):
					if(arr[i]%prime == 0):
						del arr[i]
				if arr[index]<min:
					del arr[index]
				else:
					index+=1
			return arr
		p = random_prime(2,255)
		q = random_prime(2,255)
		n = p*q
		t = (p-1)*(q-1)
		e = random_prime(2,t)
		#import pdb; pdb.set_trace()
		d = modular_multiplicative_inverse(e,t)
		self.n = n #public key 1
		self.e = e #public key 2
		self.d = d #private key
		print("keys: "+str(n)+" "+str(e)+" "+str(d))

	def encrypt(self,m,n,e):
		m_int = int.from_bytes(m, byteorder='big', signed=False)
		crypted = (m_int**e)%n
		b = bytearray()
		binStr = bin(crypted)[2:]
		if(len(binStr)%8!=0):
			binStr = '0'*(8-len(binStr)%8)+binStr
		for i in range(0,len(binStr),8):
			b.append(int(binStr[i:i+8],2))
		return bytes(b)

	def decrypt(self,mEnc, d, n):
		mEnc_int = int.from_bytes(mEnc, byteorder='big', signed=False)
		#import pdb; pdb.set_trace()
		decrypted = (mEnc_int**d)%n #numerical result out of range?????
		print(decrypted)
		b = bytearray()
		binStr = bin(decrypted)[2:]
		if(len(binStr)%8!=0):
			binStr = '0'*(8-len(binStr)%8)+binStr
		for i in range(0,len(binStr),8):
			b.append(int(binStr[i:i+8],2))
		return bytes(b)

if __name__ == "__main__":
	RSA_1 = RSA()
	x = RSA_1.encrypt('hi'.encode(),RSA_1.n, RSA_1.e)
	print(x)
	y = RSA_1.decrypt(x,RSA_1.d, RSA_1.n)
	print(y.decode(encoding='UTF-8'))
