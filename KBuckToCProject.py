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
# end of class File 



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
            #    d.append(alphabet[y]) 
                d.append('') 
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
        #    print("state: " + st) 
            # prevent end of file check 
            if (x < self.fileLen-1): 
                # check to see if the next line will be for the same state
                if (self.originalList[x+1].split(",")[0] == st): 
                    newList.append(newst) 
                else:  
                    newList.append(newst) 
                    stateMatrix[int(st)][index] = newList
                    newList = []
            #        for x in range(0,len(stateMatrix[int(st)][index])): 
            #            print("transition: " + alphabet[index])
            #            print("new state: " + stateMatrix[int(st)][index][x])
            # hit last line of state - transition - new state 
            else: 
                newList.append(newst) 
                stateMatrix[int(st)][index] = newList
            #    for x in range(0,len(stateMatrix[int(st)][index])): 
            #        print("transition: " + alphabet[index])
            #        print("new state: " + stateMatrix[int(st)][index][x]) 
                newList = []
            #print(stateMatrix[int(st)][index]) 
        return stateMatrix 
# end of class Converter (Step 1) 



def SearchAlphabet(alphabet, trans): # search through the alphabet for corresponding index 
    for x in range(0,len(alphabet)): 
        if (alphabet[x] == trans): 
            return x 
# end of SearchAlphabet 



def Step2(SM, A): # NFA to DFA subset reconstruction 
    oldSM = SM 
    newSM = SM
    myList = []
    #go through each possibility 
    for st in range(0,len(oldSM)): 
        # follow all emp to end states 
        for trans in range(1,len(A)): #skip empties (check them in follow) 
            myList = Follow(oldSM,st,trans,trans,'no')
            # order numerically and remove duplicates
            newSM[st][trans] = list(set(myList)) 
    return(newSM) 
# end of Step2  



def Follow(oldSM, st, t, trans, u): 
    print("st: " + str(st) + " t: " + str(t) + " trans: " + str(trans) + " u: " + str(u))
    newState = st # gets passed back to newSM
    used = u #keeps track if used the current transition 
    newList = []
    S = int(st) 
    T = int(trans) 
    r = 0

    # nothing in that set 
    if (oldSM[S][T] == ''):  
        T = 0
    # nothing even with empty transition 
    if (oldSM[S][T] == ''): 
        return('') 

    #traverse the oldSM to get all possible paths  
    for x in range(0,len(oldSM[S][T])): # current state possibilities
    #    print("here") 
    #    print(oldSM[S][T][x]) 
        if (used == 'yes'): # traverse only empties 
            r = 1
        else: 
            r = len(oldSM[x])
        print("used " + used) 
        for y in range(0,r): #all possibilities from new start state 
            print("in") 
            for z in range(0,len(oldSM[x][y])): #even empties 
                newState = oldSM[x][y][z]
    #            print(newState) 
                if (newState != ''): # recursion for paths 
                    print("new " + str(newState)) 
                    newList.append(int(newState)) 
                    if (used == 'no' and trans == t): # transition string not used yet 
                        return(Follow(oldSM,newState,t,y,'yes'))
    return(newList) 
# end of Follow 



def main(): 
    # call all functions from main 
    originallist = File.readFile()
    # print(originallist)
    # converter is step 1 
    converter = Converter(originallist) 
    # pull apart original list into segments 
    finalStates = converter.step1A()
    print("Final States: ") 
    print(finalStates)
    startState = converter.step1B() 
    print("Start State: ") 
    print(startState) 
    alphabet = converter.step1C() 
    print("Alphabet: ") 
    print(alphabet) 
    stateMatrix = converter.step1D(alphabet)
    print("Original NFA State Matrix: ") 
    print(stateMatrix) 

    # expand matrix for every possibility (SM is new expanded stateMatrix) 
    SM = Step2(stateMatrix, alphabet) 
    print("Expanded DFA State Matrix: ") 
    print(SM)
    print("-- SPACE for TESTING --") 
    print("should be 10") 
    print(SM[9][2]) 
    print("should be 1, 2, 3, 4, 6, 7, 8")
    print(SM[5][1])
    print("should be empty") 
    print(SM[8][1])
# end of main  



# call main then use main to call all functions 
if __name__ == '__main__':
        main() 
# end 