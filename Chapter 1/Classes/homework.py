# Exercise for Classes: Homework Solution

class Car():                                                    # we initialize a class called "Car"
    
    def __init__(self, topSpeed, acc):                          # __init__ method, called when an object of this class is created
                                                                # takes maximum velocity and accelearation as arguments
        self.topSpeed = topSpeed                                # we create a variable called "topSpeed" associated with this class/object by "self"
        self.acceleration = acc                                 # variable "acceleration" also associated with this class/objct by "self"
    
    def calcTime(self, currentSpeed):                           # we create a new method that will calculate the time required for the car to accelerate to top speed 
        t = (self.topSpeed - currentSpeed) / self.acceleration  # we calculate this time using the equation provided in the hint
        return t                                                # this method has to return the calculated time, therefore we write "return"


car = Car(75, 3.5)                                              # we create an object of "Car" class that we call "car", remember that
                                                                # we need to input two arguments: top speed and acceleration
time = car.calcTime(30)                                         # we calculate the time required to accelerate from 30 m/s to 75 m/s using the "calcTime" method
print(time)                                                     # and in the end we can finally display this time
