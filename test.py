import numpy as np

square = "Ph2"

base = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]
]

xaxis = ['a','b','c','d','e','f','g','h','i']
x = int(xaxis.index(square[-2]))
y = 8 - int(square[-1])

for row in range(0,8):
    for collumn in range(0,8):
        base[collumn][row]-=collumn

        differ1 = abs(x-row)
        differ2 = abs(y-collumn)

        if differ1>differ2:
            base[collumn][row] += 3-0.5*differ1

        else:
            base[collumn][row] += 3-0.5*differ2


for i in base:
    print(i)
