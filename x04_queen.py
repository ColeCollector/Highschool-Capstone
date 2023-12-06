def queen(square):
  """
  input:
  str square: the coordinate of the square that the queen is currently located in
  examples: 'f3' or 'g6'
  
  return:
  list of possible squares that the queen can move to:
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

  for i in range(0,8):
    x = xaxis[i]
    differ = abs(xnum - xaxis.index(x))

    if ynum-differ+1 > 0 and ynum-differ+1 <= 8:
      available.append(f"{x}{ynum-differ+1}")
      
    if ynum+differ+1 <= 8 and ynum+differ+1 <= 8:
      available.append(f"{x}{ynum+differ+1}")

    if str(square) in available:
      available.remove(str(square))
  
  print(available)

  return available


def main():
  myList = queen('f3')
  myList.sort()
  assert myList == ['a3', 'a8', 'b3', 'b7', 'c3', 'c6', 'd1', 'd3', 'd5', 'e2', 'e3', 'e4', 'f1', 'f2', 'f4', 'f5', 'f6', 'f7', 'f8', 'g2', 'g3', 'g4', 'h1', 'h3', 'h5']
  myList = queen('g7')
  myList.sort()
  assert myList == ['a1', 'a7', 'b2', 'b7', 'c3', 'c7', 'd4', 'd7', 'e5', 'e7', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g8', 'h6', 'h7', 'h8']

if __name__ == "__main__":
  main()
