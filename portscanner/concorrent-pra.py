import concurrent.futures
import time
import random


def task(name):
    print(f'The task {name} is strating...')
    rt=random.randint(1,5)
    time.sleep(rt)
    print(f'The task {name} is completed after {rt}')
    return rt


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    ftask={executor.submit(task,i): i for i in range(5)}

    for future in concurrent.futures.as_completed(ftask):
        task_name=ftask[future]
        try:
            result=future.result()
            print(f"task {task_name} executed succsessfully")
        except Exception as e:
            print(f'task failed {task_name}')