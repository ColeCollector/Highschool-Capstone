import pygame
import backup
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

#program needs to be given board and moves
board = ['ra8', 'nb8', 'bc8', 'qd8', 'ke8', 'bf8', 'ng8', 'rh8', 'pa7', 'pb7', 'pc7', 'pd7', 'pe7', 'pf7', 'pg7', 'ph7', 'Pa2', 'Pb2', 'Pc2', 'Pd2', 'Pe2', 'Pf2', 'Pg2', 'Ph2', 'Ra1', 'Nb1', 'Bc1', 'Qd1', 'Ke1', 
'Bf1', 'Ng1', 'Rh1']
moves = [{'ra8': []}, {'nb8': []}, {'bc8': []}, {'qd8': []}, {'ke8': []}, {'bf8': []}, {'ng8': []}, {'rh8': []}, {'pa7': []}, {'pb7': []}, {'pc7': []}, {'pd7': []}, {'pe7': []}, {'pf7': []}, {'pg7': []}, {'ph7': 
[]}, {'Pa2': ['a3', 'a4']}, {'Pb2': ['b3', 'b4']}, {'Pc2': ['c3', 'c4']}, {'Pd2': ['d3', 'd4']}, {'Pe2': ['e3', 'e4']}, {'Pf2': ['f3', 'f4']}, {'Pg2': ['g3', 'g4']}, {'Ph2': ['h3', 'h4']}, {'Ra1': []}, {'Nb1': ['Na3', 'Nc3']}, {'Bc1': []}, {'Qd1': []}, {'Ke1': []}, {'Bf1': []}, {'Ng1': ['Nf3', 'Nh3']}, {'Rh1': []}]
#board = ['kd7', 'pe6', 'Pe5', 'pf5', 'Nd4', 'Pf4', 'pg4', 'Na3', 'Pg3', 'Be2', 'Kf2']
#moves = [{'kd7': []}, {'pe6': []}, {'Pe5': []}, {'pf5': []}, {'Nd4': ['Nb3', 'Ndb5', 'Ndc2', 'Nc6', 'Nf3', 'Nxe6', 'Nxf5']}, {'Pf4': []}, {'pg4': []}, {'Na3': ['Nb1', 'Nab5', 'Nac2', 'Nc4']}, {'Pg3': []}, {'Be2': ['Ba6', 'Bb5', 'Bc4', 'Bd1', 'Bd3', 'Bf1', 'Bf3', 'Bxg4']}, {'Kf2': ['Ke1', 'Ke3', 'Kf1', 'Kf3', 'Kg1', 'Kg2']}]
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
poop = False
movecount = 0
"""for piece in board:
    pieces.append(pygame.image.load(f"{images[piece[0]]}.png"))
    things.append(piece)
    pos.append(pygame.Vector2(37.5+340+75*xaxis.index(piece[1]), 37.5+60+75*(8-int(piece[2]))))
    ogpos.append([37.5+340+75*xaxis.index(piece[1]), 37.5+60+75*(8-int(piece[2])]))

for move in allmoves:
    movepos.append([37.5+340+75*xaxis.index(move[-2]), 37.5+60+75*(8-int(piece[2]))])
    thing2.append(move)
"""




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





while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If you click middle mouse button
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:




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
                            #if you are clicking on a piece
                            if (pos[bonded].x > i[0]-50 and pos[bonded].x < i[0]+50) and (pos[bonded].y > i[1]-50 and pos[bonded].y <i[1]+50):
                                playsound.playsound("move.mp3",block=False)
                                pos[bonded].x = i[0]
                                pos[bonded].y = i[1]
                                
                                #print("Your move:",thing2[j])
                                
                                modified = modify(moves,thing2[j])
                                
                                moves = modified[0]
                                board = modified[1]

                                king = [False,False]

                                for i in moves:
                                    if list(i.keys())[0][0] == "K":
                                        king[0] = True

                                    elif list(i.keys())[0][0] == "k":
                                        king[1] = True

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
                                    exit()
                                
                                #if no black king
                                elif king[1] == False:
                                    font = pygame.font.Font('freesansbold.ttf', 50)
                                    text = font.render("You Won", True, 'purple')
                                    textRect = text.get_rect()
                                    textRect.center = (1280 // 2, 720 // 2)
                                    screen.blit(text, textRect)

                                    pygame.display.flip()
                                    playsound.playsound("mate.mp3")
                                    time.sleep(1)
                                    exit()

                                poop = True
                                break
                    else:
                        continue
                    break
                

                if poop == False:
                    pos[bonded].x = ogpos[bonded][0]
                    pos[bonded].y = ogpos[bonded][1]

                else:
                    poop = False
                    movecount+=1
                    analysis = backup.chess(board,movecount)
                    board = analysis.board
                    compmove = analysis.move
                    
                    
                    for i in pos:
                        if compmove in list(moves[pos.index(i)].values())[0]:
                            i.x = movepos[thing2.index(compmove)][0]
                            i.y = movepos[thing2.index(compmove)][1]
                            break
                    

                    moves = analysis.moves
                    allmoves = []
                    for i in moves:
                        vals = list(i.values())[0]
                        if vals!=[]:
                            for j in vals:
                                allmoves.append(j)
                    

                    pieces = []
                    for i in range(0,len(board)):
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
                    playsound.playsound("move.mp3",block=False)


                                    
                bonded = None
                
    
               



    #pe6 [677.5, 247.5]
    #Pe5 [677.5, 322.5]
    #pf5 [752.5, 322.5]
    #Nd4 [602.5, 397.5]
    #Pf4 [752.5, 397.5]
    #pg4 [827.5, 397.5]
    #Na3 [377.5, 472.5]
    #Pg3 [827.5, 472.5]
    #Be2 [677.5, 547.5]
    #Kf2 [752.5, 547.5]
    #kd7 [602.5, 172.5]
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    for j in range(0,8):
        for i in range(0,8):

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
             

            for move in allmoves:
                if "=" in move:
                    if xaxis.index(move[-4]) == i and 8-int(move[-3]) == j:
                        if color == "white":
                            color = "pink"
                        elif color == "#D684FF":
                            color = "#FF7070"

                elif xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:
                    if color == "white":
                        color = "pink"
                    elif color == "#D684FF":
                        color = "#FF7070"

            pygame.draw.rect(screen,color,pygame.Rect(340+75*i, 60+75*j, 75, 75))


            #pieces
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
                                    #print(board[pos.index(i)])
                                    i.x = mouse[0]
                                    i.y = mouse[1]
                                    bonded = pos.index(i)
                                    break
 
                else:
                    pos[bonded].x = mouse[0]
                    pos[bonded].y = mouse[1]



    #pieces = Image.open("pieces.png").crop((0,0,30,30))
            


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
exit()
    

