import math
import random
import pickle






white_file = open("ColeCollector-white.pgn","r")
white_info = white_file.read().split("\n\n")

black_file =  open("ColeCollector-black.pgn","r")
black_info = black_file.read().split("\n\n")


alpha = ['a','b','c','d','e','f','g','h','-']
lines = []

def based_move(played_moves):
    next_move = {}  
    total_moves_played = 0

    if len(played_moves) % 2 == 0:
        info = black_info

    else:
        info = white_info

    for i in range(len(info)-1):
        mylist = info[i].split('\n')[-1].split(" ")
        filtered_list = [item for item in mylist if item.replace('+','') and any(char in alpha for char in item)]
        lines.append(filtered_list)

        moves,outcome = filtered_list[:-1],filtered_list[-1]

        # This should allow for alternate move orders
        moves_sofar = moves[:len(played_moves)]
        moves_sofar.sort()
        sorted_played_moves = played_moves
        sorted_played_moves.sort()

        if len(moves) > len(played_moves) and moves_sofar == sorted_played_moves:
            
            if outcome != '1/2-1/2':
                if moves[len(played_moves)] not in next_move:
                    next_move[moves[len(played_moves)]] = [0,0]
                next_move[moves[len(played_moves)]][1] += 1
                total_moves_played+=1

            if outcome == '1-0':
                next_move[moves[len(played_moves)]][0] += 1

    for move in next_move:

        winrate = 1-next_move[move][0]/next_move[move][1]
        #print(winrate,move)
        winrate/=2

        next_move[move] = winrate - (1.96/(next_move[move][1]+1))*(math.sqrt(winrate*(1-winrate)+((1.96**2)/(4*(next_move[move][1]+1)))))
    
        
    with open('book_black.pkl', 'wb') as filed:
        pickle.dump(lines, filed)

    # So that we don't follow one game
    if total_moves_played == 1: return None

    try:
        next_move = dict(sorted(next_move.items(), key=lambda item: item[1], reverse=True)[:3])
        #print(next_move)
        #print(list(next_move.keys()))
        return random.choice(list(next_move.keys()))
    
    except:
        return None


if __name__ == "__main__":
    print(based_move(['d4','d5','Bf4']))
