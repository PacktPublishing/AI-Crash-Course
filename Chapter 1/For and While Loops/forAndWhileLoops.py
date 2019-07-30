# Introduction to For and While Loops

for i in range(1, 20):
    print(i)

L3 = [3,4,1,6,7,5]
for element in L3:
    print(element)

stop = False
i = 0
while stop == False:  # alternatively it can be "while not stop:"
    i += 1
    print(i)
    if i >= 19:
        stop = True

L4 = [[2, 9, -5], [-1, 0, 4], [3, 1, 2]]
for row in L4:
    for element in row:
        print(element)
