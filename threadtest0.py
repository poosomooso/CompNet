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
    print("STARTING2")
    h.start()
    f.start()
    f.join()
    h.join()
    print("DONE2")

def hoo():
    li=list()
    ct=0
    for I in goo():
        print("hoo2",I)
        li += [I]
    
    ct+=1
    print("hoo2",ct,li)
    print("END hoo")


def goo():
    "gets values from Q1 queue; foo puts values onto Q1 queue"
    while True:
        g = Q1.get()
        
        print("goo2",g)
        if g != "END FOO":
            yield g
        else:
            break
    print("END goo2")

def foo(n):
    "gets values from n"
    for s in [random.randint(1,n**2) for rr in range(n)]:
        print("foo2",s)
        Q1.put(s)
        time.sleep(.1)
        
    Q1.put("END FOO") # tell hoo (Q1.get() thread we are done.
    print("END foo2")
    time.sleep(1)


def main():
    threadEG(4) # four samples
