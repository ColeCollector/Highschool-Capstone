#!python3

def knight(square):
  """
  input:
  str square: the coordinate of the square that the knight is currently located in
  examples: 'f3' or 'g6'
  
  return:
  list of possible squares that the knight can move to:
  """

  available = []

  currentx = square[0]
  currenty = square[1]
  
  xaxis = ['a','b','c','d','e','f','g','h']
  yaxis = ['1','2','3','4','5','6','7','8']
  
  xnum = xaxis.index(currentx)
  ynum = yaxis.index(currenty)

  for i in range(0,8):
    x = xaxis[i]
    y = yaxis[i]
    differ = abs(xnum - xaxis.index(x))

    if differ == 2:

      if ynum + 2 < 9:
        available.append(f"{x}{ynum + 2}")
      if ynum > 0: 
        available.append(f"{x}{ynum}")

    if differ == 1:

      if ynum + 3 < 9:
        available.append(f"{x}{ynum + 3}")
      if ynum - 1 > 0:
        available.append(f"{x}{ynum - 1}")

  if str(square) in available:
    available.remove(str(square))
  
  
  print(available)
    
  return available


def main():
  myList = knight('g7')
  myList.sort()
  assert myList == ['e6', 'e8', 'f5', 'h5']
  myList = knight('d4')
  myList.sort()
  assert myList == ['b3', 'b5', 'c2', 'c6', 'e2', 'e6', 'f3', 'f5']

if __name__ == "__main__":
  main()
