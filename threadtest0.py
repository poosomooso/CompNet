#thread example

import threading
import Queue
import time
import random

Q1=Queue.Queue(100)  #100 limits number of inputs from foo that can be Queued.

def threadEG(x):
    h=threading.Thread(target=hoo,name="HIGHER")
    # note that "goo" is started by "for I in goo()" in function "hoo"
    # goo reads queued items from foo and yields them to hoo
    f=threading.Thread(target=foo,name="LOWER",args=(x,))
    print("STARTING")
    h.start()
    f.start()
    f.join()
    h.join()
    print("DONE")

def hoo():
    li=list()
    ct=0
    for I in goo():
        print("hoo",I)
        li += [I]
    
    ct+=1
    print("hoo",ct,li)
    print("END hoo")


def goo():
    "gets values from Q1 queue; foo puts values onto Q1 queue"
    while True:
        g = Q1.get()
        
        print("goo",g)
        if g != "END FOO":
            yield g
        else:
            break
    print("END goo")

def foo(n):
    "gets values from n"
    for s in [random.randint(1,n**2) for rr in range(n)]:
        print("foo",s)
        Q1.put(s)
        time.sleep(.1)
        
    Q1.put("END FOO") # tell hoo (Q1.get() thread we are done.
    print("END foo")
    time.sleep(1)


if __name__ == "__main__":
    threadEG(4) # four samples
