from multiprocessing import Process, Queue

def foo(x, q):
    print x
    from time import sleep
    sleep(2)
    q.put( "foo ex" )

def bar(x, q) :
    print x
    from time import sleep
    sleep(1)
    q.put( "bar ex" )

if __name__ == '__main__':
    
    queue = Queue()

    p1 = Process(target = foo, args=("foo", queue))
    p2 = Process(target = bar, args=("bar", queue))
    p1.start()
    p2.start()
    #print queue.get()
    p1.join()
    p2.join()
    print queue.get()

