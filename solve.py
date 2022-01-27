
# before placing value
def isValid(c,board,i,j):
  # val = board[i][j]
  for k in range(len(board)):
    if(board[i][k] == c):
      return False
    
    if(board[k][j] == c):
      return False
    
    if(board[3*(i//3)+(k//3)][3*(j//3)+(k%3)] == c):
      return False

  return True

# after placing value
def isBoardValid(c,board,i,j):

  for k in range(len(board)):
    if(board[i][k] == c and k!=j ):
      return False
    
    if(board[k][j] == c and k!=i):
      return False
    
    row = 3*(i//3)+(k//3)
    col = 3*(j//3)+(k%3)
    if(board[row][col] == c and (row!=i and col!=j)):
      return False

  return True

def checkValidity(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if(board[i][j]!=0):
        if(not isBoardValid(board[i][j],board,i,j)):
          return False
  return True

def solve(board):
#   l = ['1','2','3','4','5','6','7','8','9']
  for i in range(len(board)):
    for j in range(len(board[0])):
      if(board[i][j]==0):
        for c in range(1,10):
          if(isValid(c,board,i,j)):
            board[i][j] = c

            if(solve(board)):
              return True
            else:
              board[i][j] = 0
        return False
  return True

def printSudoku(board):
  for i in range(len(board)):
    if(i%3==0 and i!=0):
      print('------------------------')
    for j in range(len(board[0])):
      if(j%3==0 and j!=0):
        print('|',end=" ")
      if(j == len(board[0])-1):
        print(board[i][j])
      else:
        print(board[i][j],end=" ")

    
if __name__=="__main__":
    # board_2 = [
    # ['7','8','.','4','.','.','1','2','.'],
    # ['6','.','.','.','7','5','.','.','9'],
    # ['.','.','.','6','.','1','.','7','8'],
    # ['.','.','7','.','4','.','2','6','.'],
    # ['.','.','1','.','5','.','9','3','.'],
    # ['9','.','4','.','6','.','.','.','5'],
    # ['.','7','.','3','.','.','.','1','2'],
    # ['1','2','.','.','.','7','4','.','.'],
    # ['.','4','9','2','.','6','.','.','7']
    # ]
    board_2 = [
    [7,7,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
    ]

    # printSudoku(board_2)
    # fillSudoku(board_2)
    # printSudoku(board_2)
    print(isBoardValid(7,board_2,0,1))

