import pygame
import sudoku
from random import randint



class button():
	def __init__(self, color, coor, size, number, locked = False):
		self.color = color
		self.x = 10 + (size + 2) * coor[0]
		self.y = 10 + (size + 2) * coor[1]
		self.size = size
		self.number = number
		self.locked = locked
		self.mark = set()


	def draw(self, win):
		pygame.draw.rect(win, (0,0,0), (self.x-2, self.y-2, self.size+4, self.size+4), 0)
		pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 0)
		
		if self.number[0] != 0:
			font = pygame.font.SysFont('Calibri', self.size - 10, bold= True if self.locked else False)
			text = font.render(str(self.number[0]), 1, (0,0,0))
			win.blit(text, (self.x + (self.size//2 - text.get_width()//2 - 1), self.y + (self.size//2 - text.get_height()//2 + 2)))

		if self.mark:
			for i in list(self.mark):
				font = pygame.font.SysFont('Calibri', int((self.size - 10) / 2.5))
				text = font.render(str(i), 1, (0,0,0))
				win.blit(text, (self.x + (i-1)%3 * (self.size//3 + 3) + 1, self.y + (i-1)//3 * (self.size//3 + 1)))

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.size:
			if pos[1] > self.y and pos[1] < self.y + self.size:
				return True
		return False


def display_errors(sud, tiles, chosen_tile):
	for i in range(81):
		if not sud.validate_target(i): tiles[i].color = (255, 200, 200) 
		else: tiles[i].color = (255, 255, 255)
	if chosen_tile: chosen_tile.color = (chosen_tile.color[0]- 50, chosen_tile.color[1] - 50, chosen_tile.color[2])


def event_handler():											# used for displaying numbers while solving the sudoku
	for event in pygame.event.get():								# ensures that pygame window events are handled so that
		if event.type == pygame.KEYDOWN:							# no window freeze can occur
			if event.key == pygame.K_EQUALS:  return 10				# changes the speed of displaying
			elif event.key == pygame.K_MINUS: return -10
			return True
	return False

def new_sudoku(code, tile_size):
	sud = sudoku.Sudoku(code)
	tiles = []
	for i in range(81):
		tiles.append(button((255, 255, 255), (i%9, i//9), tile_size, sud.data[i], sud.data[i][0] != 0))
	return (sud, tiles)



def main():
	def display():
		screen.fill((255, 255, 255))
		for tile in tiles: tile.draw(screen)
		for i in range(4): pygame.draw.line(screen, (0, 0, 0), (8, 8 + i*(tile_size+2)*3), ((tile_size+3)*9, 8 + i*(tile_size+2)*3), 4)
		for i in range(4): pygame.draw.line(screen, (0, 0, 0), (8 + i*(tile_size+2)*3, 8), (8 + i*(tile_size+2)*3, (tile_size+3)*9), 4)
		pygame.display.update()

	pygame.init()
	tile_size = 60																			# change if you want to make the window bigger
	screen = pygame.display.set_mode(((tile_size+2)*9 + 20, (tile_size+2)*9 + 20))
	pygame.display.set_caption('Sudoku')
	pygame.display.set_icon(pygame.image.load('icon.png'))

	# code = '000000000000003085001020000000507000004000100090000000500000073002010000000040009' # the worst case scenario
	code = '530070000600195000098000060800060003400803001700020006060000280000419005000080079' # wikipedia example

	board, tiles = new_sudoku(code, tile_size)
	
	chosen_tile = None
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					display_errors(board, tiles, chosen_tile)

					mouse_pos = pygame.mouse.get_pos()
					for i in range(81):
						if tiles[i].locked != True and tiles[i].isOver(mouse_pos):
							if chosen_tile: chosen_tile.color = (chosen_tile.color[0] + 50, chosen_tile.color[1] + 50, chosen_tile.color[2])
							chosen_tile = tiles[i]
							chosen_tile.color = (chosen_tile.color[0]- 50, chosen_tile.color[1] - 50, chosen_tile.color[2])
							break

			if event.type == pygame.KEYDOWN:
				if chosen_tile and chr(event.key).isnumeric():
					if pygame.key.get_mods() in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT):
						chosen_tile.number[0] = 0
						if int(chr(event.key)) == 0: chosen_tile.mark = set()
						elif int(chr(event.key)) in chosen_tile.mark: chosen_tile.mark.remove(int(chr(event.key)))
						else: chosen_tile.mark.add(int(chr(event.key))) 
					else:
						chosen_tile.mark = set()
						if chosen_tile.number[0] == int(chr(event.key)): chosen_tile.number[0] = 0
						else: chosen_tile.number[0] = int(chr(event.key))

				elif event.key == pygame.K_SPACE:
					for tile in tiles:
						if not tile.locked:
							tile.number[0] = 0
							tile.mark = set()

					chosen_tile = []
					display_errors(board, tiles, chosen_tile)
					if pygame.key.get_mods() in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT):
						board.solve_backtracking()
					else: board.solve_backtracking(display = display, events = event_handler)

				elif event.key == pygame.K_ESCAPE:
					for tile in tiles:
						if not tile.locked: tile.number[0] = 0

				elif event.key == pygame.K_q:
					with open('easy.txt', 'r') as f:
						code = f.read().split('\n')[randint(0, 49)]
					board, tiles = new_sudoku(code, tile_size)

				elif event.key == pygame.K_w:
					with open('medium.txt', 'r') as f:
						code = f.read().split('\n')[randint(0, 49)]
					board, tiles = new_sudoku(code, tile_size)

				elif event.key == pygame.K_e:
					with open('hard.txt', 'r') as f:
						code = f.read().split('\n')[randint(0, 49)]
					board, tiles = new_sudoku(code, tile_size)

				display_errors(board, tiles, chosen_tile)

		display()
	
main()