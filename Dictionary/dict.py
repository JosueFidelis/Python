import json
import difflib

data = json.load(open("data.json"))


def dictionary(word):
    if (word.upper() in data):
        return data[word.upper()]
    if (word.title() in data):
        return data[word.title()]
    
    word = word.lower()
    if (word in data):
        return data[word]
    else:
        try:
            closest = difflib.get_close_matches(word, data.keys(), 1, 0.7)[0]
            return ["don't enter if", closest]
        except IndexError:
            return "This word isnt in the dictionary"

while True:
    word = input("What word are you searching? press ':Q' to exit\n")

    if (word == ":Q"):
        break
    else:
        dictionary(word)
        meaning = dictionary(word)
        if (type(meaning) == list and meaning[0] != "don't enter if"):
            for i in meaning:
                print(i)
        elif (meaning[0] == "don't enter if"):
            print("Did you mean '%s'?" %meaning[1])
            ans = input("If it is, please type 'y', else type 'n'")
            if ans == "y":
                meaning = dictionary(meaning[1])
                for i in meaning:
                    print(i)
            elif ans == "n":
                print("This word isn't in the dictionary")
            else:
                print("We didn't understand your entry")
        else:
            print(meaning)
        print("\n")
