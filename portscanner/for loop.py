for i in range(100):
    if(i%3==0 and i%5==0):
        print(f'fizzbuzz n={i}\n')
    elif(i%3==0):
        print(f'fizz n={i}\n')
    elif(i%5==0):
        print(f'buzz n={i}\n')
    else:
        print(f"The {i} is neither fizz nor buzz")