#remember lowercase = black
#         upercase = white


import time
start = time.time()

xaxis = ['a','b','c','d','e','f','g','h']
yaxis = ['1','2','3','4','5','6','7','8']



def fen2pos(fen):
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

def pawn(square,board1,board2):
    global xaxis, yaxis
    available = []
 
    xnum = xaxis.index(square[1:][0])
    ynum = yaxis.index(square[1:][1])


    if f"{square[1]}{ynum+2}" not in board2:
        if ynum+2!=8:
            available.append(f"{square[1]}{ynum+2}")
            if f"{square[1]}{ynum+3}" not in board2 and ynum==1:
                available.append(f"{square[1]}{ynum+3}")
        else:
            available.append(f"{square[1]}{ynum+2}=Q")
            available.append(f"{square[1]}{ynum+2}=R")
            available.append(f"{square[1]}{ynum+2}=B")
            available.append(f"{square[1]}{ynum+2}=N")


    if f"{xaxis[xnum+1]}{ynum+2}" in board2:
        if (board1[board2.index(f"{xaxis[xnum+1]}{ynum+2}")])[:1].isupper() != square[:1].isupper():
            #pawn takes right
            if ynum+2!=8:
                available.append(f"{square[1]}x{xaxis[xnum+1]}{ynum+2}")
            else:
                available.append(f"{square[1]}x{xaxis[xnum+1]}{ynum+2}=Q")
                available.append(f"{square[1]}x{xaxis[xnum+1]}{ynum+2}=R")
                available.append(f"{square[1]}x{xaxis[xnum+1]}{ynum+2}=B")
                available.append(f"{square[1]}x{xaxis[xnum+1]}{ynum+2}=N")
    
    if f"{xaxis[xnum-1]}{ynum+2}" in board2 and xnum>0:
        #pawn takes left
        if (board1[board2.index(f"{xaxis[xnum-1]}{ynum+2}")])[:1].isupper() != square[:1].isupper():
            if ynum+2!=8:
                available.append(f"{square[1]}x{xaxis[xnum-1]}{ynum+2}")
            else:
                available.append(f"{square[1]}x{xaxis[xnum-1]}{ynum+2}=Q")
                available.append(f"{square[1]}x{xaxis[xnum-1]}{ynum+2}=R")
                available.append(f"{square[1]}x{xaxis[xnum-1]}{ynum+2}=B")
                available.append(f"{square[1]}x{xaxis[xnum-1]}{ynum+2}=N")

    
    available.sort()
    return {square:available}


#board = fen2pos("r1B1k2r/ppPp1p1n/n3p1p1/6Q1/qPq5/N1B5/1P2PPPP/R3K2R w KQkq - 0 1")
#board = fen2pos("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board = fen2pos("k7/8/8/8/3B4/8/8/7K w - - 0 1")
#board = fen2pos("r3k2r/pQpp1p1n/n1P1p1pN/8/qP3B2/N1B1b3/1PK1PPPP/R6R w HAkq - 0 1")
#board = fen2pos ("8/B6B/B6B/B6B/B6B/B6B/B6B/B7 w - - 0 1")
#board = fen2pos("2q5/4q3/8/1p2R1q1/q1R5/8/2q1p3/k6K w - - 0 1")
#board = fen2pos ("rnbqkbnr/pppp1ppp/8/8/4pP2/6PP/PPPPP3/RNBQKBNR b KQkq f3 0 3")
board = fen2pos("n1n4k/1P1PP3/8/1P1P4/1pPp4/2P1n3/P4PP1/K7 w - - 0 1")



moves = []
board2 = []

#an homage to andrew
tally = 0


for i in board[0]:
    board2.append(i[1:])


for i in board[0]:
    if i[:1] == "B" or i[:1] == "b":
        print(bishop(board[0][tally],board[0],board2))

    elif i[:1] == "R" or i[:1] == "r":
        print(rook(board[0][tally],board[0],board2))
    
    elif i[:1] == "N" or i[:1] == "n":
        print(knight(board[0][tally],board[0],board2))

    elif i[:1] == "Q" or i[:1] == "q":
        queen = bishop(board[0][tally],board[0],board2)[i]+rook(board[0][tally],board[0],board2)[i]
        queen.sort()
        print({i:queen})

    elif i[:1] == "P":
        print(pawn(board[0][tally],board[0],board2)) 

    elif i[:1] == "K":
        pass

    tally=tally+1



print(f"Program ran for {time.time()-start} seconds\n")