import pygame
import sudoku
from random import randint


class button():
    def __init__(self, color, coor, size, number, outline, fontsize, locked = False, outline_size = 4):
        self.color = color
        self.x = 10 + (size + 2) * coor[0]
        self.y = 10 + (size + 2) * coor[1]
        self.width = self.height = size
        self.number = number
        self.outline = outline
        self.fontsize = fontsize
        self.locked = locked
        self.os = outline_size

    def draw(self, win):
        #Call this method to draw the button on the screen
        if self.outline:
            pygame.draw.rect(win, self.outline, (self.x-self.os//2, self.y-self.os//2, self.width+self.os, self.height+self.os), 0)
        if self.color:
        	pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.number[0] != 0:
            font = pygame.font.SysFont('Calibri', self.fontsize, bold= True if self.locked else False)
            text = font.render(str(self.number[0]), 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2 - 1), self.y + (self.height/2 - text.get_height()/2 + 2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


def display():
	screen.fill((255, 255, 255))
	for tile in tiles: tile.draw(screen)
	for i in range(4): pygame.draw.line(screen, (0, 0, 0), (8, 8 + i*(tile_size+2)*3), ((tile_size+3)*9, 8 + i*(tile_size+2)*3), 4)
	for i in range(4): pygame.draw.line(screen, (0, 0, 0), (8 + i*(tile_size+2)*3, 8), (8 + i*(tile_size+2)*3, (tile_size+3)*9), 4)
	pygame.display.update()

def display_errors():
	for i in range(81):
		if not current.validate_target(i): tiles[i].color = (255, 200, 200) 
		else: tiles[i].color = (255, 255, 255)
	if chosen_tile: chosen_tile.color = (chosen_tile.color[0]- 50, chosen_tile.color[1] - 50, chosen_tile.color[2])

pygame.init()

with open('puzzles.txt', 'r') as f:
	puzzles = f.read().split('\n')


# choice = puzzles.pop(randint(0, len(puzzles)-1))
choice = '000000000000003085001020000000507000004000100090000000500000073002010000000040009' # the worst case scenario
# choice = '530070000600195000098000060800060003400803001700020006060000280000419005000080079'

current = sudoku.Sudoku(choice)
# solved = sudoku.Sudoku(choice)
# solved.solve_backtracking()

chosen_tile = None

tile_size = 60
tiles = []
for i in range(9):
	for j in range(9):
		tiles.append(button((255, 255, 255), (j, i), tile_size, current.board[i][j], (0, 0, 0), tile_size - 10, current.board[i][j][0] != 0))


screen = pygame.display.set_mode(((tile_size+2)*9 + 20, (tile_size+2)*9 + 20))
pygame.display.set_caption('Sudoku')
pygame.display.set_icon(pygame.image.load('icon.png'))

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				display_errors()

				mouse_pos = pygame.mouse.get_pos()
				for i in range(81):
					if tiles[i].locked != True and tiles[i].isOver(mouse_pos):
						if chosen_tile: chosen_tile.color = (chosen_tile.color[0] + 50, chosen_tile.color[1] + 50, chosen_tile.color[2])
						chosen_tile = tiles[i]
						chosen_tile.color = (chosen_tile.color[0]- 50, chosen_tile.color[1] - 50, chosen_tile.color[2])
						break

		if event.type == pygame.KEYDOWN:
			key = chr(event.key)
			if chosen_tile and key in '1234567890':
				chosen_tile.number[0] = int(key)

			if key == ' ':
				for tile in tiles:
					if not tile.locked: tile.number[0] = 0
				current.solve_backtracking(functions=[display])
			display_errors()
    	
	display()
	
