#Introduction/refresher to Python

#Displaying text
print('Hello world!')

#Creating variables and basic operations
x = 0

x += 1

x -= 1

x /= 2

x *= 2

y = 3
print(x + y)

#if conditions
x = 5
if x > 0:
    print('x is greater than 0')
elif x == 0:
    print('x is equal to 0')
else:
    print('x is lower than 0')

#for and while loops
for i in range(1, 20):
  print(i)
 
stop = False
i = 0
while not stop:
    i += 1
    print(i)
    if i >= 19:
        stop = True
    
#methods
def division(a, b):
    result = a / b
    return result

print(division(5,2))
