import pygame
from solve import solve, isBoardValid,checkValidity

pygame.font.init()

WIDTH,HEIGHT = 540,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SUDOKU SOLVER AND VISUALIZER")
WHITE = (255,255,255)
FPS = 60

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self,rows,cols,width,height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        # model:current grid
        self.model = None
        # selected : position selected i,j = self.selected
        self.selected = None
        # cubes :matrix/list of objects of class Cube ,each object corresponds each value/cell in the sudoku grid
        self.cubes = [[Cube(self.board[i][j],i,j,width,height)for j in range(cols)]for i in range(rows)]

    def draw(self,win):
        gap = self.width / 9
         # Drawing each cell,placing values
        
        for i in range(self.rows):
            for j in range(self.cols):
                  self.cubes[i][j].draw(win)

        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
        
       
    def clear(self):
      row,col = self.selected

      if(board.cubes[row][col].value == 0):
        board.cubes[row][col].set_temp(0)
    

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_val(val)
            self.update_model()

            # if isBoardValid(val,self.model,row,col) and solve(self.model):
            if isBoardValid(val,self.model,row,col):
                return True
            else:
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].set_temp(val)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)
    
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
      # param: position  and return: (row, col)
      
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def set_color(self,color):
      i,j = self.selected
      self.cubes[i][j].set_cube_color(color)

    def reset(self):
      self.cubes = [[Cube(self.board[i][j],i,j,self.width,self.height)for j in range(self.cols)]for i in range(self.rows)]

        



class Cube:

    rows = 9
    cols = 9

    def __init__(self,value,row,col,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False
        self.color = None

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (0,0,0))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            box = pygame.Rect(x,y,gap,gap)
            pygame.draw.rect(win,(0,153,153),box)
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        

        if self.selected:
          pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    
    def set_val(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val
    
    def set_cube_color(self,color):
      self.color = color


def isValid(c,board,i,j):
  # val = board[i][j]
  for k in range(board.rows):
    if(board.cubes[i][k].value == c):
      return False
    
    if(board.cubes[k][j].value == c):
      return False
    
    if(board.cubes[3*(i//3)+(k//3)][3*(j//3)+(k%3)].value == c):
      return False

  return True

def fillSudoku(board):

  for i in range(board.rows):
    for j in range(board.cols):
      if(board.cubes[i][j].value==0):
        pygame.event.pump()
        for c in range(1,10):
            if(isValid(c,board,i,j)):
                board.cubes[i][j].set_val(c)

                # screen.fill((255, 255, 255))
                draw_window(board)
                pygame.time.delay(20)
                if(fillSudoku(board)):
                    return True
                else:
                    board.cubes[i][j].set_val(0)
                    # screen.fill((255, 255, 255))
                    draw_window(board)
                    pygame.time.delay(50)

        return False
  return True

def draw_window(board):
  WIN.fill(WHITE)
  fnt = pygame.font.SysFont("comicsans", 40)
  board.update_model()
  if(checkValidity(board.model)):
    text = fnt.render("VALID BOARD" , 1, (255, 0, 0))
    WIN.blit(text, (20, 560))
  else:
    text = fnt.render("NOT VALID BOARD", 1, (255, 0, 0))
    WIN.blit(text, (20, 560))
  board.draw(WIN)
  pygame.display.update()



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



def main():

    board = Grid(9,9,WIDTH,540)
    board2 = Grid(9,9,WIDTH,540)
    key = None
    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
            
            if(event.type == pygame.KEYDOWN) :
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_r:
                    board.reset()
                    key = None
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    if(fillSudoku(board2)):
                        print("success")
                    else:
                        print("failed")
                    # printSudoku(board.board)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
          board.sketch(key)
          i,j = board.selected
          if(board.place(board.cubes[i][j].temp)):
            board.set_color("green")
          else:
            board.set_color("red")


    
        draw_window(board)

    pygame.quit()    



if __name__=="__main__":
    main()
# TO DO:
# CHECK VALIDITY OF SUDOKU GRID BEFORE SOLVING IT
