#remember lowercase = black
#         upercase = white


import time
start = time.time()

xaxis = ['a','b','c','d','e','f','g','h']
yaxis = ['1','2','3','4','5','6','7','8']



def fen2pos(fen):
    print(fen)
    positions = []
    castle = {"K":False,"Q":False,"k":False,"q":False}
    number = 8
    column = 1
    letters = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}


    for i in range(64):
        try:
            column+=int(fen[i]) 
        except:
            if fen[i] == " ":
                break
            elif fen[i] == "/":
                number-=1
                column = 1
            else: 
                positions.append(f"{fen[i]}{letters[column]}{number}")
                column +=1
    


    for i in fen.split(" ")[2]:
        castle[i]=True
        
    return positions,castle,fen.split(" ")[3]


def pos2fen(pos):
    letters = ['a','b','c','d','e','f','g','h','i']
    x = ""
    row = 8
    collumn = -1
    pos.append({" i1":"1"})
    for i in pos:
        if int(list(i.keys())[0][2]) != row:
            row-=1

            if collumn!=7:
                if 0!=letters.index(list(i.keys())[0][1]):
                    x = f"{x}{-collumn+7}"
                else:
                    x = f"{x}{-collumn+7}/{list(i.keys())[0][0]}"

            while int(list(i.keys())[0][2]) != row:
                x = f"{x}/8"
                row-=1

            if collumn !=7 and 0!=letters.index(list(i.keys())[0][1]):
                x = f"{x}/{letters.index(list(i.keys())[0][1])}{list(i.keys())[0][0]}"
                
            if collumn==7:
                x = f"{x}/{list(i.keys())[0][0]}"
            

        else:
            if collumn+1!=letters.index(list(i.keys())[0][1]):
                x = f"{x}{letters.index(list(i.keys())[0][1])-collumn-1}{list(i.keys())[0][0]}"
            else:
                x = f"{x}{list(i.keys())[0][0]}"
        


        collumn = letters.index(list(i.keys())[0][1])
    
  
    x += "w KQkq - 0 1"
    return x


def rook(square,board1,board2):
  global xaxis

  first = square[:1]
  last = square[1:]
 
  available = []
  vertical = [True,True]
  horizontal = [True,True]


  for i in range(1,8):

    if vertical[0] == True and int(last[1])+i<=8:
        #up
        pos = f"{last[0]}{int(last[1])+i}"
        
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            vertical[0] = False
        else:
            available.append(f"{first.upper()}{pos}")
    
    if vertical[1] == True and int(last[1])-i>0:
        #down
        pos = f"{last[0]}{int(last[1])-i}"
        
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            vertical[1] = False
        else:
            available.append(f"{first.upper()}{pos}")

    if horizontal[0] == True and xaxis.index(last[0])+i<8:
        #left
        pos = f"{xaxis[xaxis.index(last[0])+i]}{last[1]}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            horizontal[0] = False
        else:
            available.append(f"{first.upper()}{pos}")

    if horizontal[1] == True and xaxis.index(last[0])-i>=0:
        #right
        pos = f"{xaxis[xaxis.index(last[0])-i]}{last[1]}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            horizontal[1] = False
        else:
            available.append(f"{first.upper()}{pos}")


  available.sort()

  return {square:available}

def knight(square,board1,board2):
  global xaxis,yaxis

  available = []

  currentx = square[1:][0]
  currenty = square[1:][1]
  first = square[:1]
  
  xnum = xaxis.index(currentx)
  ynum = yaxis.index(currenty)

  for i in range(0,8):
    x = xaxis[i]
    differ = abs(xnum - xaxis.index(x))

    if differ == 2:

      if ynum + 2 < 9:
        pos = f"{x}{ynum + 2}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                    available.append(f"Nx{pos}")

        else:
            available.append(f"N{pos}")

      if ynum > 0: 
        pos = f"{x}{ynum}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                    available.append(f"Nx{pos}")

        else:
            available.append(f"N{pos}")

    if differ == 1:
      if ynum + 3 < 9:
        pos = f"{x}{ynum + 3}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                    available.append(f"Nx{pos}")

        else:
            available.append(f"N{pos}")

      if ynum - 1 > 0:
        pos = f"{x}{ynum - 1}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                    available.append(f"Nx{pos}")
        else:
            available.append(f"N{pos}")

  if str(square) in available:
    available.remove(str(square))
  
  available.sort()

  return {square:available}

def bishop(square,board1,board2):
  global xaxis,yaxis

  available = []
  top = [True,True]
  bottom = [True, True]
  
  xnum = xaxis.index(square[1:][0])
  ynum = yaxis.index(square[1:][1])

  first = square[:1]

  for i in range(0,8):


    if ynum+2+i<=8 and xnum-i-1>=0 and top[0] == True:
        #top left
        pos = f"{xaxis[xnum-i-1]}{ynum+2+i}"
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            top[0] = False

        else:
            available.append(f"{first.upper()}{pos}")

    if ynum+2+i<=8 and xnum+i+1<8 and top[1] == True:
        pos = f"{xaxis[xnum+i+1]}{ynum+2+i}"
        #top right
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            top[1] = False

        else:
            available.append(f"{first.upper()}{pos}")

    if ynum-i>0 and xnum-i-1>=0 and bottom[0] == True:
        #bottom left
        pos = f"{xaxis[xnum-i-1]}{ynum-i}"

        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            bottom[0] = False

        else:
            available.append(f"{first.upper()}{pos}")
    

    if ynum-i>0 and xnum+i+1<8 and bottom[1] == True:
        #bottom right
        pos = f"{xaxis[xnum+i+1]}{ynum-i}"
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                available.append(f"{first.upper()}x{pos}")
            bottom[1] = False

        else:
            available.append(f"{first.upper()}{pos}")


  available.sort()

  return {square:available}

def pawn(square,board1,board2,enpassent):
    global xaxis, yaxis
    available = []
 
    xnum = xaxis.index(square[1:][0])+1
    ynum = yaxis.index(square[1:][1])+1


    #making pawns go different directions based on color
    if square[0] == "P":
        x = 1
        special = [2,8,5]
        
    else:
        x= -1
        special = [7,1,4]

    if f"{square[1]}{ynum+1*x}" not in board2:
        if ynum+1*x!=special[1]:
            available.append(f"{square[1]}{ynum+1*x}")

            #double pawn move
            if f"{square[1]}{ynum+2}" not in board2 and ynum==special[0]:
                available.append(f"{square[1]}{ynum+2*x}")
        else:
            available.append(f"{square[1]}{ynum+1*x}=Q")


    if xnum<8:
        if f"{xaxis[xnum]}{ynum+1*x}" in board2:
            
            #pawn takes right
            if (board1[board2.index(f"{xaxis[xnum]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                if ynum+1*x!= special[1]:
                    available.append(f"{square[1]}x{xaxis[xnum]}{ynum+1*x}")

                else:
                    available.append(f"{square[1]}x{xaxis[xnum]}{ynum+1*x}=Q")


    if xnum-2>=0:
        if f"{xaxis[xnum-2]}{ynum+1*x}" in board2:

            #pawn takes left
            if (board1[board2.index(f"{xaxis[xnum-2]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                if ynum+1*x!=special[1]:
                    available.append(f"{square[1]}x{xaxis[xnum-2]}{ynum+1*x}")
                else:
                    available.append(f"{square[1]}x{xaxis[xnum-2]}{ynum+1*x}=Q")

    
    if xnum<8:
        if f"{xaxis[xnum]}{ynum+1*x}" == enpassent and ynum == special[2]:
            available.append(f"{xaxis[xnum-1]}x{enpassent}")


    
    available.sort()
    return {square:available}

def king(square,board1,board2,castle):
    global xaxis, yaxis
    available = []

    xnum = xaxis.index(square[1:][0])
    ynum = yaxis.index(square[1:][1])

    def check(pos):
        if pos in board2:
            if (board1[board2.index(pos)])[:1].isupper() != square[:1].isupper():
                available.append(f"Kx{pos}")
        else:
            available.append(f"K{pos}")

    if ynum+1 < 8:
        #up
        
        pos = f"{xaxis[xnum]}{yaxis[ynum+1]}"
        check(pos)
        if xnum+1 < 8:
            pos = f"{xaxis[xnum+1]}{yaxis[ynum+1]}"
            check(pos)

        if xnum-1 > 0:  
            pos = f"{xaxis[xnum-1]}{yaxis[ynum+1]}"  
            check(pos)
            
    if ynum-1 > 0:
        #down
        pos = f"{xaxis[xnum]}{yaxis[ynum-1]}"
        check(pos)

        if xnum+1 < 8:
            pos = f"{xaxis[xnum+1]}{yaxis[ynum-1]}"
            check(pos)

        if xnum-1 > 0:  
            pos = f"{xaxis[xnum-1]}{yaxis[ynum-1]}"  
            check(pos)

    if xnum+1 < 8:
        #right
        pos = f"{xaxis[xnum+1]}{yaxis[ynum]}"
        check(pos)

    if xnum-1 > 0:  
        #left
        pos = f"{xaxis[xnum-1]}{yaxis[ynum]}"
        check(pos)




    available.sort()
    return {square:available}




#board = fen2pos("r1B1k2r/ppPp1p1n/n3p1p1/6Q1/qPq5/N1B5/1P2PPPP/R3K2R w KQkq - 0 1")
#board = fen2pos("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board = fen2pos("k7/8/8/8/3B4/8/8/7K w - - 0 1")
#board = fen2pos("r3k2r/pQpp1p1n/n1P1p1pN/8/qP3B2/N1B1b3/1PK1PPPP/R6R w HAkq - 0 1")
board = fen2pos ("8/B6B/B6B/B6B/B6B/B6B/B6B/B7 w - - 0 1")
#board = fen2pos("2q5/4q3/8/1p2R1q1/q1R5/8/2q1p3/k6K w - - 0 1")
#board = fen2pos ("rnbqkbnr/pppp1ppp/8/8/4pP2/6PP/PPPPP3/RNBQKBNR b KQkq f3 0 3")
#board = fen2pos("7k/5Q2/4q3/4K3/8/8/8/8 w - - 0 1")




moves = []
board2 = []


#an homage to andrew
tally = 0


for i in board[0]:
    #interestingly we have to act like kings don't exist 
    #because otherwise the king will want to stay in danger
    board2.append(i[1:])


for i in board[0]:
    if i[:1] == "B" or i[:1] == "b":
        moves.append(bishop(board[0][tally],board[0],board2))

    elif i[:1] == "R" or i[:1] == "r":
        moves.append(rook(board[0][tally],board[0],board2))

    elif i[:1] == "N" or i[:1] == "n":
        moves.append(knight(board[0][tally],board[0],board2))
    
    elif i[:1] == "Q" or i[:1] == "q":
        queen = bishop(board[0][tally],board[0],board2)[i]+rook(board[0][tally],board[0],board2)[i]
        queen.sort()
        moves.append({i:queen})

    elif i[:1] == "P" or i[:1] == "p":
        moves.append(pawn(board[0][tally],board[0],board2,None)) 

    elif i[:1] == "K" or i[:1] == "k":
        moves.append(king(board[0][tally],board[0],board2,board[2]))

    tally+=1
    
allmoves = []
wdupes = []
bdupes = []

for j in moves:
    if list(j.keys())[0][0].isupper():
        for k in (list(j.values())[0]):
            if k in allmoves:
                wdupes.append(k)
            else:
                allmoves.append(k)

allmoves = []


for j in moves:
    if list(j.keys())[0][0].isupper() == False:
        for k in (list(j.values())[0]):
            if k in allmoves:
                bdupes.append(k)
            else:
                allmoves.append(k)


for j in moves:
    if list(j.keys())[0][0].isupper() == False:
        for k in (list(j.values())[0]):
            if k in bdupes:
                list(j.values())[0][list(j.values())[0].index(k)] = f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}"


    else:
        for k in (list(j.values())[0]):
            if k in wdupes:
                list(j.values())[0][list(j.values())[0].index(k)] = f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}"

allmoves = []

for i in moves:
    allmoves.append(list(i.keys())[0])
print(allmoves)

move = input(">")

while move not in allmoves:
    move = input(">")


print(pos2fen(moves))

print(f"Program ran for {round((time.time()-start),4)} seconds\n")
