from threading import Thread
import queue
import time


def funcA():
    time.sleep(1)
    print ("func A")
    
def funcB():
    time.sleep(3)
    print ("func B")

threads = []
threads.append(Thread(target=funcA))
threads.append(Thread(target=funcB))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print ("finished")

    