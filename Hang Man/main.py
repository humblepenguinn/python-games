import os
import random


class Game(object):
    def __init__(self): 
        self.words = ["UBUNTU", "PYTHON", "BANNNANA", "APPLE", "LINUX", "WINDOWS", "CAR", "COUNTRIES", "PAKISTAN", "RICKSHAW"]
        self.word = random.choice(self.words)
        self.guess = "".join([str("-") for _ in range(len(self.word))])
        self.wrong_letters = ""
        
    def main(self):
        os.system("clear")
        print("HANGMAN \n")

        print("""
-------
|     
|    
|    
|    
|
|---------""")


        while True:
            print(f"Current Guess: {self.guess}")
            print(f"Wrong Guesses: {self.wrong_letters}")

            letter = input("\nPlease enter a letter. > ").upper()

            if letter in self.word:
                temp = ""
                for index in range(len(self.word)):
                    if letter == self.word[index]:
                        temp += letter

                    elif self.guess[index] != "-":
                        temp += self.guess[index]

                    else:
                        temp += "-"

                self.guess = temp

            else:
                self.wrong_letters += letter

            if self.word == self.guess:
                print("You Win! And you live to play another day!")
                print("""
     O
    \\|/
     |
    / \\""")
                exit()

        
            if len(self.wrong_letters) == 0:
                print("""
            -------
            |     
            |    
            |    
            |    
            |
            |---------""")

            if len(self.wrong_letters) == 1:
                print("""
            -------
            |     O
            |    
            |    
            |    
            |
            |---------""")

            if len(self.wrong_letters) == 2:
                print("""
            -------
            |     O
            |     |
            |     |
            |    
            |
            |---------""")

            if len(self.wrong_letters) == 3:
                print("""
            -------
            |     O
            |    \\|/
            |     |
            |    
            |
            |---------""")

            if len(self.wrong_letters) == 4:
                print("""
            -------
            |     O
            |    \\|/
            |     |
            |    / \\
            |
            |---------""")
                
            if len(self.wrong_letters) == 5:
                print("""
            -------
            |     |
            |     O
            |    /|\\
            |     |
            |    | |
            |---------""")

            
            if len(self.wrong_letters) >= 5:
                print("You Lose! Sorry Sucker!")
                print(f"The word was {self.word}")
                exit()
            
game = Game()
game.main()




