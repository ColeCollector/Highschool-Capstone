import random
import pickle

# Loading the lists from the file
with open('book_lichess.pkl', 'rb') as file:
    data = pickle.load(file)

def based_move(played_moves):
    next_move = {}  
    total_moves_played = 0
    
    color = 'black' if len(played_moves) % 2 == 0 else 'white'

    for line in data:
        moves,outcome = line[:-1],line[-1]

        # This should allow for alternate move orders
        if len(moves) > len(played_moves) and sorted(moves[:len(played_moves)]) == sorted(played_moves):

            if outcome != '1/2-1/2':
                if moves[len(played_moves)] not in next_move:
                    next_move[moves[len(played_moves)]] = [0,0]

                next_move[moves[len(played_moves)]][1] += 1
                total_moves_played+=1

            if outcome == '1-0':
                next_move[moves[len(played_moves)]][0] += 1

    # If no games or 1 game has been played
    if total_moves_played in [0,1]: return None

    for move in next_move:
        if color == 'black': winrate = 1-next_move[move][0]/next_move[move][1]
        else: winrate = next_move[move][0]/next_move[move][1]

        next_move[move] = winrate * (((next_move[move][1]+1)/(total_moves_played+1))**0.5)

    next_move = dict(sorted(next_move.items(), key=lambda item: item[1], reverse=True)[:3])
    return random.choice(list(next_move.keys()))

if __name__ == "__main__":
    print(based_move(['d4','d5']))