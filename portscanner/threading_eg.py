import threading
import time


def print_num():
    for i in range(6):
        print(i)
        time.sleep(1)

def print_let():
    for lett in 'ABCDEF':
        print(lett)
        time.sleep(1)
def greet():
    for i in range(6):
        print("Hello")
        time.sleep(1)


t1=threading.Thread(target=print_num)
t2=threading.Thread(target=print_let)
t3=threading.Thread(target=greet)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# print_num()
# print_let()