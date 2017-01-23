#Threaded version of Sock Factory.
#Start Knitter and Packer together.

import time
import threading
from threading import Thread
from queue import Queue

knit_time = 0.01    # Fast producer, slow consumer
pack_time = 0.05

class Knitter:

    def __init__(self, sock_queue):
        self.sock_queue = sock_queue

    def start(self, quantity):
        for sock in range(quantity):
            self.knit(sock)


    def knit(self, sock):
        print('Knitting sock %d' % sock)
        time.sleep(knit_time)
        self.addToOutput(sock)


    def addToOutput(self, sock):
       self.sock_queue.put(sock)


class Packer:
    def __init__(self, name, sock_queue):
        self.name = name
        self.sock_queue = sock_queue


    def start(self):
        while True:
            sock1, sock2 = self.collect_pair_socks();
            print('%s collected %d and %d from the queue' % (self.name, sock1, sock2))
            self.pack(sock1, sock2);
            if self.sock_queue.empty():
                break


    def collect_pair_socks(self):
        sock1 = self.sock_queue.get()   # If no socks, block until one is available
        sock2 = self.sock_queue.get()
        return sock1, sock2


    def pack(self, sock1, sock2):
        print('%s is about to pack pair of socks %d and %d' % (self.name, sock1, sock2))
        time.sleep(pack_time)
        print('%s has packed pair of socks %d and %d' % (self.name, sock1, sock2))
        self.sock_queue.task_done()   # one call per task done
        self.sock_queue.task_done()


    def fetchSock(self):
        return self.sock_queue.get()



def main():

    sock_pile = Queue()

    sock_knitter = Knitter(sock_pile)
    knitter_thread = Thread(target=sock_knitter.start, args=[10])
    knitter_thread.start()

    sock_packer_1 = Packer('Packer 1', sock_pile)
    packer_thread_1 = Thread(target=sock_packer_1.start)
    packer_thread_1.start()

    sock_packer_2 = Packer('Packer 2', sock_pile)
    packer_thread_2 = Thread(target=sock_packer_2.start)
    packer_thread_2.start()

    sock_packer_3 = Packer('Packer 3', sock_pile)
    packer_thread_3 = Thread(target=sock_packer_3.start)
    packer_thread_3.start()

    sock_pile.join()       # Wait for all jobs in queue to be done (knitter and packer will be working)
    knitter_thread.join()  # Wait until knitter is done
    packer_thread_1.join()   # Wait until packer is done
    packer_thread_2.join()   # Wait until packer is done
    packer_thread_3.join()   # Wait until packer is done


    print('All done')

if __name__ == '__main__':
    main()
