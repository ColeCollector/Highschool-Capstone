**Somethings to know:**
-The files with a "_" at the start are the important ones 
-The files with a "Z" at the start are the unimportant old files

-A chess move will contain a piece that was moved represented by one letter at the start and the square it moved to (a letter and number)
-An uppercase letter in a chess move represents a white piece and a lowercase letter represents a black piece
-If there is only the square in the chess move that means that a pawn was moved
-There is no en passant and no castling due to time pressure

**Terminology:**

Heatmap - Best locations for pieces
FEN - A string of text that represents a current chess position
PGN - A block of text that represents a full chess game

**You can paste one of these two things into https://lichess.org/analysis to look at the chess positon you are in or game you just played**


All previous games are stored in the !book.txt channel, the point of this was to use the past games to find which moves to play which I started to add in test.py but I stopped since I had already spent around 80 hours on this

"_HowTheAlgorithmWorks.PNG" is an image that shows an exmample of how the minmax algorithm works to analyze positions. It looks at all positions that are four moves away, then it assigns them all values, this is what the gold section is. Then it fills in the rest of the table with this information based on who's move it is picking either the maximum value or the minimum value.