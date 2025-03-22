import pygame
import chess
import chess.engine
import _openingtree
import random
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Initialize variables
running = True
holding = False
bonded = None
movemade = False
compmove = None
hint = None
hint_end = None
original = None
eval_toggle = False
switch = True
resign = False
treemove = 0
eval = 0
drop_counter = 0

pgn = []

sounds = [pygame.mixer.Sound('sounds/mate.mp3'),pygame.mixer.Sound('sounds/move.mp3'),pygame.mixer.Sound('sounds/sparkle.mp3'),pygame.mixer.Sound('sounds/takes.mp3')]
sounds[2].set_volume(0.05)

# Initialize chess board
board = chess.Board()
board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')   

# Define the path to the Stockfish executable
stockfish_path = "stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Define square coordinates and image mappings
xaxis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
images = {"K": "white/King", "Q": "white/Queen", "R": "white/Rook", "B": "white/Bishop", "N": "white/Knight", "P": "white/Pawn",
          "k": "black/King", "q": "black/Queen", "r": "black/Rook", "b": "black/Bishop", "n": "black/Knight", "p": "black/Pawn"}

# Display text on the screen
def show_text(text, size, location, color):
    font_surface = pygame.font.Font(None, size).render(text, True, color)
    text_rect = font_surface.get_rect(center=location)
    screen.blit(font_surface, text_rect)

def savegame(pgn):
    if pgn!=[]:
        file = open("stockfish_book.txt","a")

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

def check_condition(switch, piece, i, j, opponent):
    if piece == None:
        return False
    
    if switch:
        if '=' in piece:
            return xaxis.index(piece[-4]) == i and 8 - int(piece[-3]) == j
        
        elif 'O-O' == piece:
            if opponent == True:
                return 6 == i and 0 == j
            else:
                return 6 == i and 7 == j

        elif 'O-O-O' == piece:
            if opponent == True:
                return 2 == i and 0 == j
            else:
                return 2 == i and 7 == j
        
        else:
            return xaxis.index(piece[-2]) == i and 8 - int(piece[-1]) == j
    else:
        if '=' in piece:
            return 7 - xaxis.index(piece[-4]) == i and int(piece[-3]) - 1 == j
        
        elif 'O-O' == piece:
            if opponent == True:
                return 1 == i and 0 == j
            else:
                return 1 == i and 7 == j

        elif 'O-O-O' == piece:
            if opponent == True:
                return 5 == i and 0 == j
            else:
                return 5 == i and 7 == j
        
        else:
            return 7 - xaxis.index(piece[-2]) == i and int(piece[-1]) - 1 == j

def piece_with_square(piece, square):
    piece_symbol = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol().lower()
    return f"{piece_symbol}{chess.square_name(square)}"

# Resets board visuals
def board_reset():
    global circle_squares, moves, board_pieces, piece_images, pos, og_pos, movepos, sorted_pieces, sorted_moves
    piece_images = []
    pos = []
    og_pos = []
    movepos = []
    sorted_pieces = []
    sorted_moves = []
    board_pieces = []
    moves = {}
    circle_squares = []

    # Initialize board piece_images
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            board_pieces.append(piece_with_square(piece, square))

    # Initialize moves
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        piece_square = piece_with_square(piece, move.from_square)
        san_move = board.san(move).replace('+', '').replace('#', '')
        if piece_square not in moves:
            moves[piece_square] = []
        moves[piece_square].append(san_move)
        circle_squares.append(san_move)

    # Initialize board rendering
    for j in range(8):
        for i in range(8):
            for piece in board_pieces:
                if check_condition(switch, piece, i, j, None):
                    piece_images.append(pygame.image.load(f"images/{images[piece[0]]}.png"))
                    sorted_pieces.append(piece)
                    pos.append(pygame.Vector2(340 + 75 * i + 37.5, 60 + 75 * j + 37.5))
                    og_pos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])

            for move in circle_squares:
                if check_condition(switch, move, i, j, None):
                    movepos.append([340 + 75 * i + 37.5, 60 + 75 * j + 37.5])
                    sorted_moves.append(move)

board_reset()

transparent_surface = pygame.Surface((1280, 200), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 128))

# Create a surface for the circle
circle_surface = pygame.Surface((1280, 200), pygame.SRCALPHA)
circle_surface.set_alpha(64)

# Draw a circle on the surface
pygame.draw.circle(circle_surface, (64,20,86), (30, 30), 15)

while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            holding = True

            # Buttons
            for j in range(4):
                if pygame.Rect(1000,265+50*j,150,40).collidepoint(mouse):
                    if button_text[j] == "Resign":
                        resign = True

                    elif button_text[j] == "Hint":
                        result = engine.play(board, chess.engine.Limit(time=0.5))
                        hint = f"{board.piece_at(result.move.from_square)}{chess.square_name(result.move.from_square)}"
                        hint_end = board.san(result.move).replace('+','').replace('#', '')

                    elif button_text[j] == "Eval":
                        if eval_toggle:
                            eval_toggle = False
                        else:
                            eval_toggle = True

                    elif button_text[j] == "Flip":
                        if switch == True: switch = False
                        else: switch = True

                        # Don't print an old hint
                        hint = None
                        hint_end = None

                        # Get the best move from Stockfish
                        result = engine.play(board, chess.engine.Limit(time=1))
                        original = f"{board.piece_at(result.move.from_square)}{chess.square_name(result.move.from_square)}"

                        compmove = board.san(result.move).replace('+','').replace('#', '')
                        pgn.append(compmove)
                        board.push(result.move)
                        
                        board_reset()
                        
                        # Drawing the chess board
                        for j in range(8):
                            for i in range(8):
                                color = "white" if (i + j) % 2 == 0 else "#D684FF"
                                pygame.draw.rect(screen, color, pygame.Rect(340 + 75 * i, 60 + 75 * j, 75, 75))

                        # Drawing piece_images
                        for i in range(len(piece_images)):
                            piece_images[i].convert()
                            rect = piece_images[i].get_rect(center=(pos[i].x, pos[i].y))
                            screen.blit(piece_images[i], rect)

                        # Mate sound
                        if "#" in compmove:
                            sounds[0].play()

                        # Moving sound
                        elif "x" not in compmove:
                            sounds[1].play()

                        # Play different sound for capture
                        else:
                            sounds[3].play()

                        pygame.display.flip()
            
            # Switching to a new piece if you click on another piece while holding a piece
            for i in og_pos:
                if sorted_pieces[og_pos.index(i)][0].isupper() == switch:
                    if (mouse[0] > i[0] - 50 and mouse[0] < i[0] + 50) and (mouse[1] > i[1] - 50 and mouse[1] < i[1] + 50):
                        
                        # To fix a bug/visual thing
                        if bonded != og_pos.index(i):
                            drop_counter = 0

                        bonded = og_pos.index(i)
                        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if bonded is not None:
                if sorted_pieces[bonded] in moves:
                    for l, i in enumerate(movepos):
                        if (mouse[0] > i[0] - 50 and mouse[0] < i[0] + 50) and (mouse[1] > i[1] - 50 and mouse[1] < i[1] + 50):
                            if sorted_pieces[bonded] in moves and sorted_moves[l] in moves[sorted_pieces[bonded]]:
                                hint = None
                                hint_end = None

                                #play moving sound
                                if "x" not in sorted_moves[l]:
                                    sounds[1].play()

                                #play different sound for capture
                                else:
                                    sounds[3].play()

                                pos[bonded] = pygame.Vector2(i[0], i[1])
                                movemade = True

                                san_move = sorted_moves[l]
                                pgn.append(san_move)
                                move = board.parse_san(san_move)
                                board.push(move)

                                board_reset()

                                # Drawing the chess board
                                for j in range(8):
                                    for i in range(8):
                                        color = "white" if (i + j) % 2 == 0 else "#D684FF"
                                        pygame.draw.rect(screen, color, pygame.Rect(340 + 75 * i, 60 + 75 * j, 75, 75))

                                # Drawing piece_images
                                for i in range(len(piece_images)):
                                    piece_images[i].convert()
                                    rect = piece_images[i].get_rect(center=(pos[i].x, pos[i].y))
                                    screen.blit(piece_images[i], rect)

                                pygame.display.flip()
                                
                                treemove = _openingtree.based_move(pgn)

                                if treemove != None: 
                                    compmove = treemove
                                    treemove = board.parse_san(treemove)
                                    original = f"{board.piece_at(treemove.from_square)}{chess.square_name(treemove.from_square)}"
                                    pgn.append(compmove)
                                    board.push(treemove)

                                else:
                                    # Get the best move from Stockfish
                                    '''
                                    result = engine.play(board, chess.engine.Limit(time=1))
                                    original = f"{board.piece_at(result.move.from_square)}{chess.square_name(result.move.from_square)}"
                                    compmove = board.san(result.move).replace('+','').replace('#', '')
                                    pgn.append(compmove)
                                    board.push(result.move)
                                    '''
                                    # If the bot isn't mated
                                    if not board.is_checkmate():
                    
                                        # Gets the top 10 best moves from stockfish and grabs a random one based on its score

                                        info = engine.analyse(board, chess.engine.Limit(time=1.0), multipv=5)

                                        top10 = []
                                        top10_weights = []
                                        print("")
                                        for move_info in info:
                                            move = move_info["pv"][0]
                                            san_move = board.san(move)
                                            score = move_info["score"].relative.score()
                                            original = f"{board.piece_at(move.from_square)}{chess.square_name(move.from_square)}"
                                            top10.append([san_move,original,move])

                                            print(san_move,score)

                                            if score == None and info.index(move_info) == 0: 
                                                score = 1000
                                            else:
                                                score = -1000

                                            top10_weights.append(score)

                                            if score < top10_weights[0]-100:
                                                break

                                        if min(top10_weights) <= 0:
                                            top10_weights = [top+min(top10_weights)*-1 for top in top10_weights]
                                        try:
                                            random_move = random.choices(top10,top10_weights)[0]
                                        except:
                                            random_move = top10[0]

                                        original = random_move[1]
                                        compmove = random_move[0].replace('+','').replace('#', '')
                                        pgn.append(compmove)
                                        board.push(random_move[2])

                                if eval_toggle:
                                    info = engine.analyse(board, chess.engine.Limit(time=2))
                                    eval = info["score"]
                                    eval = eval.pov(chess.WHITE).score()


                                # Opening Tree Sound effect
                                if treemove != None: 
                                    sounds[2].play()
                                
                                # Mate sound
                                if "#" in compmove:
                                    sounds[0].play()

                                # Moving sound
                                elif "x" not in compmove:
                                    sounds[1].play()

                                # Play different sound for capture
                                else:
                                    sounds[3].play()

                                board_reset()
                                break

                if not movemade:
                    if (mouse[0] > og_pos[bonded][0] - 50 and mouse[0] < og_pos[bonded][0] + 50) and (mouse[1] > og_pos[bonded][1] - 50 and mouse[1] < og_pos[bonded][1] + 50):
                        drop_counter += 1
                        pos[bonded] = pygame.Vector2(og_pos[bonded][0], og_pos[bonded][1])
                        if drop_counter == 2:
                            drop_counter = 0
                            bonded = None

                    else:
                        pos[bonded] = pygame.Vector2(og_pos[bonded][0], og_pos[bonded][1])
                        bonded = None
                        
                else:
                    movemade = False
                    bonded = None

            holding = False

    screen.fill("white")

    button_text = ["Resign","Hint","Eval","Flip"]

    for j in range(4):
        if pygame.Rect(1000,265+50*j,150,40).collidepoint(mouse):
            pygame.draw.rect(screen, '#D684FF', (1000,265+50*j,150,40))
            show_text(button_text[j],40,(1075,285+50*j),'white')

        else:
            pygame.draw.rect(screen, '#AE4ADB', (1000,265+50*j,150,40))
            show_text(button_text[j],40,(1075,285+50*j),'white')

    # Drawing the chess board
    for j in range(8):
        for i in range(8):
            color = "white" if (i + j) % 2 == 0 else "#D684FF"

            if check_condition(switch, compmove, i, j, True):
                color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"
    
            if check_condition(switch, original, i, j, None):
                color = "#FFFFC6" if (i + j) % 2 == 0 else "#FFE884"

            if check_condition(switch, hint_end, i, j, None):
                color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

            if check_condition(switch, hint, i, j, None):
                color = "#C9E5C0" if (i + j) % 2 == 0 else "#ACE89B"

            pygame.draw.rect(screen, color, pygame.Rect(340 + 75 * i, 60 + 75 * j, 75, 75))

            if bonded is not None and sorted_pieces[bonded] in moves:
                for move in moves[sorted_pieces[bonded]]:
                    if check_condition(switch, move, i, j, None):
                        screen.blit(circle_surface, [377.5 - 30 + 75 * i, 97.5 - 30 + 75 * j])


    # Drawing piece_images
    for i in range(len(piece_images)):
        piece_images[i].convert()
        rect = piece_images[i].get_rect(center=(pos[i].x, pos[i].y))
        screen.blit(piece_images[i], rect)

    if holding:
        if bonded != None:
            pos[bonded] = pygame.Vector2(mouse[0], mouse[1])

    if eval_toggle:
        pygame.draw.rect(screen,'#AE4ADB',(250,60,20,600))
        if eval != None:
            pygame.draw.rect(screen,'white',(252,62,16,298+eval/3))
            show_text(str(round(eval/60,2)),40,(200,720/2),'#AE4ADB')

    if len(moves) == 0 or resign == True:
        font = pygame.font.Font('freesansbold.ttf', 50)

        if (len(pgn) % 2 == 1 and switch == True) or (len(pgn) % 2 == 0 and switch == False):
            text = font.render("You Won", True, 'green')
            
        else:
            text = font.render("You Lost", True, 'red')

        textRect = text.get_rect()
        textRect.center = (1280 // 2, 720 // 2)
        
        screen.blit(transparent_surface, (0,720/2-100,600,100))
        screen.blit(text, textRect)
        pygame.display.flip()
        time.sleep(3)
                                                
        savegame(pgn)
        pgn = []
        resign = False
        original = None
        compmove = None
        eval = 0
                                          
        board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') 
        board_reset()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
engine.quit()