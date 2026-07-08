import os


name=input("Enter the name of file:")

if(os.path.exists(name)):
    print(f"The file is already exists.\n")
    print("Here's the content:")
    file=open(name,'r')
    print(file.read())
    ch=input("if you want to update content write 'update'\nfor replace write'replace'\notherwise enter 'none':").lower()
    if(ch=='update'):
        f=open(name,'a')
        cont=input("Enter the content for update:")
        f.write(cont)
        f.close()
        f=open(name,'r')
        print(f.read())
    elif(ch=='replace'):
        f=open(name,'w')
        cont=input("Enter the new content:")
        f.write(cont)
        f.close()
        f=open(name,'r')
        print(f.read())
    else:
        print("Thanks for using")
else:
    file=open(name,'w')
    print("File is created")
    s=input("Enter the content you want to insert:")
    file.write(s)
    ch=input('for update content write "update" \n for replace old content write "replace"\n otherwise write "None":').lower()

    if(ch=='update'):
        f=open(name,'a')
        cont=input("Enter the content:")
        f.write(cont)
        f.close()
        f=open(name,'r')
        print(f.read())
    elif(ch=='replace'):
        f=open(name,'w')
        cont=input("Enter the content:")
        f.write(cont)
        f.close()
        f=open(name,'r')
        print(f.read())
    else:
        print("thanks for using")
