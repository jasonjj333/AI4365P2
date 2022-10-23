with open('ex1.con') as f:
    constraints = f.readlines()
print(constraints)


with open('ex1.var') as p:
   for line in p:
    for word in line.split(" "):
        values.add(word)