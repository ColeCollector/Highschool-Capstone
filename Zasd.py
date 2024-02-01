import numpy as np

square = "Pf3"


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
y = int(square[-1])

for i in range(0,7):
    try:
        if i<3:
            base[y-1+i][x-1] = 3.0
            base[y-1+i][x+1] = 3.0


        if i<5:
            base[y-2][x-2+i] = 2.0
            base[y+2][x-2+i] = 2.0

            base[y-2+i][x-2] = 2.0
            base[y-2+i][x+2] = 2.0

        if i<7:
            base[y-3][x-3+i] = 1.0
            base[y+3][x-3+i] = 1.0
            
            base[y-3+i][x-3] = 1.0
            base[y-3+i][x+3] = 1.0

    except:
        pass
    


base[y][x] = 10.0




for i in base:
    print(i)
