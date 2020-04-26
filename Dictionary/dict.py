import mysql.connector
import difflib

con = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)

def convert(tuple, dictionary):
    for word, meaning in tuple:
        dictionary.setdefault(word, []).append(meaning)
    return dictionary

def wordSuggestion(word, cursor):
    firstChar = word[0]
    lastChar = word[len(word) - 1]
    cursor.execute("SELECT * FROM Dictionary WHERE Expression LIKE '%s' OR Expression LIKE '%s'" %(firstChar + '%', '%' + lastChar))
    
    result = cursor.fetchall()

    dictionary = {}    
    dictionary = convert(result, dictionary)

    closest = difflib.get_close_matches(word, dictionary.keys(), 1, 0.7)


    if (closest):
        return ['suggestion' , closest[0], dictionary[closest[0]]]

    return []



def getDefinition(word, cursor):
    cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s'" %word)

    result = cursor.fetchall()
    if result:
        dictionary = {}
        dictionary = convert(result, dictionary)
        return ['ok', word, dictionary[word]]

    result = wordSuggestion(word, cursor)
    
    return result

def printDefinition(definitions):
    definitionNumber = 0
    for i in definitions:
        definitionNumber += 1
        print(str(definitionNumber) + ". " + i)


while True:
    word = input("What word are you searching? press ':Q' to exit\n")
    cursor = con.cursor()
    
    if (word.lower() == ":q"):
        break
    
    definitions = getDefinition(word, cursor)

    if (definitions):
        
        if (definitions[0] == "ok"):
            printDefinition(definitions[2])

        elif(definitions[0] == 'suggestion'):
            print("Did you mean '%s'?" %definitions[1])
            ans = input("If so, please type 'y', if not type 'n'\n")
            if (ans.lower() == "y"):
                printDefinition(definitions[2])
            else:
                print("This word isn't in the dictionary")
    
    else:
        print("Word not found")

    print("\n")
