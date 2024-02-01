import pygame
import time
import random
from PIL import Image
import copy

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
holding = False
bonded = None
turn = "white"
switch = True

board = ['kc8', 'pe6', 'Pe5', 'pf5', 'Nd4', 'Pf4', 'pg4', 'Na3', 'Pg3', 'Be2', 'Kg2']
moves = [{'kc8': []}, {'pe6': []}, {'Pe5': []}, {'pf5': []}, {'Nd4': ['Nb3', 'Nb5', 'Nc2', 'Nc6', 'Nf3', 'Nxe6', 'Nxf5']}, {'Pf4': []}, {'pg4': []}, {'Na3': ['Nb1', 'Nb5', 'Nc2', 'Nc4']}, {'Pg3': []}, {'Be2': ['Ba6', 'Bb5', 'Bc4', 'Bd1', 'Bd3', 'Bf1', 'Bf3', 'Bxg4']}, {'Kg2': ['Kf1', 'Kf2', 'Kf3', 'Kg1', 'Kh1', 'Kh2', 'Kh3']}]
allmoves = ['Nb3', 'Ndb5', 'Ndc2', 'Nc6', 'Nf3', 'Nxe6', 'Nxf5', 'Nb1', 'Nab5', 'Nac2', 'Nc4', 'Ba6', 'Bb5', 'Bc4', 'Bd1', 'Bd3', 'Bf1', 'Bf3', 'Bxg4', 'Kf1', 'Kf2', 'Kf3', 'Kg1', 'Kh1', 'Kh2', 'Kh3']
xaxis = ['a','b','c','d','e','f','g','h']
images = {"K":"Wking", "Q":"Wqueen","R":"Wrook","B":"Wbishop","N":"Wknight","P":"Wpawn","k":"Bking","q":"Bqueen","r":"Brook","b":"Bbishop","n":"Bknight","p":"Bpawn"}
pieces = []
pos = []
ogpos = []
movepos = []

for j in range(0,8):
    for i in range(0,8):
        for piece in board:
            if xaxis.index(piece[1]) == i and 8-int(piece[2]) == j: 
                pieces.append(pygame.image.load(f"{images[piece[0]]}.png"))
                pos.append(pygame.Vector2(37.5+340+75*i, 37.5+60+75*j))
                ogpos.append([37.5+340+75*i, 37.5+60+75*j])

        for move in allmoves:
            if xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:
                movepos.append([37.5+340+75*i, 37.5+60+75*j])
                

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if you are holding left click
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding = True


        #if you let go of left click
        if event.type == pygame.MOUSEBUTTONUP:
            holding = False
            if bonded!= None:
                
                    
                for i in movepos:
                    print(allmoves[movepos.index(i)])
                    print(list(moves[bonded].values())[0])

                    if (pos[bonded].x > i[0]-50 and pos[bonded].x < i[0]+50) and (pos[bonded].y > i[1]-50 and pos[bonded].y <i[1]+50):
                        pos[bonded].x = i[0]
                        pos[bonded].y = i[1]
                        break

                if pos[bonded].y != i[1]:
                    pos[bonded].x = ogpos[bonded][0]
                    pos[bonded].y = ogpos[bonded][1]

                bonded = None

    
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

                if xaxis.index(move[-2]) == i and 8-int(move[-1]) == j:
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
    

