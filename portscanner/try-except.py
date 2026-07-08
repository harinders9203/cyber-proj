# try:
#     a=input("Enter a name:")
# except KeyboardInterrupt:
#     print("\nYou give unexpected input")



a=int(input("Enter a number:"))
a1=int(input("Enter a number:"))
try:
    print(a/a1)
except ZeroDivisionError:
    print("its not divisble by zero")