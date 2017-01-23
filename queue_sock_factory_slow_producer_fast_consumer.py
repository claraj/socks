#Threaded version of Sock Factory.
#Start Knitter and Packer together.

import time
import threading
from threading import Thread
from queue import Queue, Empty

knit_time = 1.05
pack_time = 0.01    # Slow producer, faster consumer


class Knitter:

    def __init__(self, sock_queue):
        self.sock_queue = sock_queue


    def start(self, quantity):
        for sock in range(quantity):
            self.knit(sock)
        print('Knitter is done')


    def knit(self, sock):
        print('Knitting sock %d' % sock)
        time.sleep(knit_time)
        self.addToOutput(sock)


    def addToOutput(self, sock):
        print('Adding sock %d to queue' % sock)
        self.sock_queue.put(sock)



class Packer:
    def __init__(self, name, sock_queue):
        self.name = name
        self.sock_queue = sock_queue
        self.keep_packing = True


    def start(self):
        while self.keep_packing:
            sock1, sock2 = self.collect_pair_socks();
            if sock1 is not None:
                self.pack(sock1, sock2);
                print('%s collected %d and %d from the queue' % (self.name, sock1, sock2))


    def collect_pair_socks(self):
        try:
            sock1 = self.sock_queue.get(timeout=1)   # If no socks, wait up to one second for one to be available
        except Empty:
            print('The sock queue is empty.')
            return None, None   # no socks, queue is empty

        sock2 = self.sock_queue.get()  # Got to get a second sock to be able to process the first sock. Wait forever.
        return sock1, sock2


    def pack(self, sock1, sock2):
        print('%s is about to pack pair of socks %d and %d' % (self.name, sock1, sock2))
        time.sleep(pack_time)
        self.sock_queue.task_done()   # one call per task done
        self.sock_queue.task_done()
        print('%s has packed pair of socks %d and %d' % (self.name, sock1, sock2))





def main():

    sock_pile = Queue()

    sock_knitter = Knitter(sock_pile)
    knitter_thread = Thread(target=sock_knitter.start, args=[10])
    knitter_thread.start()

    sock_packer = Packer('Packer 1', sock_pile)
    packer_thread = Thread(target=sock_packer.start)
    packer_thread.start()

    knitter_thread.join()  # Block until knitter is done

    print('Knitter is done, stopping packer')

    # Stop packer by setting keep_packing flag
    sock_packer.keep_packing = False
    print('Waiting for packer to stop (it might be waiting for the second sock for a pair)')

    packer_thread.join()   # Block until packer is done
    print('Packer is done')

    sock_pile.join()       # Wait for all jobs to be marked as done

    print('All done.')


if __name__ == '__main__':
    main()
