
#Word List Sourced From: https://github.com/dolph/dictionary

MINIMUM_WORD_LENGTH = 3
MAX_WORDS = 4
CHAR_TO_INDEX = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}
INDEX_TO_CHAR = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class WordBuckets:
    def __init__(self):
        self.startingBuckets = []
        #self.endingBuckets = []
        for i in range(26):
            self.startingBuckets.append([])
            #self.endingBuckets.append([])
    def CharToIndex(self,char):
        return CHAR_TO_INDEX[char.lower()]
    def Insert(self,word):
        self.startingBuckets[self.CharToIndex(word[0])].append(word)
        #self.endingBuckets[self.CharToIndex(word[len(word)-1])].append(word)
    def __str__(self):
        total = ""
        for b in self.startingBuckets:
            total += "s: "+str(b)+"\n"
        for e in self.endingBuckets:
            total += "e: "+str(e)+"\n"
        return total

class LetterBoxPuzzle:
    def __init__(self,sides : list,wordBucket : WordBuckets):
        self.sides = sides
        self.wordBucket = wordBucket
        self.solutions = []
    def ReturnLetters(self):
        letters = []
        for side in self.sides:
            for l in side:
                letters.append(l)
        return letters

    def IsSameSide(self,char1,char2):
        for side in self.sides:
            if(char1 in side and char2 in side):
                return True
        return False
    def CullBucket(self,buckets,validLetters):
        for bucket in buckets:
            for word in bucket[:]:
                lastChar = ""
                for char in word:
                    if (char not in validLetters or lastChar == char or self.IsSameSide(char,lastChar)):
                        bucket.remove(word)
                        break
                    lastChar = char
    def CullBucketWords(self):
        validLetters = self.ReturnLetters()
        self.CullBucket(self.wordBucket.startingBuckets,validLetters)
        #self.CullBucket(self.wordBucket.endingBuckets,validLetters)

    def IsSolved(self,wordList):
        letters = self.ReturnLetters()
        for word in wordList:
            for char in word:
                if(char in letters):
                    letters.remove(char)
        return len(letters) == 0

    def GetNextBucket(self,word):
        return self.wordBucket.startingBuckets[CHAR_TO_INDEX[word[len(word)-1]]]

    def Solve(self,words=[],singleSolution=True):
        i = 0
        for bucket in self.wordBucket.startingBuckets:
            if(len(bucket) == 0):
                continue

            res = self.RecursiveSolve(bucket,words,singleSolution)
            if(res != False):
                self.solutions.append(res)
                if(singleSolution):
                    break
            i += 1
            print("Percent Done: "+str((i / 26.0) * 100.0))
    def RecursiveSolve(self,bucket,words,singleSolution):
        if(self.IsSolved(words)):
            #print("Solution: ",words)
            return words
        elif(len(words) == MAX_WORDS):
            return False

        for nextWord in bucket:
            newWordList = words[:]; newWordList.append(nextWord)
            res = self.RecursiveSolve(self.GetNextBucket(nextWord),newWordList,singleSolution)
            if(res == -1):
                return -1
            if(res != False):
                self.solutions.append(res)
                if(singleSolution):
                    return -1

        return False
    def SortSolutions(self):
        self.solutions.sort(key=(lambda x:len(x)))


def BucketWords(fileName):
    buckets = WordBuckets()
    wordFile = open(fileName,'r')
    for word in wordFile.read().split('\n'):
        if(len(word) >= MINIMUM_WORD_LENGTH):
            buckets.Insert(word)

    wordFile.close()
    return buckets


# puzzle = LetterBoxPuzzle([['a','c','o'],['h','l','u'],['d','p','g'],['y','r','n']],buckets)

if __name__ == '__main__':
    buckets = BucketWords("popular.txt")
    print("Words Bucketted")
    while True:
        sides = []
        for i in range(4):
            print("Enter the words of side("+str(i)+"), with spaces between each letter")
            sides.append(input().lower().split(" "))
        print(sides)
        puzzle = LetterBoxPuzzle(sides,buckets)
        #puzzle = LetterBoxPuzzle([['a', 'c', 'o'], ['h', 'l', 'u'], ['d', 'p', 'g'], ['y', 'r', 'n']], buckets)
        removeCount = puzzle.CullBucketWords()

        print("Single(0) or All(1) Solutions?")
        solutionType = input()
        if(solutionType == "0"):
            print("Solving for single...")
            puzzle.Solve(singleSolution=True)
        else:
            print("Solving for all...")
            puzzle.Solve(singleSolution=False)
        puzzle.SortSolutions()
        print("Solution(s):",puzzle.solutions)