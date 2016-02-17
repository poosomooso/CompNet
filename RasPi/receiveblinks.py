#
## Introducton to Python breadboarding - Receive Blinks
#
from  SetPin import SetPin
import time
import MorseCode

def receiveblinks(RXpin,blinks=200,duration=.0909090909/2):
    dits=''
    for i in range(blinks):
        num_high = 0
        for j in range(11):
            if RXpin.read_pin():
                num_high += 1
            time.sleep(duration)
        dits+=("." if  round(num_high/11.0)==1 else " ")
    morse_mess = ''
    morse_chars = dits.split(' ')
    for c in morse_chars:
        if c=='':
            morse_mess+=' '
        elif c=='.':
            morse_mess+='.'
        elif c=='...':
            morse_mess+='-'
    message = ''
    d = MorseCode.ReverseCode
    letters = morse_mess.split(' ')
    for l in range(len(letters)):
        if letters[l]=='' and l+1<len(letters) and letters[l+1]=='':
            message+=' '
        else:
            try:
                message+=d[letters[l]]
            except KeyError:
                pass
    print(message)
if __name__ == "__main__":

    with SetPin(16,"GPIO_23",direction="RX") as RXpin:
        receiveblinks(RXpin)
