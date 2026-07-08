import itertools

name=input("Enter the name:")
dob=input("Enter the DOB of victim in DDMMYYYY:")
sc=input("Enter any special character:")
ps=[name,dob,sc]
f=open(f'{name}.txt','w')


for i in range(1, len(ps)+1):
    for combi in itertools.permutations(ps,i):
        word="".join(combi)
        f.write(f'{word}\n')
f.close()
f=open(f'{name}.txt','r')
print(f.read())
f.close()