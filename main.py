import pyttsx3
import random
from PyDictionary import PyDictionary
from rich import print
from rich.console import Console
import pyphen
syllabels = pyphen.Pyphen(lang='en')

def openfile(name_of_file:str):
    # read a txt file and extract all the words into a list
    name = name_of_file
    text_file = open(name , 'r')
    text = text_file.read()
    #cleaning
    text = text.lower()
    words = text.split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word.replace("'s", '') for word in words]
    # replace â€™ with '
    words = [word.replace("â€™", "'") for word in words]
    #finding uniquecbachelor's
    
    unique = []
    for word in words:
        if word not in unique:
            unique.append(word)
    return unique

dictionary=PyDictionary()
mistakes_file = "mistakes.txt"
corrects_file = "corrects.txt"
words_file = "Words.txt"
important_file = "importants.txt"
words:list = openfile(words_file)
corrects:list = openfile(corrects_file)
important_file_list:list = openfile(important_file)
mistakes_file_list = openfile(mistakes_file)
mistaken_words = []
corrects.sort()
words.sort()

def dump_to_file(file,text):
# Open the file in append & read mode ('a+')
    with open(file, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text)

def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.7)
    engine.say(text)
    engine.runAndWait()

def say_slow(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 0.8)
    engine.say(text)
    engine.runAndWait()

def find_uniques(unique:list,corrects:list):
    """
    List of the words that are in the qunique list but not in the corrects list
    """
    list_of_words = []
    for word in unique:
        if word not in corrects:
            list_of_words.append(word)
    return list_of_words

def printlbl(word:str, true=True):

    lbl = ""
    for letters in word:
        lbl+=(letters+" ")
    
    if true:
        Console().print(lbl, style="bold Green")
    else:
        Console().print(lbl, style="Red")

def printdict(dictionary:dict):
    """
    printing python dictionary
    """
    for key, value in dictionary.items():
        Console().print(key,":", value, style="bold white")

# spliting the string by - s , example: hello -> he-ll-o
# cooperation co-oper-ation
def split_word(word:str):
    word = word.split("-")
    return word

def main():
    unique = find_uniques(words,corrects)
    temp_corrects = []
    word_of_choice = random.choice(unique)
    if len(unique) == 1:
        print("You have learned all the words!")
        return
    
    Console().print('You have [red]'+str(len(unique))+'[/]'+" words to learn", style="white on blue")
    say("You have "+str(len(unique))+" words to learn")
    say("Let's start with the first word")            
    say(word_of_choice)
    
    counter = 0

    while True:
        unique = find_uniques(words, corrects)
        unique = find_uniques(unique, temp_corrects)
        if len(unique) == 1:
            print("You have learned all the words!")
            return
        elif len(unique) % 10 == 0:
            Console().print('[red]'+str(len(unique))+'[/]'+" words to go")
        input_word = str(input("Enter a word: ")).lower()
     
        if input_word == 'exit' or input_word == '0':
            return
        
        if input_word == "r" or input_word == "repeat" and word_of_choice != "repeat":
            say(word_of_choice)
            input_word = str(input("Enter a word: ")).lower()          

        if input_word == "d" or input_word == "definition" and word_of_choice != "definition": 
            with Console().status("Loading the definition..", spinner="dots"): 
                printdict(dictionary.meaning(last_word))        
            input_word = str(input("Enter a word: ")).lower()
                             
        if input_word == "*":
            dump_to_file(important_file,last_word) 
            Console().print(last_word.capitalize(), "added to important words ✅", style="white on blue")
            say(word_of_choice)
            input_word = str(input("Enter a word: ")).lower()     
            
        if input_word == word_of_choice or input_word+'s' == word_of_choice or input_word+'es' == word_of_choice or input_word == word_of_choice+ 's' or input_word == word_of_choice+ 'es':
            Console().print("✅ Correct ✅", style="white on green")
            say(word_of_choice)
            dump_to_file(corrects_file,word_of_choice)
            print(word_of_choice.capitalize())
            temp_corrects.append(word_of_choice)           
            last_word = word_of_choice
            word_of_choice=random.choice(unique)
            say(word_of_choice)  
            counter = 0
        
        elif counter == 1:
            Console().print("Game Over!", style="white on red")
            say("Game Over!")
            print("The word was: ")
            printlbl(word_of_choice.capitalize() + "✅", true=True)            
            printlbl(input_word + "❌", true=False)            
            say("The word was: ")
            say_slow(word_of_choice) 
            if len(split_word(syllabels.inserted(word_of_choice))) > 1:
                say_slow(split_word(syllabels.inserted(word_of_choice)))
                say(word_of_choice)
            dump_to_file(mistakes_file,word_of_choice)
            mistakes_file_list=openfile(mistakes_file)
            if word_of_choice in mistakes_file_list and mistakes_file_list.count(word_of_choice) != 1:
                print("You had problems with this word ", mistakes_file_list.count(word_of_choice), " times")
            defination_decision = str(input("Do you want to see the definition of the word? (y/n)")).lower()
            if defination_decision == 'y':
                with Console().status("Loading the definition..", spinner="dots"): 
                    printdict(dictionary.meaning(word_of_choice)) 
            elif defination_decision == '*':
                dump_to_file(important_file,word_of_choice) 
                Console().print(word_of_choice.capitalize(), "added to important words ✅", style="white on blue")
                say(word_of_choice)    
            elif defination_decision == 'exit':
                return       
            last_word = word_of_choice            
            word_of_choice=random.choice(unique)
            say("Get ready! The next word is: "+str(word_of_choice))       
            counter = 0 
        
        else:
            counter += 1
            print("❌ Incorrect! ❌")
            say("That was incorrect!, try again")         
            say_slow(word_of_choice)
            print("🟥"* len(word_of_choice), len(word_of_choice))

main()

