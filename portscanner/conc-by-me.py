import random
import time
import concurrent.futures

def task(name):
    print(f'the task {name} is executing...\n')
    rt=random.randint(1,5)
    time.sleep(rt)
    print(f"The task is executed after {rt}s\n")
    return rt

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    ftask={executor.submit(task, i): i for i in range(5)}
    for ft in concurrent.futures.as_completed(ftask):
        taskn=ftask[ft]
        try:
            result=ft.result()
            print("The task is completed\n")
        except Exception:
            print("The task isn't completed\n")