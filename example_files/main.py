

################## METHODS #####################
################################################
def findVariableIndex(variable, variableNames):
    if variable in variableNames:
        return variableNames.index(variable)
    print("findVariableIndex:: VARIABLE DOES NOT EXIST")
    return 0

def checkExpression(num1, operator, num2):
    if num1 == 0 or num2 == 0:
        return True
    elif operator == "=":
        return num1 == num2
    elif operator == "!":
        return num1 != num2
    elif operator == "<":
        return num1 < num2
    elif operator == ">":
        return num1 > num2
    else:
        print("checkExpression:: INCORRECT OPERATOR ", operator)
        return False


######## Find Most Constrained Variable ########
def findMostConstrainedVar(constraints, variableNames):
    mostConstrainedVar = variableNames[0]
    mostNumConstraints = 0
    indexOfMostConstrainedVar = -1
    numConstraintsforVar = 0
    for variable in variableNames:
        for constraint in constraints:
            if variable in constraint:
                numConstraintsforVar+=1
        if mostNumConstraints < numConstraintsforVar:
            mostConstrainedVar = variable
            mostNumConstraints = numConstraintsforVar
        numConstraintsforVar = 0

    
    return mostConstrainedVar

######### Find Least Constrained Value ##########
def findLeastConstrainedValue(constraints,variableValues,variable,variableNames):

    variableIndex = findVariableIndex(variable,variableNames)
    dict = {}
    for value in variableValues[variableIndex]:
        dict[value] = 0


    for constraint in constraints:
        arguments = []
        for i in constraint.split(" "):
            arguments.append(i)
        if variable in constraint:
            for value in variableValues[variableIndex]:
                indexOfVariableInArgument = arguments.index(variable)
                if indexOfVariableInArgument == 0:
                    if checkExpression(value, arguments[1], assignment[arguments[2]]):
                        tempNum = dict[value]
                        dict[value] = tempNum+1
                else:
                    if checkExpression(assignment[arguments[2]], arguments[1], value):
                        tempNum = dict[value]
                        dict[value] = tempNum+1
    print(dict) 
    #Sort dict in descending order:
    #sorted_dict = sorted(dict.items(),key=lambda x:x[1],reverse=True)
    #for i in sorted_dict: i[0] = key i[1] = value

    #If all dict values = 0, => FAILURE
    maxCount = 0
    maxValue = 0 
    for value in variableValues[variableIndex]:
        if maxCount < dict[value]:
            maxCount = dict[value]
            maxValue = value
    
    return maxValue


############## Backtracking Method ##############



#################### RUNNER #####################
#################################################

################# Read files ####################
constraints = []
with open('ex1.con') as f:
    for line in f:
        newLine = line.replace("\n","")
        constraints.append(newLine)

variableCounter = 0
with open('ex1.var') as p:
   for line in p:
    variableCounter+=1

variableValues = [[] for i in range(variableCounter)]
counter = 0
variableNames = []
checker = True
with open('ex1.var') as p:
    for line in p:
        for word in line.split(" "):
            if(checker):
                variableNames.append(word[0:1])
                checker = False
            else:
                newWord = word.replace("\n","")
                if(newWord != ""):
                    variableValues[counter].append(newWord)
        checker = True
        counter+=1

assignment = {}
for variable in variableNames:
    assignment[variable] = 0



print("Constraints",constraints)
print("Variable Names:", variableNames)
print("Variables Values: ",variableValues)
print("Assignment: ", assignment)


print(findMostConstrainedVar(constraints,variableNames))
print(findLeastConstrainedValue(constraints, variableValues, variableNames[0], variableNames))
