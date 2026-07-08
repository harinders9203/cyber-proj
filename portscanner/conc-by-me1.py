import random
import concurrent.futures
import time
import os


def task(name):
    print(f"The task {name} is execuiting....\n")
    rt=random.randint(1,5)
    rt=time.sleep(rt)
    print(f"The time is completed after {rt}s\n")
    os.system("cls")
    return rt


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    ft={executor.submit(task,i):i for i in range(6)}
    for fts in concurrent.futures.as_completed(ft):
        fnshdtsk=ft[fts] #finished task
        try:
            print(f'The task is completed\n')
        except Exception:
            print("The task is failed")