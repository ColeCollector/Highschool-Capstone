import math

file = open("ColeCollector-white.pgn","r")
info = file.read().split("\n\n")

alpha = ['a','b','c','d','e','f','g','h','-']

def based_move(played_moves):
    next_move = {}  
    total_moves_played = 0

    for i in range(len(info)-1):
        mylist = info[i].split('\n')[-1].split(" ")
        filtered_list = [item for item in mylist if item.replace('+','') and any(char in alpha for char in item)]
        moves,outcome = filtered_list[:-1],filtered_list[-1]

        if len(moves) > len(played_moves) and moves[:len(played_moves)] == played_moves:
            
            if outcome != '1/2-1/2':
                if moves[len(played_moves)] not in next_move:
                    next_move[moves[len(played_moves)]] = [0,0]
                next_move[moves[len(played_moves)]][1] += 1
                total_moves_played+=1

            if outcome == '1-0':
                next_move[moves[len(played_moves)]][0] += 1

    for move in next_move:

        winrate = 1-next_move[move][0]/next_move[move][1]
        winrate/=2

        next_move[move] = winrate - (1.96/(next_move[move][1]+1))*(math.sqrt(winrate*(1-winrate)+((1.96**2)/(4*(next_move[move][1]+1)))))
    
    # So that we don't follow one game
    if total_moves_played == 1: return None

    try:
        return max(next_move, key=next_move.get)
    
    except:
        return None


if __name__ == "__main__":
    print(based_move(['d4','d5','Bf4']))
