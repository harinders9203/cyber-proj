import random

#greetings
print("Hello welcome to hangman game")

#wordlist

wordlist=['hacker','cyber','security','ethical','hacking']

#randomly choose a word

r=random.choice(wordlist)

#asking user to choose a word

w=input("Guess the word: ").lower()

for letter in r:
    if(letter==wordlist):
        print('right')
    else:
        print("wrong")

# print(w.lower())