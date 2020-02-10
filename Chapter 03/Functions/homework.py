# Exercise for Functions: Homework Solution

def distance(x1, y1, x2, y2):                       # we create a new function "distance" that takes coordinates of both points as arguments
    d = pow(pow(x1 - x2, 2) + pow(y1 - y2, 2), 0.5) # we calculate the distance between two points using the formula provided in the hint ("pow" function is power)
    return d                                        # this line means that our function will return the distance we calculated before

dist = distance(0, 0, 3, 4)                         # we call our function while inputting 4 required arguments, that are coordinates
print(dist)                                         # we display the calculated distance
