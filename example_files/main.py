

################## METHODS #####################
################################################

def findVariableIndex(variable, variableNames):
    if variable in variableNames:
        return variableNames.index(variable)
    print("findVariableIndex:: VARIABLE DOES NOT EXIST ", variable)
    return 0

def printAssignment(assignment):
    answer = ""
    for key in assignment:
        answer+=key+"="+str(assignment[key])+","
    print(answer[:-1])

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

def checkAssignment(assignment, constraints, variableNames):
    for key in assignment:
        if assignment[key] == 0:
            return False
    for constraint in constraints:
        arguments = []
        for i in constraint.split(" "):
            arguments.append(i)
        if checkExpression(assignment[arguments[0]], arguments[1], assignment[arguments[2]]) == False:
            return False
    return True

def checkFailure(assignment):
    for key in assignment:
        if assignment[key] == -1:
            return True
    return False


######## Find Most Constrained Variable ########
def findMostConstrainedVar(variableValues, constraints):
    
    dict = {}
    sorted_dict = {}
    for variable in variableNames:
        dict[variable] = len(variableValues[findVariableIndex(variable,variableNames)])
    sorted_dict = sorted(dict.items(),key=lambda x:x[1],reverse=False)
   
    trueOrder = []
    tempGroup = {}
    constrainingVar = ""
    maxConstraining = -1
    numConstraining = 0
    for key in sorted_dict:
        tempGroup = {}
        for i in sorted_dict:
            if not i[0] in trueOrder and dict[key[0]] == dict[i[0]]:
                tempGroup[i[0]] = 0
        for tempKey in tempGroup:
            print("tempGroup:",trueOrder)
            numConstraining = 0
            for constraint in constraints:
                if tempKey[0] in constraint:
                    latterArgument = ""
                    for i in constraint.split(" "):
                        if i != tempKey[0] and i != "=" and i != "!" and i != "<" and i != ">":
                            print("compare ", i, tempKey[0])
                            latterArgument = i
                    print("Checking if ", latterArgument, " is in ",trueOrder)
                    if not latterArgument in trueOrder:
                        numConstraining+=1
            print(tempKey[0], " constraining ",numConstraining, ". Max = ",maxConstraining)
            if maxConstraining < numConstraining:
                maxConstraining = numConstraining
                constrainingVar = tempKey[0]
        trueOrder.append(constrainingVar)
        maxConstraining = -1
    print("trueOrder: ",trueOrder)
    return trueOrder    





        


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
    #Sort dict in descending order:
    sorted_dict = sorted(dict.items(),key=lambda x:x[1],reverse=True)
    #for i in sorted_dict: i[0] = key i[1] = value
    #If all dict values = -1, => FAILURE
    return sorted_dict


############## Backtracking Method ##############
def backtrack(assignment, constraints,variableValues, variableNames):
    if  checkAssignment(assignment, constraints, variableNames):
        return assignment
    constrainedVarList = findMostConstrainedVar(variableValues, constraints)
    for variable in constrainedVarList:
        variableIndex = findVariableIndex(variable, variableNames)
        dict = findLeastConstrainedValue(constraints, variableValues, variable, variableNames)
        for value in dict: # value = variable's value
            tempValue = assignment[variable]
            assignment[variable] = value[0]
            print("BRANCH")
            printAssignment(assignment)
            if checkAssignment(assignment, constraints, variableNames):
                result = backtrack(assignment, constraints, variableValues, variableNames)
                if  not checkFailure(result):
                    return result
                assignment[variable] = tempValue
    return {"A":-1}  # FAILURE
        


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
printAssignment(assignment)

print(findMostConstrainedVar(variableValues,constraints))
print(findLeastConstrainedValue(constraints, variableValues, variableNames[0], variableNames))
print("BackTrack:",backtrack(assignment,constraints,variableValues,variableNames))
