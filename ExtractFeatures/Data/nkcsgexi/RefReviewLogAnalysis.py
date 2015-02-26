from twisted.python.util import println
import re
class Revision:
    def __init__(self):
        self.lines = list()
    def addLine(self, line):
        self.lines.append(line)
    def hasContent(self):
        return len(self.lines) > 0
    def toString(self):
        return "Accept"
    def getCodeChangeType(self, line):
        if(line.find("Changed") != -1):
            return 1
        if(line.find("Removed") != -1):
            return 2
        if(line.find("Added") != -1):
            return 3
        return 4
    def getTailingInt(self, text):
        numbers = re.findall('\d+', text)
        return numbers[len(numbers) - 1]
    def categorizeAllLines(self):
        changed = list()
        added = list()
        removed = list()
        for line in self.lines:
            type = self.getCodeChangeType(line) 
            number = self.getTailingInt(line)
            if(type == 4):
                continue
            if(type == 1):
                changed.append(number)
            if(type == 2):
                removed.append(number)
            if(type == 3):
                added.append(number)
        return [changed, removed, added]
    def calculatePercentage(self):
        numbers = self.categorizeAllLines()
        allChanged = numbers[0]
        allRemoved = numbers[1]
        allAdded = numbers[2]
        overall = "All change: " + allChanged[0] + " " + allRemoved[0] + " " + allAdded[0]
        overallChange = int(allChanged[0]) + int(allRemoved[0]) + int(allAdded[0])
        println(overall)
        refactoring = [self.addFromIndexOne(allChanged)
                       ,self.addFromIndexOne(allRemoved), 
                       self.addFromIndexOne(allAdded)]
        refactoringInfo = 'Refactoring change: ' + str(refactoring[0]) + ' ' + str(refactoring[1]) + ' ' + str(refactoring[2])
        refactoringChange = refactoring[0] + refactoring[1] +refactoring[2] 
        println(refactoringInfo)
        self.percentage = float(refactoringChange) / overallChange
    def addFromIndexOne(self, list):
        count = 0
        for i in range(1, len(list) - 1):
            count += int(list[i])
        return count
    
def isStart(line):
    return (line.find("=========") != -1)
fname = "/home/xige/Desktop/StudyInfo.log"
with open(fname) as f:
    content = f.readlines()
allRevisions = list()
index = 0

current = Revision()
for line in content:
    if(isStart(line) == True):
        if(current.hasContent()):
            current.calculatePercentage()
            allRevisions.append(current)
            current = Revision()
        continue
    current.addLine(line)
allPerc = 0.0
for revision in allRevisions:
    allPerc += revision.percentage
println("Results:" + str(allPerc/len(allRevisions)))    
    
    
    