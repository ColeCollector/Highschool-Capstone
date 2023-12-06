#!python3

def bishop(square,board1,board2):
  """
  input:
  str square: the coordinate of the square that the bishop is currently located in
  examples: 'f3' or 'g6'
  
  return:
  list of possible squares that the bishop can move to:
  """

  #I accidentally got rows and collumns mixed up...
  available = []

  currentx = square[0]
  currenty = square[1]
  
  xaxis = ['a','b','c','d','e','f','g','h']
  yaxis = ['1','2','3','4','5','6','7','8']
  
  xnum = xaxis.index(currentx)
  ynum = yaxis.index(currenty)
  
  for i in range(0,8):
    x = xaxis[i]
    differ = abs(xnum - xaxis.index(x))

    if ynum-differ+1 > 0 and ynum-differ+1 <= 8:
      available.append(f"{x}{ynum-differ+1}")
      
    if ynum+differ+1 <= 8 and ynum+differ+1 <= 8:
      available.append(f"{x}{ynum+differ+1}")

    if str(square) in available:
      available.remove(str(square))
  
  available.sort()
  print(available)
  for i in board2:
    if i in available:
      print(i)
      for k in range(1,8):
        try:
          print(f"{xaxis[xaxis.index(i[:1])+k]}{yaxis[yaxis.index(i[1:])+k]}")
        except:
          pass

  return available

