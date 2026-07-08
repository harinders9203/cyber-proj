import itertools

name=input("Enter the name of the victim:")

file=open(f'{name}.txt','w')

for word in itertools.product(name,repeat=len(name)):
    a="".join(word)
    file.write("".join(word)+'\n')

file=open(f'{name}.txt','r')
print(file.read())
# print(dir(itertools))