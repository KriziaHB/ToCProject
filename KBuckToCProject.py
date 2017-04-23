import re

regex = r"([a-zA-z]*)(//|#)(.*)"
numbersRegex = r"(\d[0-9]*)"

class File():
    @staticmethod
    def readFile():
        myList = []
         # r is the default read flag
        with open("NFA1.txt", "r") as file:
            # read each line 
            for line in file:
                # If the line doesn't match the regex statement
                if not re.match(regex, line):
                    # This will split the line based on " //" and only append the first part
                    myList.append(line.split(" //")[0])
        return myList



class Converter(object):

    originalList = []
    states = []
    alphLen = 0
    stateLen = 0
    fileLen = 0

    def __init__(self, ol):
        super(Converter, self).__init__()
        self.originalList = ol
        self.stateLen = len(ol) 


    def step1A(self): # take apart originallist into usable arrays
        # originalList[1] becomes array of finalStates 
        finalState = []
        matches = re.findall(numbersRegex, self.originalList[1])
        for match in matches:
            finalState.append(match)
        return finalState


    def step1B(self): 
        # originalList[2] becomes array of startState
        startState = []
        matches = re.findall(numbersRegex, self.originalList[2])
        for match in matches:
            startState.append(match)
        return startState
    

    def step1C(self): 
        # originalList[3] becomes array of alphabet
        a = self.originalList[3].split("{")[1]
        b = a.split("}")[0]
        c = b.split(",")
        self.alphLen = len(c)
        return c
         
    
    def step1D(self, alphabet): 
        # originalList[0] becomes array of states with each alphabet/transition
        stateMatrix = [] 
        a = self.originalList[0].split("{")[1] 
        b = a.split("}")[0] 
        c = b.split(",") 
        # add in each transition for each state  
        for x in c:  
            d = []
            for y in range(0,self.alphLen):  
                d.append(alphabet[y])
            stateMatrix.append(d)
        # For originalList[6] to end of originalList[] 
        # file length to know when hitting the end 
        self.fileLen = len(self.originalList) 
        # states[current state] = transitions[transition, new state]
        newList = [] 
        for x in range(6,self.fileLen):
            st = self.originalList[x].split(",")[0] 
            tr = self.originalList[x].split(",")[1] 
            newst = self.originalList[x].split(",")[2] 
            index = SearchAlphabet(alphabet, tr) 
            print("state: " + st) 
            # prevent end of file check 
            if (x < self.fileLen-1): 
                print("outer if") 
                # check to see if the next line will be for the same state
                if (self.originalList[x+1].split(",")[0] == st): 
                    newList.append(newst) 
                    print("if / if") 
                else:  
                    print("if / else") 
                    # if a single line for this state, then add immediately 
                    if (len(newList) == 0): 
                        print("if / else / if") 
                        stateMatrix[int(st)][index] = newst
                        print("transition: " + alphabet[index])
                        print("new state: " + stateMatrix[int(st)][index])
                    # if a list of newStates for same transition 
                    else: 
                        print("if / else / else") 
                        newList.append(newst) 
                        stateMatrix[int(st)][index] = newList
                        newList = []
                        for x in range(0,len(stateMatrix[int(st)][index])): 
                            print("transition: " + alphabet[index])
                            print("new state: " + stateMatrix[int(st)][index][x])
            # hit last line of state - transition - new state 
            else:
                print("outer else")  
                # if a single line for this state, then add immediately 
                if (len(newList) < 1): 
                    print("else / if") 
                    stateMatrix[int(st)][index] = newst
                    print("transition: " + alphabet[index])
                    print("new state: " + stateMatrix[int(st)][index])
                # if a list of newStates for same transition 
                else: 
                    print("else / else") 
                    newList.append(newst) 
                    stateMatrix[int(st)][index] = newList
                    for x in range(0,len(stateMatrix[int(st)][index])): 
                        print("transition: " + alphabet[index])
                        print("new state: " + stateMatrix[int(st)][index][x])
                    newList = []
            #print(stateMatrix[int(st)][index]) 
        return stateMatrix 



def SearchAlphabet(alphabet, trans): # search through the alphabet for corresponding index 
    for x in range(0,len(alphabet)): 
        if (alphabet[x] == trans): 
            return x 


        
def main(): 
    # call all functions from main 
    originallist = File.readFile()
    # print(originallist)
    converter = Converter(originallist) 
    # pull apart original list into segments 
    finalStates = converter.step1A()
    startState = converter.step1B() 
    alphabet = converter.step1C() 
    stateMatrix = converter.step1D(alphabet)
    # print(stateMatrix) 


# call main then use main to call all functions 
if __name__ == '__main__':
        main() 