MorseCode = {'R': '.-.', 'O': '---', 'Z': '--..', 'E': '.', 'X': '-..-', 'I': '..', 'P': '.--.', 'C': '-.-.', 'Q': '--.-', 'S': '...', 'K': '-.-', 'G': '--.', 'N': '-.', 'T': '-', 'H': '....', 'W': '.--', 'J': '.---', 'D': '-..', 'B': '-...', 'L': '.-..', 'M': '--', 'Y': '-.--', 'V': '...-', 'A': '.-', 'F': '..-.', 'U': '..-'}
ReverseCode = {}
for k in MorseCode.keys():
    ReverseCode[MorseCode[k]]=k

if __name__ == "__main__":
    for k in  sorted(MorseCode):
        print ("{} {}".format(k,MorseCode[k]))
