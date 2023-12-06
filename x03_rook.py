#!python3

def rook(square):
  """
  input:
  str square: the coordinate of the square that the rook is currently located in
  examples: 'f3' or 'g6'
  
  return:
  list of possible squares that the rook can move to:
  """
  available = []

  currentx = square[0]
  currenty = square[1]
  
  xaxis = ['a','b','c','d','e','f','g','h']
  yaxis = ['1','2','3','4','5','6','7','8']
  
  xnum = xaxis.index(currentx)
  ynum = yaxis.index(currenty)

  for i in range(0,8):
    available.append(f"{xaxis[i]}{currenty}")
    available.append(f"{currentx}{yaxis[i]}")


    if str(square) in available:
        available.remove(str(square))
  
  print(available)

  return available

def main():
  myList = rook('f3')
  myList.sort()
  assert myList == ['a3', 'b3', 'c3', 'd3', 'e3', 'f1', 'f2', 'f4', 'f5', 'f6', 'f7', 'f8', 'g3', 'h3']
  myList = rook('g7')
  myList.sort()
  assert myList == ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g8', 'h7']

if __name__ == "__main__":
  main()
