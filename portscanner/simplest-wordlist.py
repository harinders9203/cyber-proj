#simple wordlist

words=['admin','admin123','root','root123']
f=open('f1.txt',"w")
n=words.__len__()
for i in range(n):
    f.write(f'{words[i]}\n')

f.close()
f=open('f1.txt',"r")
print(f.read())