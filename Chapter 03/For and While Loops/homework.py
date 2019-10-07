# Exercise for For and While Loops: Homework Solution

n = 5                       # the number factorial of which we are searching for

# for loop approach
factorial = 1               # this will be out factorial, we give it value 1
for i in range(1, n + 1):   # we iterate through every positive integer lower or equal to n, remember, upper bounds are excluded in Python
    factorial *= i          # we multiply factorial by i, this is why we initialized factorial to 1, if we set it to 0, then the product would be equal to 0
print(factorial)            # we display the product, factorial

# while loop approach
factorial = 1               # this will be out factorial, we give it value 1
i = 1                       # we create a variable i, which as previously, will count the number of iterations
while i <= n:               # initializing "while" loop, that will work as long as i is less or equal to n
    factorial *= i          # once again, we multiply our factorial by i, also the reason why factorial and i were set to 1 not 0
    i += 1                  # we increase i by one so that our loop will finally end
print(factorial)            # we display the factorial
