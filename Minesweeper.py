import random

class Minesweeper:
    
    
    def __init__(self, width,height, mine):
        
        self.height = height 
        self.width = width 
        self.mine_num= mine
        self.covered_cell = 0

        self.mines = set()
        
        while len(self.mines) != self.mine_num:

            i = random.randint(0,width - 1)
            j = random.randint(0,height - 1)
            
            if (i,j) not in self.mines:
                
                self.mines.add((i,j))
    
        self.mines_num = self.calculate_adjacent_mines()
    
    def is_mine(self, cell):
        
        i,j = cell
        return (i,j) in self.mines

    
    def calculate_adjacent_mines(self):
        
        mines_num = [] 
        for i in range(self.width):
            row = []
            
            for j in range(self.height):
                
                row.append(0)
            mines_num.append(row)        
        
        for i in range(self.width):
            
            for j in range( self.height):
                
                if(i,j) in self.mines: mines_num[i][j] = -9
                for di in [-1, 0, 1]: 
                
                    for dj in [-1, 0, 1]:  
                    
                        ni, nj = i + di, j + dj
                    
                        if(ni == i and nj == j): continue
                        if 0 <= ni < self.width and 0 <= nj < self.height:
                            
                            if (ni,nj) in self.mines:
                               mines_num[i][j] += 1
        
        return mines_num
    
    def uncover_cell(self, cell_x, cell_y):   
        
        if self.grid[cell_x][cell_y] == 'flag' or self.grid[cell_x][cell_y] == 'uncovered': return
        self.grid[cell_x][cell_y] = 'uncovered'
        self.covered_cell += 1

    def flag_cell(self,cell_x,cell_y):
        
        if self.grid[cell_x][cell_y] == 'uncovered': return
        self.grid[cell_x][cell_y] = 'flag'
        
        
    def start(self):
        
        self.grid = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append('covered')
            self.grid.append(row)
        return self.grid


class Sentence():
    
    def __init__(self,cells, count):
        
        self.cells = set(cells)
        self.count = count
    
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def known_mines(self):
        
        if len(self.cells)== self.count: return self.cells 
        
        return set()
       
    
    def known_safes(self):

        if self.count == 0: return self.cells
        return set()
        
    def mark_mine(self,cell):
        
        if cell not in self.cells: return
        
        self.cells.remove(cell)
        self.count -= 1
        
    def mark_safe(self,cell):
        
        if cell not in self.cells: return
        
        self.cells.remove(cell)



class MinesweeperAI():
    
    def __init__(self,width, heigth):
        
        self.height = heigth
        self.width = width
        
        self.moves_made = set() #keeping the of which cells have been clicked on
        
        self.mines = set() #keeping the track of mine cells
        self.safes = set() #keeping the track of safe cells
        self.flagged = set() #keeping the track of flaged cells
        self.knowledge = [] #list of sentences about the game to be true
    
    def mark_mine(self,cell):
        
        self.mines.add(cell)
        
        for sentence in self.knowledge:
            
            sentence.mark_mine(cell)
            self.mines.add(cell)
    
    def mark_safe(self,cell):
        
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            self.safes.add(cell)
             
    def add_knowledge(self,cell,count):
        
        self.moves_made.add(cell)
        self.mark_safe(cell)

        for sentence in self.knowledge:
            
            sentence.mark_safe(cell)
        
        cells = set()
        x,y = cell 
        for di in [-1,0,1]:
            for dj in [-1,0,1]:

                dx = x + di
                dy = y+ dj

                if (dx == x and dy ==y or (dx >= self.width or dy >= self.height or dx < 0 or dy <0)): continue
                
                if ( (dx,dy) in self.safes):
                    self.safes.add((dx,dy))  
                elif((dx,dy) in self.mines):
                    count -= 1
                    self.mines.add((dx,dy))
                else:
                    cells.add((dx,dy))             
        
        if count == 0:
            self.safes = self.safes.union(cells)

        for sentence in self.knowledge:
            
            if cells.issubset(sentence.cells):
                
                new_cell = sentence.cells -  cells
                new_count = sentence.count - count
            
                self.knowledge.append(Sentence(new_cell,new_count))
                self.knowledge.remove(sentence)
            
            elif sentence.cells.issubset(cells):
                
                new_cell = cells - sentence.cells
                new_count = count - sentence.count
                
                self.knowledge.append(Sentence(new_cell,new_count))
                self.knowledge.remove(sentence)
        
        for sentence in self.knowledge:
            if sentence is None: 
                self.knowledge.remove(sentence)
                continue
            self.safes = self.safes.union(sentence.known_safes())
            self.mines = self.mines.union(sentence.known_mines())    
        self.knowledge.append(Sentence(cells,count))

    def make_random_move(self):
        
        move = set()
        
        while len(move) != 1:
            
            i = random.randint(0,self.width- 1)
            j = random.randint(0,self.height - 1)

            cell = (i,j)
            
            if cell in self.mines or cell in self.moves_made: continue
            
            move.add(cell)
        return move.pop() 
    
    def make_safe_move(self):
        
        newSet = self.safes - self.moves_made
        if(len(newSet) == 0):
            return None
        return newSet.pop()
    
