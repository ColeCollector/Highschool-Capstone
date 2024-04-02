def theory(pgn):
    file = open("!book.txt","r")
    info = file.read().split("\n")

    for i in info:
        past = ""
        for x,char in enumerate(i):
            if x < len(i)-1:
                if char not in ['.','0','1','2','3','4','5','6','7','8','9'] or (i[x-1] not in ['.','0','1','2','3','4','5','6','7','8','9',' '] and char!="." ):
                    if len(past)==0:past = past+char
                    elif (char==" " and past[-1]==" ") == False: past = past+char
        

        past = past.split(" ")[1:]
        if len(past)> len(pgn):
            for x, p in enumerate(pgn):

                if x==len(pgn)-1:
                    return p

                if p != past[x]:
                    break

print(theory(['d4', 'Nc6', 'd5']))