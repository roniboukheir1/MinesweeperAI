import pygame,os
import Minesweeper

#WINDOWS
WIDTH = 600
HEIGHT = 400
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#COLORS
GRAY = (200,200,200)
BLACK = (0,0,0)
WHITE = (250,250,250)
BLUE = (0,0,250)
GREEN = (0,250,0)
RED = (250,0,0)
NAVY = (0,0,128)
DARK_GRAY = (150,150,150)
 
#Sizes
padding = 15
boarder_width = (int)(3/4 *( WIDTH - padding))
boarder_height = (int) (HEIGHT - padding * 2)
cell_num = 90
cell_size = 40
cell_num_width = boarder_width // cell_size
cell_num_height = boarder_height // cell_size
INNER_CELL_PADDING = 4
mine_num = 8
cell_num = cell_num_height * cell_num_width

#images
mine = pygame.transform.scale(pygame.image.load(os.path.join('assets','images','mine.png')),  (cell_size -INNER_CELL_PADDING, cell_size - INNER_CELL_PADDING))
flag = pygame.transform.scale(pygame.image.load(os.path.join('assets','images','flag.png')), (cell_size -INNER_CELL_PADDING, cell_size - INNER_CELL_PADDING))

#game
global lost 
lost = False
aiButton = pygame.Rect((3/4 * WIDTH - 10),(1/4 * HEIGHT + 20),140,50)
resetButton = pygame.Rect((3/4 * WIDTH - 10),(1/4 * HEIGHT + 90), 140,50)

#Fonts
pygame.font.init()
smallFonts = pygame.font.Font(os.path.join('assets','fonts','OpenSans-Regular.ttf'),20)
mediumFont = pygame.font.Font(os.path.join('assets','fonts','OpenSans-Regular.ttf'),25)
largeFont = pygame.font.Font(os.path.join('assets','fonts','OpenSans-Regular.ttf'),40)

def draw_grid(grid,adjacent_mines,game):

    for i in range(len(grid)):
    
        for j in range(len(grid[i])):
            
            rect= pygame.Rect(( i * cell_size ) + 15, (j * cell_size) + 15 , cell_size,cell_size)
            cell = grid[i][j]
           
            if cell == 'covered':
                pygame.draw.rect(WINDOWS,GRAY,rect)
                pygame.draw.rect(WINDOWS,WHITE,rect,1)
        
            else:
                if cell == 'flag':
                    WINDOWS.blit(flag,rect)                 

                elif game.is_mine((i,j)) :
                    for i in range(len(grid)):
                        for j in range(len(grid[i])):
                            if game.is_mine((i,j)):
                                rect= pygame.Rect(( i * cell_size ) + 15, (j * cell_size) + 15 , cell_size,cell_size)
                                WINDOWS.blit(mine, rect)
                    global lost      
                    lost = True 
                
                elif cell == 'uncovered': 
                    
                    pygame.draw.rect(WINDOWS,DARK_GRAY,rect)
                    pygame.draw.rect(WINDOWS,WHITE,rect,1)

                    color = getColor(adjacent_mines[i][j])
                    text = smallFonts.render(str(adjacent_mines[i][j]), True, color)
                    rect.x = rect.x + INNER_CELL_PADDING + 10
                    rect.y = rect.y + INNER_CELL_PADDING
                    WINDOWS.blit(text,rect)
    
    #AI button
    aiMoveText = mediumFont.render("AI Move",True,BLACK)
    textRect = aiMoveText.get_rect(center = aiButton.center)
    pygame.draw.rect(WINDOWS,WHITE,aiButton)
    WINDOWS.blit(aiMoveText,textRect)

    #Reset Button
    resetText = mediumFont.render("Reset", True,BLACK)
    textRect = resetText.get_rect(center = resetButton.center)
    pygame.draw.rect(WINDOWS,WHITE,resetButton)
    WINDOWS.blit(resetText,textRect)

def getColor(num):
    
    if(num == 1):
        return BLUE
    elif (num == 2):
        return GREEN
    elif(num == 3):
        return RED
    else:
        return NAVY
        
def main():

    start = True
    while True:

        if start:

            game = Minesweeper.Minesweeper(cell_num_width, cell_num_height, mine_num)
            ai = Minesweeper.MinesweeperAI(cell_num_width, cell_num_height)
            grid = game.start()
            adjacent_mines = game.calculate_adjacent_mines()
            start = False
            
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.display.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                
                cell_x =  ((int)(mouse_pos[0] - padding)//cell_size)
                cell_y = ((int)((mouse_pos[1] - padding)//cell_size))

                print(ai.mines)
                if 0 <= cell_x < cell_num_width and 0 <= cell_y < cell_num_height:
                    if event.button == 1:
                        game.uncover_cell(cell_x, cell_y)
                        ai.mark_safe((cell_x,cell_y))
                        ai.moves_made.add((cell_x,cell_y))
                        ai.add_knowledge((cell_x,cell_y),adjacent_mines[cell_x][cell_y])
                   
                    elif event.button == 3:
                        game.flag_cell(cell_x ,cell_y )
                        ai.mark_mine((cell_x,cell_y))
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if aiButton.collidepoint(mouse_pos):
                            move = ai.make_safe_move()
                            if move == None:
                                print("The AI make a random move, because there is no safe moves left") 
                                move = ai.make_random_move()
                            else:
                                print("AI made a move: {}".format(move))
                            x,y = move
                            game.uncover_cell(x,y)
                            ai.add_knowledge(move,adjacent_mines[x][y])

                        elif resetButton.collidepoint(mouse_pos):
                            main()
        
        if cell_num - mine_num == game.covered_cell or lost:
            
            text = 'You Lost!' if lost else 'You Won!'
            text = largeFont.render(text,True, BLACK)
            textRect = pygame.Rect(boarder_width // 4, boarder_height// 2.5, 40,40)
            draw_grid(grid,adjacent_mines,game)
            WINDOWS.blit(text,textRect)
            pygame.display.flip()
            pygame.time.delay(5000)
            break

        draw_grid(grid,adjacent_mines,game)
        pygame.display.flip()
    
    pygame.display.quit()

if __name__ == "__main__":
    main()
