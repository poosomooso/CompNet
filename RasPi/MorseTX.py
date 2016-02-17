# Module MorseTX
from MorseCode import MorseCode


def MorseTX(M):
    for W in M.split(" "):
        for L in W:
            for Dd in MorseCode[L]:
                yield (1,.5) if Dd == "." else(1 ,1.5) #dot or dash
                yield (0,.5) #end of dot or dash
            yield(0,1)#end of letter
        yield (0,2)#end of word
    yield (0,4) #end of message


if __name__ == "__main__":
    print("AN ACE")
    for OOKtuple in MorseTX("AN ACE"):
        print(OOKtuple)
    print("OOK AT ME")
    for OOKtuple in MorseTX("OOK AT ME"):
        print(OOKtuple)



~                                                                               
~                    