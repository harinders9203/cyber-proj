a=int(input("Enter a number:"))
fizz=a%3
buzz=a%5
if (fizz == 0 and buzz == 0):
    print('fizzbuzz')
elif(fizz==0):
    print('fizz')
elif(buzz==0):
   print('buzz')
else:
    print("This number is neither fizz nor buzz")