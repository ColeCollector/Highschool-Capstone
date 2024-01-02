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
side=1
num=10
var=1

for side in range(0,10):
    try:
        for i in range((side*2)+1):
            #left
            if y+i-side>-1 and x-1-side>-1:
                base[y+i-side][x-1-side]+=8-2*side

            #right
            if y+i-side>-1 and x+1+side>-1:
                base[y+i-side][x+1+side]+=8-2*side
            
            #down
            if y+1+side<8 and x+i-side>-1:
                base[y+1+side][x+i-side]+=8-2*side

            #up
            if y-1-side<8 and x+i-side>-1:
                base[y-1-side][x+i-side]+=8-2*side


        #top left
        if y-side>-1 and x-side>-1:
            base[y-side][x-side] += 10-2*side
            

        #top right
        if y-side>-1 and x+side<8:
            base[y-side][x+side] += 10-2*side
        

        #bottom left
        if y+side<8 and x-side>-1:
            base[y+side][x-side] += 10-2*side
        

        #bottom right
        if y+side<8 and x+side<8:
            base[y+side][x+side] += 10-2*side

        
        
    except:
        pass


    


base[y][x] = 12





for i in base:
    print(i)
