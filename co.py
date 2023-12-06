def bishop(square,board1,board2):

  #I accidentally got rows and collumns mixed up...
  available = []
  switch = True
  switch2 = True
  
  xaxis = ['a','b','c','d','e','f','g','h']
  yaxis = ['1','2','3','4','5','6','7','8']
  
  xnum = xaxis.index(square[0])
  ynum = yaxis.index(square[1])

  second = False

  for i in list(range(xnum+1,8)) + list(range(xnum-1,8)):
    
    if second == True:
       i = -i+8

    x = xaxis[i]
    differ = abs(xnum - xaxis.index(x))
    
    if ynum-differ+1 > 0 and ynum-differ+1 <= 8:
      pos = f"{x}{ynum-differ+1}"
      if switch == True and pos not in board2:
        available.append(f"{x}{ynum-differ+1}")

      elif switch == True:
        switch = False
  
    if ynum+differ+1 <= 8 and ynum+differ+1 <= 8:
      pos = f"{x}{ynum+differ+1}"
      if switch2 == True and pos not in board2:
        available.append(f"{x}{ynum+differ+1}")

      elif switch2 == True:
        switch2 = False

    if str(square) in available:
      available.remove(str(square))

    if i == 7:
       switch = True
       switch2 = True
       second = True
  
  available = (list(dict.fromkeys(available)))
  available.sort()
  print(available)
  return available