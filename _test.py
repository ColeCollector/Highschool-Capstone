import chess
import chess.engine
import random

# Define the path to the Stockfish executable
stockfish_path = "stockfish.exe"


# Initialize the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Create a new chess board
board = chess.Board()
board.set_fen('rnbqkbnr/pppp2pp/8/4pp2/2BPP3/8/PPP2PPP/RNBQK1NR b KQkq - 0 3')

# Analyze the position and get the top 10 moves
info = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=5)

# Extract and print the top 10 moves and their evaluations
top5 = []
top5_weights = []
switch = False

for move_info in info:
    move = move_info["pv"][0]  # Get the principal variation (best move)
    san_move = board.san(move)  # Convert move to SAN notation
    score = move_info["score"].relative.score()  # Get the evaluation score
    original = f"{board.piece_at(move.from_square)}{chess.square_name(move.from_square)}"

    top5.append([san_move,original,move])
    top5_weights.append(score)
    print(san_move,score)

if min(top5_weights) <= 0:
    top5_weights = [1 + top+min(top5_weights)*-1 for top in top5_weights]



print(random.choices(top5,top5_weights))

# Close the engine
engine.quit()
exit()