import colors as color
import constants as c
import pygame
from random import randint
from time import time
from tile import SudokuTile
from sudoku import Sudoku

def display(tile_size, window, tiles):
	# BACKGROUND
	window.fill(color.WHITE)
	rect_size = tile_size * 9 + c.thin*6 + c.thick*4
	rect = (c.border, c.border, rect_size, rect_size)
	pygame.draw.rect(window, color.BLACK, rect)

	# TILES
	for tile in tiles:
		tile.draw(tile_size, window)

	pygame.display.update()

def new_sudoku(level):
	difficulty = {pygame.K_q: 'novice', pygame.K_w: 'intermediate', pygame.K_e: 'expert'}
	with open('puzzles\\' + difficulty[level] + '.txt', 'r') as f:
		data = f.read().split('\n')[randint(0, 49)]
	title = difficulty[level].title()
	pygame.display.set_icon(pygame.image.load('icons\\' + difficulty[level] + '.png'))
	sudoku = Sudoku(data)
	tiles = [SudokuTile((i % 9, i // 9), color.WHITE, d) for i, d in enumerate(sudoku.data)]
	return sudoku, tiles, title

def clear_sudoku(tiles):
	for tile in tiles:
		if not tile.lock:
			tile.marks = set()
			tile.number[0] = 0
		tile.color = color.WHITE

def main(tile_size = 60):
	pygame.init()

	win_size_x = tile_size * 9 + c.border*2 + c.thin*6 + c.thick*4
	win_size_y = tile_size * 9 + c.border*2 + c.thin*6 + c.thick*4
	window = pygame.display.set_mode((win_size_x, win_size_y))
	chosen_tile = None
	index = -1
	time_passed = 0
	clock = time()
	skip = 0
	skip_threshold = 0
	solving = False
	# gameboard
	sudoku, tiles, title = new_sudoku(pygame.K_q)

	test = 0

	running = True
	while running:
		########### EVENTS ###########
		for event in pygame.event.get():
			###### when trying to close the window #######
			if event.type == pygame.QUIT:
				running = False
				break

			###### when moving the cursor ######
			elif event.type == pygame.MOUSEMOTION:
				pos = pygame.mouse.get_pos()
				coor = None
				for tile in tiles:
					coor = tile.draw(tile_size, window, pos)
					if coor: break

			####### when clicking a mouse button ######
			elif not solving and event.type == pygame.MOUSEBUTTONDOWN:
				if not coor or tiles[coor[1]*9 + coor[0]].lock: continue

				##### number input mode #####
				### regular mode ###
				if coor and event.button == 1:
					if chosen_tile: chosen_tile.color = color.WHITE
					chosen_tile = tiles[coor[1]*9 + coor[0]]
					chosen_tile.color = color.BLUE
				### marking mode ###
				elif coor and event.button == 3:
					if chosen_tile: chosen_tile.color = color.WHITE
					chosen_tile = tiles[coor[1]*9 + coor[0]]
					chosen_tile.color = color.GREEN

			###### when pressing a key ######
			elif event.type == pygame.KEYDOWN:
				### '0' to '9' ###
				if not solving and chosen_tile and ord('0')  <= event.key <= ord('9'):
					
					##### number input #####
					### regular mode ###
					if chosen_tile.color == color.BLUE:
						chosen_tile.marks = set()
						if chosen_tile.number[0] == int(chr(event.key)):
							chosen_tile.number[0] = 0

						else:
							chosen_tile.number[0] = int(chr(event.key))

					### marking mode ###
					if chosen_tile.color == color.GREEN:
						chosen_tile.number[0] = 0
						if int(chr(event.key)) == 0:
							chosen_tile.marks = set()

						elif int(chr(event.key)) in chosen_tile.marks:
							chosen_tile.marks.remove(int(chr(event.key)))

						else:
							chosen_tile.marks.add(int(chr(event.key)))

				### spacebar ###
				elif event.key == pygame.K_SPACE:
					clear_sudoku(tiles)
					if index >= 0:
						index = -1
						solving = False
						skip = 0
					else:
						solving = True
						chosent_tile = None
						index = 0

				### 'q', 'w', 'e' ###
				elif event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
					sudoku, tiles, title = new_sudoku(event.key)
					clock = time()
					time_passed = 0
					index = -1
					solving = False
					skip = skip_threshold = 0
					
				### '=' ###
				elif solving and event.key == pygame.K_EQUALS:
					if skip_threshold == 0: skip_threshold = 1
					else: skip_threshold *= 2

				### '-' ###
				elif solving and event.key == pygame.K_MINUS:
					skip = 0
					skip_threshold //= 2

				### esc ###
				elif not solving and event.key == pygame.K_ESCAPE:
					clear_sudoku(tiles)

		########### SOLVING THRESHOLD ###########
		if solving and index == 81:
			solving = False
			skip = 0

		########### SOLVING ###########
		elif index >= 0:
			# print(index // 9 * 9 + index % 9)
			while index < 81 and tiles[index].lock:
				tiles[index].color = color.GREEN_SOLVE
				index += 1
			if index < 81 and sudoku.solve_backtracking_step(index):
				for tile in tiles:
					if tile.color == color.RED_SOLVE:
						tile.color = color.WHITE
				tiles[index].color = color.GREEN_SOLVE
				index += 1
			elif index < 81:
				tiles[index].color = color.RED_SOLVE
				index -= 1
				while index < 81 and tiles[index].lock:
					tiles[index].color = color.RED_SOLVE
					index -= 1

		########### DISPLAY AND SKIPPING ###########
		if not solving or skip == skip_threshold:
			display(tile_size, window, tiles)
			skip = 0
			print(index)
		else: skip += 1

		########### WINDOW CAPTION ###########
		if index == -1:
			time_passed = int(time() - clock)
			time_passed = ' {}:{}'.format(time_passed//60, str(time_passed-(time_passed//60)*60).rjust(2, '0'))
			pygame.display.set_caption(title + ' sudoku' + time_passed)
		elif index == 81:
			pygame.display.set_caption(title + ' sudoku' + ' solved')
		else:
			skipping = ' | skipping ' + str(skip_threshold) + ' frame' + ('s' if skip_threshold > 1 else '') if skip_threshold != 0 else ''
			pygame.display.set_caption(title + ' sudoku' + ' solving' + skipping)

		test += 1
if __name__ == '__main__': main()
