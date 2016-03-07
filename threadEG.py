#threadtest
import threading
import Queue
import time
import threadtest0
Q1=Queue.Queue(10)

def threadtest(x):
    threadtest0.main()
    f=threading.Thread(target=foo,name="HIGHER")
    g=threading.Thread(target=goo,name="LOWER",args=(x,))
    print("STARTING")
    f.start()
    g.start()

    #synchronize threads when they end
    g.join()
    f.join()
    print("DONE")

def hoo():
    while True:
        #gets the item or waits until there is an item to get
        g= Q1.get()
        print("hoo",g)
        if g != "END GOO":
            yield g
        else:
            break
    raise StopIteration

        
    print("END hoo")

def foo():
    li=list()
    ct=0
    for i in hoo():
        print("foo",i)
        li += [i]
    
    ct+=1
    print("foo",ct,li)
    print("END foo")

def goo(X):
    for i in range(X):
        print("goo",i)
        Q1.put(i)
        time.sleep(.1)
    Q1.put("END GOO")
    print("END goo")

    
    time.sleep(1)

threadtest(5)
