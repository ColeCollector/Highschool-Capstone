import pygame
import _analyze
import copy 
import playsound
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
holding = False
bonded = None
turn = "white"
switch = True
compmove = None
king = [True,True]

#program needs to be given board and moves
board = ['ra8', 'nb8', 'bc8', 'qd8', 'ke8', 'bf8', 'ng8', 'rh8', 'pa7', 'pb7', 'pc7', 'pd7', 'pe7', 'pf7', 'pg7', 'ph7', 'Pa2', 'Pb2', 'Pc2', 'Pd2', 'Pe2', 'Pf2', 'Pg2', 'Ph2', 'Ra1', 'Nb1', 'Bc1', 'Qd1', 'Ke1', 
'Bf1', 'Ng1', 'Rh1']
moves = [{'ra8': []}, {'nb8': []}, {'bc8': []}, {'qd8': []}, {'ke8': []}, {'bf8': []}, {'ng8': []}, {'rh8': []}, {'pa7': []}, {'pb7': []}, {'pc7': []}, {'pd7': []}, {'pe7': []}, {'pf7': []}, {'pg7': []}, {'ph7': 
[]}, {'Pa2': ['a3', 'a4']}, {'Pb2': ['b3', 'b4']}, {'Pc2': ['c3', 'c4']}, {'Pd2': ['d3', 'd4']}, {'Pe2': ['e3', 'e4']}, {'Pf2': ['f3', 'f4']}, {'Pg2': ['g3', 'g4']}, {'Ph2': ['h3', 'h4']}, {'Ra1': []}, {'Nb1': ['Na3', 'Nc3']}, {'Bc1': []}, {'Qd1': []}, {'Ke1': []}, {'Bf1': []}, {'Ng1': ['Nf3', 'Nh3']}, {'Rh1': []}]

allmoves = []

for i in moves:
    vals = list(i.values())[0]
    if vals!=[]:
        for j in vals:
            allmoves.append(j)

xaxis = ['a','b','c','d','e','f','g','h']
images = {"K":"Wking", "Q":"Wqueen","R":"Wrook","B":"Wbishop","N":"Wknight","P":"Wpawn","k":"Bking","q":"Bqueen","r":"Brook","b":"Bbishop","n":"Bknight","p":"Bpawn"}
pieces = []
pos = []
ogpos = []
movepos = []
things = []
thing2 = []
pgn = []
movemade = False
movecount = 0



#intially render the board
for j in range(0,8):
    for i in range(0,8):
        for piece in board:
            if xaxis.index(piece[1]) == i and 8-int(piece[2]) == j: 
                pieces.append(pygame.image.load(f"{images[piece[0]]}.png"))
                things.append(piece)
                pos.append(pygame.Vector2(37.5+340+75*i, 37.5+60+75*j))
                ogpos.append([37.5+340+75*i, 37.5+60+75*j])

        for move in allmoves:
            if xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:
                movepos.append([37.5+340+75*i, 37.5+60+75*j])
                thing2.append(move)


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

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
            things.pop(moves.index(take))
            ogpos.pop(moves.index(take))
            pos.pop(moves.index(take))
            pieces.pop(moves.index(take))

    if take != None:
        moves.remove(take)

    moves.remove(original)
    moves.append({move:""})
    board = []
    for i in range(len(moves)):
        board.append(list(moves[i].keys())[0])
    return [moves,board,take]

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

    
    if dupes !=[]:
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

def savegame(pgn):
    if pgn!=[]:
        file = open("!book.txt","a")

        #printing the pgn and writing it in "book.txt"
        for i in range(len(pgn)):
            if i%2==0:
                file.write(f"{int((i+2)/2)}. {pgn[i]} ")
                print(f"{int((i+2)/2)}. {pgn[i]}",end=" ")
            else:
                file.write(f"{pgn[i]} ")
                print(pgn[i],end=" ")

        file.write(f"\n")
        print("\n\n")

        
        file.close()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            savegame(pgn)
            running = False


        #if you are holding left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            holding = True


        #if you let go of left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            holding = False
            if bonded!= None:
                for i in movepos:
                    for j in list_duplicates_of(movepos,i):
                        if thing2[j] in list(moves[bonded].values())[0]:
                            #if you were clicking on a piece
                            if (pos[bonded].x > i[0]-50 and pos[bonded].x < i[0]+50) and (pos[bonded].y > i[1]-50 and pos[bonded].y <i[1]+50):

                                #play moving sound
                                if "x" not in thing2[j]:
                                    playsound.playsound("move.mp3",block=False)

                                #play different sound for capture
                                else:
                                    playsound.playsound("takes.mp3",block=False)

                                pos[bonded].x = i[0]
                                pos[bonded].y = i[1]

                                #print("Your move:",thing2[j])
                                pgn.append(thing2[j])
                                
                                allmoves = removedupes(moves)
                                modified = modify(moves,thing2[j])
                                moves = modified[0]
                                board = modified[1]
                                
                                screen.fill("white")

                                #drawing everything again so that the piece we just moved 
                                #is centered on the square it moved to

                                for j in range(0,8):
                                    for i in range(0,8):
                                        
                                        #alternating white and purple
                                        if i%2 == 0:
                                            if j%2==0:
                                                color = "white"
                                            else:
                                                color = "#D684FF"
                                        else:
                                            if j%2==0:
                                                color = "#D684FF"
                                            else:
                                                color = "white"
                                        pygame.draw.rect(screen,color,pygame.Rect(340+75*i, 60+75*j, 75, 75))

                                for i in range(0,len(pieces)):
                                    pieces[i].convert()
                                    pieces1 = pieces[i].get_rect()
                                    pieces1.center = (pos[i].x,pos[i].y)
                                    screen.blit(pieces[i],pieces1)
                                
                                pygame.display.flip()
                                king = [False,False]

                                for i in moves:
                                    if list(i.keys())[0][0] == "K":
                                        king[0] = True

                                    elif list(i.keys())[0][0] == "k":
                                        king[1] = True
                                
                                #if no black king
                                if king[1] == False:
                                    font = pygame.font.Font('freesansbold.ttf', 50)
                                    text = font.render("You Won", True, 'purple')
                                    textRect = text.get_rect()
                                    textRect.center = (1280 // 2, 720 // 2)
                                    screen.blit(text, textRect)

                                    pygame.display.flip()
                                    playsound.playsound("mate.mp3")
                                    time.sleep(1)
                                    savegame(pgn)
                                    exit()

                                movemade = True
                                break
                    else:
                        continue
                    break
                
                #if a move has not been made
                if movemade == False:
                    pos[bonded].x = ogpos[bonded][0]
                    pos[bonded].y = ogpos[bonded][1]

                #if a move has been made
                else:
                    movemade = False
                    movecount+=1
                    analysis = _analyze.chess(board,movecount)
                    board = analysis.board
                    compmove = analysis.move
                    pgn.append(compmove)
                    original = analysis.original
                    original = list(original.keys())[0]

                    
                    
                    for i in pos:
                        if compmove in list(moves[pos.index(i)].values())[0]:
                            i.x = movepos[thing2.index(compmove)][0]
                            i.y = movepos[thing2.index(compmove)][1]
                            break
                    

                    moves = analysis.moves
                    allmoves = removedupes(moves)
                    

                    pieces = []
                    for _ in range(0,len(board)):
                        pieces.append("0")
                    
                    pos = copy.copy(pieces)
                    ogpos = copy.copy(pieces)
                    movepos = copy.copy(pieces)
                    things = copy.copy(pieces)
                    thing2 = copy.copy(pieces)



                    for j in range(0,8):
                        for i in range(0,8):
                            for piece in board:
                                if xaxis.index(piece[1]) == i and 8-int(piece[2]) == j: 
                                    pieces[board.index(piece)] = pygame.image.load(f"{images[piece[0]]}.png")
                                    things[board.index(piece)] = piece
                                    pos[board.index(piece)] = pygame.Vector2(37.5+340+75*i, 37.5+60+75*j)
                                    ogpos[board.index(piece)] = [37.5+340+75*i, 37.5+60+75*j]

                            for move in allmoves:
                                if "=" in move:
                                    if xaxis.index(move[-4]) == i and 8-int(move[-3]) == j:
                                        movepos.append([37.5+340+75*i, 37.5+60+75*j])
                                        thing2.append(move)

                                elif xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:
                                    movepos.append([37.5+340+75*i, 37.5+60+75*j])
                                    thing2.append(move)
                    
                    #play moving sound
                    if "x" not in compmove:
                        playsound.playsound("move.mp3",block=False)

                    #play different sound for capture
                    else:
                        playsound.playsound("takes.mp3",block=False)

                    king = [False,False]

                    for i in moves:
                        if list(i.keys())[0][0] == "K":
                            king[0] = True

                        elif list(i.keys())[0][0] == "k":
                            king[1] = True
                                    
                bonded = None
                

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    #drawing the chess board
    for j in range(0,8):
        for i in range(0,8):
            
            #alternating white and purple
            if i%2 == 0:
                if j%2==0:
                    color = "white"
                else:
                    color = "#D684FF"
            else:
                if j%2==0:
                    color = "#D684FF"
                else:
                    color = "white"
            
            #showing which piece moved where by making the square yellow
            if compmove !=None and original!= None:
                if "=" in compmove:
                    if i == xaxis.index(compmove[-4]) and j==8-int(compmove[-3]):
                        if color == "white":
                            color = "#FFFFC6"
                        else:
                            color = "#FFE884"
                else:
                    if i == xaxis.index(compmove[-2]) and j==8-int(compmove[-1]):
                        if color == "white":
                            color = "#FFFFC6"
                        else:
                            color = "#FFE884"

                if i == xaxis.index(original[-2]) and j==8-int(original[-1]):
                    if color == "white":
                        color = "#FFFFC6"
                    else:
                        color = "#FFE884"

            pygame.draw.rect(screen,color,pygame.Rect(340+75*i, 60+75*j, 75, 75))
            
            if bonded!=None:
                for move in list(moves[bonded].values())[0]:
                    if "=" in move:
                        if xaxis.index(move[-4]) == i and 8-int(move[-3]) == j:

                            if color == "white":
                                color = "#EBCCFF"
                            elif color == "#D684FF":
                                color = "#945CB2"

                        pygame.draw.circle(screen, color, [377.5+75*i, 97.5+75*j], 15)

                    elif xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:

                        if color == "white":
                            color = "#EBCCFF"
                        elif color == "#D684FF":
                            color = "#945CB2"

                        pygame.draw.circle(screen, color, [377.5+75*i, 97.5+75*j], 15)
            


    #drawing pieces
    for i in range(0,len(pieces)):
        pieces[i].convert()
        pieces1 = pieces[i].get_rect()
        pieces1.center = (pos[i].x,pos[i].y)
        screen.blit(pieces[i],pieces1)


    mouse = pygame.mouse.get_pos()


    if holding == True:
        if bonded == None:
            for i in pos:
                if board[pos.index(i)][0].isupper() == switch:
                    if mouse[0] > i.x-50 and mouse[0] < i.x+50:
                        if mouse[1] > i.y-50 and mouse[1] < i.y+50:
                            #determining which piece we are clicking on
                            i.x = mouse[0]
                            i.y = mouse[1]
                            bonded = pos.index(i)
                            break

        else:
            #make the piece follow the cursor
            pos[bonded].x = mouse[0]
            pos[bonded].y = mouse[1]

    #if no white king
    if king[0] == False:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("You Lost", True, 'red')
        textRect = text.get_rect()
        textRect.center = (1280 // 2, 720 // 2)
        screen.blit(text, textRect)

        pygame.display.flip()
        playsound.playsound("mate.mp3")
        time.sleep(1)
        savegame(pgn)
        exit()
    


    #pieces = Image.open("pieces.png").crop((0,0,30,30))
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
exit()
    
