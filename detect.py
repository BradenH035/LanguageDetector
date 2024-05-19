import sys
import math

alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] #Global alphabet list


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X = {chr(i): 0 for i in range(ord('A'), ord('Z') + 1)}

    with open (filename,encoding='utf-8') as f:
        # Read each char, x, in file f. Check if its a letter or not
         for x in f.read(): 
            x = x.upper() # change everything to lowercase
            if x in X:
                X[x] += 1
  
    f.close()

    #Generate Q1 output string
    output = "Q1\n"
    for letter in X: 
        if letter == "Z":
            output += letter + " " + str(X[letter])
            break
        output += letter + " " + str(X[letter]) + "\n"

    print(output)

    return X

def languageDetector(textInput):
    english, spanish = get_parameter_vectors()
    X = shred(textInput)

    # Print Q2, round each value to 4 decimals
    print("Q2\n" + "{0:.4f}".format(X['A']*math.log(english[0])) + "\n" + 
          "{0:.4f}".format(X['A']*math.log(spanish[0])))
    
    priorPE = math.log(0.6) # Given probability that text is english/spanish 
    priorPS= math.log(0.4) # converted to Python base

    totalEnglishProb = 0
    totalSpanishProb = 0
    

    for i in range(26):
        totalEnglishProb += X[alphabet[i]] * math.log(english[i])
        totalSpanishProb += X[alphabet[i]] * math.log(spanish[i])
    

    fE = totalEnglishProb + priorPE # f(English)
    fS = totalSpanishProb + priorPS # f(Spanish)

    # Print Q3, round each value to 4 decimals
    print("Q3\n" + "{0:.4f}".format(fE) + "\n" + "{0:.4f}".format(fS))

    # P(Y = English | X)
    if fS - fE >= 100:
        pE = 0.0000
    elif fS - fE <= -100:
        pE = 1.0000
    else:
        pE = (1/(1 + math.exp(fS - fE)))

    # Print Q4, round each value to 4 decimals
    print("Q4\n" + "{0:.4f}".format(pE) + "\n")

text = sys.argv[1]
print(text)
languageDetector("samples/letter0.txt")
