# 6.00 Problem Set 3
# 
# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORDLIST_FILENAME = "D:/DEV/MOOCS/6.00.1x Files/3/words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    letters=[]
    for i in range(len(secretWord)):
        if secretWord[i] not in lettersGuessed:
            return False
    return True


def  getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    a=''
    letters=[]
    for i in range(0,len(secretWord)):
        if secretWord[i] in lettersGuessed:
            a+=secretWord[i]
        else :
            a+='_'  
    return a 
            

def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    import string
    a = string.ascii_lowercase
    b=''
    for i in a:
        if i not in lettersGuessed:
            b+=i
    return b
    
#driver function
def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
    letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
    partially guessed word so far, as well as letters that the 
    user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    print "welcome to the game, Hangman!"
    flag=0
    print "I am thinking of a word that is "+str(len(secretWord))+" letters long."
    lettersGuessed = ''
    i=0
    while i<8:
        print "-------------"
        print "You have "+str(8-i) +" guesses left."
        print "Available letters: "+str(getAvailableLetters(lettersGuessed))#usage of helper code 
        guess=raw_input("Please guess a letter: ")
        guess=guess.lower()     #in case of upper case entry

        #condition to check if letter has been guessed or not
        if guess in lettersGuessed:
            print "Oops! You've already guessed that letter: "+str(getGuessedWord(secretWord, lettersGuessed))
        else:
            lettersGuessed+=guess
            if guess in secretWord:
                    print "Good guess: "+str(getGuessedWord(secretWord, lettersGuessed))    
                    if secretWord == getGuessedWord(secretWord, lettersGuessed):
                        print "-------------"
                        print "congratulations, you won!"
                        flag=1
                        break
            else :
                i+=1
                print "Oops! That letter is not in my word: "+str(getGuessedWord(secretWord, lettersGuessed))
    if flag==0 and i==8:
        print "-------------\nSorry, you ran out of guesses. The word was "+str(secretWord)+". "                        

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
