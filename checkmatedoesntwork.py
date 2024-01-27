import time
import heatmap
import copy
import numpy as np

class chess():
    #remember:
    #lowercase = black
    #upercase = white


    xaxis = ['a','b','c','d','e','f','g','h','i']
    yaxis = ['1','2','3','4','5','6','7','8']


    def fen2pos(self,fen):
        positions = []
        #castle = {"K":False,"Q":False,"k":False,"q":False}
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
        


        #for i in fen.split(" ")[2]:
        #    castle[i]=True
            
        return positions

    def pos2fen(self,pos,turn):
        letters = ['a','b','c','d','e','f','g','h','i']
        x = ""
        row = 8
        collumn = -1
        pos.append({" i1":[]})

        for i in pos:
            switch = False
            if int(list(i.keys())[0][2]) != row:
                row-=1

                if collumn!=7:
                    if 0!=letters.index(list(i.keys())[0][1]):
                        x = f"{x}{-collumn+7}"
                    else:
                        switch = True
                        x = f"{x}{-collumn+7}"

                while int(list(i.keys())[0][2]) != row:
                    x = f"{x}/8"
                    row-=1

                if switch == True:
                    x = f"{x}/{list(i.keys())[0][0]}"

                if collumn !=7 and 0!=letters.index(list(i.keys())[0][1]):
                    x = f"{x}/{letters.index(list(i.keys())[0][1])}{list(i.keys())[0][0]}"

                if collumn==7:
                    if 0!=letters.index(list(i.keys())[0][1]):
                        x = f"{x}/{letters.index(list(i.keys())[0][1])}{list(i.keys())[0][0]}"
                    else:
                        x = f"{x}/{list(i.keys())[0][0]}"
                

            else:
                if collumn+1!=letters.index(list(i.keys())[0][1]):
                    x = f"{x}{letters.index(list(i.keys())[0][1])-collumn-1}{list(i.keys())[0][0]}"
                else:
                    x = f"{x}{list(i.keys())[0][0]}"
            
    
            collumn = letters.index(list(i.keys())[0][1])
        

        
        x += f"{self.turn[0]} KQkq - 0 1"
        return x

    def rook(self,square,board1,board2):

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

            if horizontal[0] == True and self.xaxis.index(last[0])+i<8:
                #left
                pos = f"{self.xaxis[self.xaxis.index(last[0])+i]}{last[1]}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    horizontal[0] = False
                else:
                    available.append(f"{first.upper()}{pos}")

            if horizontal[1] == True and self.xaxis.index(last[0])-i>=0:
                #right
                pos = f"{self.xaxis[self.xaxis.index(last[0])-i]}{last[1]}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    horizontal[1] = False
                else:
                    available.append(f"{first.upper()}{pos}")


        available.sort()
        return {square:available}

    def knight(self,square,board1,board2):

        available = []

        currentx = square[1:][0]
        currenty = square[1:][1]
        first = square[:1]
        
        xnum = self.xaxis.index(currentx)
        ynum = self.yaxis.index(currenty)

        for i in range(0,8):
            x = self.xaxis[i]
            differ = abs(xnum - self.xaxis.index(x))

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

    def bishop(self,square,board1,board2):

        available = []
        top = [True,True]
        bottom = [True, True]
        
        xnum = self.xaxis.index(square[1:][0])
        ynum = self.yaxis.index(square[1:][1])

        first = square[:1]

        for i in range(0,8):
            if ynum+2+i<=8 and xnum-i-1>=0 and top[0] == True:
                #top left
                pos = f"{self.xaxis[xnum-i-1]}{ynum+2+i}"
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    top[0] = False

                else:
                    available.append(f"{first.upper()}{pos}")

            if ynum+2+i<=8 and xnum+i+1<8 and top[1] == True:
                pos = f"{self.xaxis[xnum+i+1]}{ynum+2+i}"
                #top right
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    top[1] = False

                else:
                    available.append(f"{first.upper()}{pos}")

            if ynum-i>0 and xnum-i-1>=0 and bottom[0] == True:
                #bottom left
                pos = f"{self.xaxis[xnum-i-1]}{ynum-i}"

                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    bottom[0] = False

                else:
                    available.append(f"{first.upper()}{pos}")
            

            if ynum-i>0 and xnum+i+1<8 and bottom[1] == True:
                #bottom right
                pos = f"{self.xaxis[xnum+i+1]}{ynum-i}"
                if pos in board2:
                    if (board1[board2.index(pos)])[:1].isupper() != first.isupper():
                        available.append(f"{first.upper()}x{pos}")
                    bottom[1] = False

                else:
                    available.append(f"{first.upper()}{pos}")


        available.sort()

        return {square:available}

    def pawn(self,square,board1,board2):
        available = []
    
        xnum = self.xaxis.index(square[1:][0])+1
        ynum = self.yaxis.index(square[1:][1])+1


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
                if f"{square[1]}{ynum+2*x}" not in board2 and ynum==special[0]:
                    available.append(f"{square[1]}{ynum+2*x}")
            else:
                available.append(f"{square[1]}{ynum+1*x}=Q")


        if xnum<8:
            if f"{self.xaxis[xnum]}{ynum+1*x}" in board2:
                
                #pawn takes right
                if (board1[board2.index(f"{self.xaxis[xnum]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                    if ynum+1*x!= special[1]:
                        available.append(f"{square[1]}x{self.xaxis[xnum]}{ynum+1*x}")

                    else:
                        available.append(f"{square[1]}x{self.xaxis[xnum]}{ynum+1*x}=Q")


        if xnum-2>=0:
            if f"{self.xaxis[xnum-2]}{ynum+1*x}" in board2:

                #pawn takes left
                if (board1[board2.index(f"{self.xaxis[xnum-2]}{ynum+1*x}")])[:1].isupper() != square[:1].isupper():
                    if ynum+1*x!=special[1]:
                        available.append(f"{square[1]}x{self.xaxis[xnum-2]}{ynum+1*x}")
                    else:
                        available.append(f"{square[1]}x{self.xaxis[xnum-2]}{ynum+1*x}=Q")



        
        available.sort()
        return {square:available}

    def king(self,square,board1,board2):
        available = []

        xnum = self.xaxis.index(square[1:][0])
        ynum = self.yaxis.index(square[1:][1])

        def check(pos):
            if pos in board2:
                if (board1[board2.index(pos)])[:1].isupper() != square[:1].isupper():
                    available.append(f"Kx{pos}")
            else:
                available.append(f"K{pos}")

        if ynum+1 < 8:
            #up
            
            pos = f"{self.xaxis[xnum]}{self.yaxis[ynum+1]}"
            check(pos)
            if xnum+1 < 8:
                pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum+1]}"
                check(pos)

            if xnum-1 >= 0:  
                pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum+1]}"  
                check(pos)
                
        if ynum-1 >= 0:
            #down
            pos = f"{self.xaxis[xnum]}{self.yaxis[ynum-1]}"
            check(pos)

            if xnum+1 < 8:
                pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum-1]}"
                check(pos)

            if xnum-1 >= 0:  
                pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum-1]}"  
                check(pos)

        if xnum+1 < 8:
            #right
            pos = f"{self.xaxis[xnum+1]}{self.yaxis[ynum]}"
            check(pos)

        if xnum-1 >= 0:  
            #left
            pos = f"{self.xaxis[xnum-1]}{self.yaxis[ynum]}"
            check(pos)

            
        available.sort()
        return {square:available}

    def __init__(self,board):
        movecount = [0,0]
        pgn = []
        self.turn = "white"
        #lastmove = None
        while True:
            if board == ['ka8', 'kf2', 'Kh1', 'Rb1', 'ra7']:
                pass
            #THE PROBLEM IS THAT THE KING HEATMAP IS NOT RESET
            def findmoves(board):
                moves = []
                board2 = []

                #an homage to andrew
                tally = 0

                for i in board:
                    board2.append(i[1:])

                if self.turn == "white":
                    piece = ["B","R","N","Q","P","K"]

                elif self.turn == "black":
                    piece = ["b","r","n","q","p","k"]

                for i in board:

                    if i[:1] == piece[0]:
                        moves.append(self.bishop(board[tally],board,board2))

                    elif i[:1] == piece[1]:
                        moves.append(self.rook(board[tally],board,board2))

                    elif i[:1] == piece[2]:
                        moves.append(self.knight(board[tally],board,board2))
                    
                    elif i[:1] == piece[3]:
                        queen = self.bishop(board[tally],board,board2)[i]+self.rook(board[tally],board,board2)[i]
                        queen.sort()
                        moves.append({i:queen})

                    elif i[:1] == piece[4]:
                        moves.append(self.pawn(board[tally],board,board2)) 

                    elif i[:1] == piece[5]:
                        moves.append(self.king(board[tally],board,board2))

                    else:
                        moves.append({board[tally]:[]})

                    tally+=1
                return moves

            def removedupes(moves):
                allmoves = []
                dupes = []

                for j in moves:
                    if list(j.keys())[0][0].isupper() == switch:
                        for k in (list(j.values())[0]):
                            if k in allmoves:
                                dupes.append(k)
                            else:
                                allmoves.append(k)

                allmoves = []

                for j in moves:
                    if list(j.keys())[0][0].isupper() == switch:
                        for k in (list(j.values())[0]):
                            if k in dupes:
                                list(j.values())[0][list(j.values())[0].index(k)] = f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}"
                                allmoves.append(f"{k[:1]}{list(j.keys())[0][1]}{k[1:]}")
                            else:
                                allmoves.append(k)
                
                return allmoves

            def end(square,eheatmap):
                x = int(self.xaxis.index(square[-2]))
                y = 8 - int(square[-1])

                for row in range(0,8):
                    for collumn in range(0,8):
                        differ1 = abs(x-row)
                        differ2 = abs(y-collumn)

                        if differ1>differ2:
                            eheatmap[collumn][row] += 500-50*differ1

                        else:
                            eheatmap[collumn][row] += 500-50*differ2

                return eheatmap
            
            def evaluate(moves):

                evaluation = 0
                endgame = 0
                eheatmap = [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]]

                for i in moves:
                    if list(i.keys())[0][0]!="P" and list(i.keys())[0][0]!="p":
                        endgame+=1
                    
                    else:
                        eheatmap = end(list(i.keys())[0],eheatmap)
                
                if endgame<=4:
                    heatmap.map_points[5] = eheatmap
                

                    
                
                for i in moves:
                    
                    temp = list(i.keys())[0] 
                    heatm = heatmap.PieceMap(temp)
                    heat = heatm[0]
                    

                    if temp[0].isupper() == True:
                        evaluation += heatm[1]*10
                        evaluation += heat[8-int(temp[-1])][int(self.xaxis.index(temp[-2]))]

                    else:
                        evaluation -= heatm[1]*10

                        if heatmap.map_points[5] == eheatmap:
                            evaluation -= heat[8-int(temp[-1])][int(self.xaxis.index(temp[-2]))]
                        else:
                            evaluation -= heat[int(temp[-1])-1][7-int(self.xaxis.index(temp[-2]))]  
                    
                
                return evaluation
            
            def modify(moves,move):
                take = None
                for i in moves:
                    if move in list(i.values())[0]:
                        if list(i.keys())[0][0].isupper() == switch:
                            #if pawn promotion spawn a queen and get rid of pawn
                            if "=" in move:
                                if list(i.keys())[0][0].isupper():
                                    move = "Q" + move[-4] + move[-3]
                                else:
                                    move = "q" + move[-4] + move[-3]   
                            else:
                                move = list(i.keys())[0][0]+move[-2]+move[-1]
                            
                            original = i
                    

                    if list(i.keys())[0][1:] == move[-2]+move[-1]:
                        take = i

                #if pawn moves 50 move rule resets
                if take != None:
                    moves.remove(take)

                moves.remove(original)
                moves.append({move:""})
                return moves

            def depth(moves):
                depthboard = []

                for i in moves:
                    depthboard.append(list(i.keys())[0])
                
                #looking at the position from black's perspecifive
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"

                newboard = findmoves(depthboard)
                
                if self.turn == "black":
                    self.turn = "white"
                else:
                    self.turn = "black"

                return newboard

            def gameloop(mooves):
                if mooves == [{'ra3': []}, {'kf2': []}, {'Rg1': ['Ra1', 'Rb1', 'Rc1', 'Rd1', 'Re1', 'Rf1', 'Rg2', 'Rg3', 'Rg4', 'Rg5', 'Rg6', 'Rg7', 'Rg8']}, {'Kh2': ''}]:
                    pass
                king = [False,False]
                for i in mooves:
                    if list(i.keys())[0][0] == "K":
                        king[0] = True

                    elif list(i.keys())[0][0] == "k":
                        king[1] = True


                if king[1] == False:
                    return 999999

                if king[0] == False:
                    return -999999
                
                return None
                
            if self.turn == "white":
                switch = True
            else:
                switch = False

            layer0 = []
            layer1 = []
            layer2 = []
            layer3 = []
            layer4 = []
            depth1 = []
            depth2 = []
            depth3 = []
            alld1moves = []

            rid1 = []
            rid2 = []
            rid3 = []

            moves = findmoves(board)
            allmoves = removedupes(moves)
            movecopy = copy.copy(moves)
            
            for move in allmoves:
                moves = copy.copy(movecopy)
                moves = modify(moves,move)
                x = gameloop(moves)
                if x == None:
                    depth1.append(depth(moves))
                else:
                    rid1.append([x, allmoves.index(move)])


            #switching colors
            if self.turn == "white":
                self.turn = "black"
                switch = False
            else:
                self.turn = "white"
                switch = True


            for d1moves in depth1:
                
                d1allmoves = removedupes(d1moves)
                alld1moves.append(d1allmoves)
                d1movecopy = copy.copy(d1moves)


                for move in d1allmoves:

                    #print(allmoves[depth1.index(d1movecopy)],move)

                    d1moves = copy.copy(d1movecopy)
                    d1moves = modify(d1moves,move)
                    #print(move)
                    if move == "Kxa2":
                        print("1293712093")

                    x = gameloop(d1moves)
                    if x == None:
                        depth2.append(depth(d1moves))
                    else:
                        #print(allmoves[depth1.index(d1movecopy)],move)
                        rid2.append([x,depth1.index(d1movecopy)])

                depth2.append(None)


            #switching colors
            if self.turn == "white":
                self.turn = "black"
                switch = False
            else:
                self.turn = "white"
                switch = True

            for d2moves in depth2:
                if d2moves == None:
                    depth3.append(None)
                else:
                    d2allmoves = removedupes(d2moves)
                    d2movecopy = copy.copy(d2moves)
                    for move in d2allmoves:
                        d2moves = copy.copy(d2movecopy)
                        d2moves = modify(d2moves,move)
                        x = gameloop(d2moves)
                        if x == None:
                            depth3.append(depth(d2moves))
                        else:
                            #print(d1allmoves[depth2.index(d2movecopy)],move)
                            rid3.append([x,depth2.index(d2movecopy)])
                        #print(depth2.index(d2movecopy))

                    depth3.append(None)

            #exit()


            #switching colors
            if self.turn == "white":
                self.turn = "black"
                switch = False

            else:
                self.turn = "white"
                switch = True

            
            track = 0
            alpha = []
            for d3moves in depth3:
                if d3moves == None:
                    layer2.append(layer1)
                    layer1 = []
                    track+=1
                else:
                    d3allmoves = removedupes(d3moves)
                    d3movecopy = copy.copy(d3moves)
                    
                    for move in d3allmoves:
                        d3moves = copy.copy(d3movecopy)
                        d3moves = modify(d3moves,move)

                        if move == d3allmoves[0]:
                            alpha.append(evaluate(d3moves))
                            layer0.append(alpha[-1])

                        if not alpha[-1]>=max(alpha):
                            layer0.append(evaluate(d3moves))

                    if self.turn == "white":
                        layer1.append(max(layer0))
                        
                    else:
                        layer1.append(min(layer0))
                    

                    #print(track)
                    for i in rid3:
                        if i[1] == track:
                            #print(move,i[0])
                            layer1.append(i[0])

                    layer0 = []
            
            track = 0
            for i in layer2:
                if i!= []:
                    if self.turn == "white":
                        layer3.append(min(i))
                    else:
                        layer3.append(max(i))

                    for i in rid2:
                        if i[1] == track:
                            layer3.append(i[0])
                else:
                    if self.turn == "white":
                        layer4.append(max(layer3))
                    else:
                        layer4.append(min(layer3))
                    layer3 = []
                    track+=1

            #print(rid1)
            #print(rid2)
            #print(rid3)


            p = 0
            #print("\n")


            for i in allmoves:
                if len(rid1)>0:
                    if allmoves.index(i) == rid1[0][1]:
                        if allmoves.index(i) == len(layer4):
                            layer4.append(rid1[0][0])
                        else:
                            layer4[allmoves.index(i)] = rid1[0][0]
                        p = -1
                print(i,layer4[allmoves.index(i)+p])



            if self.turn == "white":
                pgn.append(allmoves[layer4.index(min(layer4))])
                switch = False
                move = allmoves[layer4.index(min(layer4))]
                
            else:
                pgn.append(allmoves[layer4.index(max(layer4))])
                switch = True
                move = allmoves[layer4.index(max(layer4))]


            moves = copy.copy(movecopy)
            moves = modify(moves,move)


            movecount[1] +=1
            movecount[0] +=1

            king = [False,False]


            for i in moves:
                if list(i.keys())[0][0] == "K":
                    king[0] = True

                elif list(i.keys())[0][0] == "k":
                    king[1] = True


            if king[1] == False:
                print("White \033[1;32;40mwon!\033[0m")
                break

            elif king[0] == False:
                print("Black \033[1;32;40mwon!\033[0m")
                break 
            
            #After 100 half moves the game ends by draw
            if movecount[1] == 1:
                print("\033[1;30;40mDraw\033[0m  by 50 move rule")
                break
            
            board = []

            for i in range(len(moves)):
                board.append(list(moves[i].keys())[0])

        for i in range(len(pgn)):
            if i%2==0:
                print(f"{int((i+2)/2)}. {pgn[i]}",end=" ")
            else:
                print(pgn[i],end=" ")

        print("\n\n")
        
#Positions I used to test for bugs
#board = self.fen2pos("r1B1k2r/ppPp1p1n/n3p1p1/6Q1/qPq5/N1B5/1P2PPPP/R3K2R w KQkq - 0 1")
#board = self.fen2pos("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board = self.fen2pos("k7/8/8/8/3B4/8/8/7K w - - 0 1")
#board = self.fen2pos("r3k2r/pQpp1p1n/n1P1p1pN/8/qP3B2/N1B1b3/1PK1PPPP/R6R w HAkq - 0 1")
#board = self.fen2pos("2q5/4q3/8/1p2R1q1/q1R5/8/2q1p3/k6K w - - 0 1")
#board = self.fen2pos ("rnbqkbnr/pppp1ppp/8/8/4pP2/6PP/PPPPP3/RNBQKBNR b KQkq f3 0 3")
#board = self.fen2pos("7k/5Q2/4q3/4K3/8/8/8/8 w - - 0 1")


start = time.time()
for i in range(1):
    board = chess.fen2pos(None,"8/8/8/8/8/r7/5k2/6RK - 0 1")
    chess(board)

print(f"\n\nProgram ran for {round((time.time()-start),3)} seconds\n")