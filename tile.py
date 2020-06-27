import pygame
import colors as color
import constants as c

class SudokuTile():
	def __init__(self, coordinates, color, number):
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.color = color
		self.number = number
		if number[0] == 0: self.lock = False
		else: self.lock = True
		self.marks = set()

	def draw(self, size, window, coordinates=None):
		x = c.border + c.thick * (1 + self.x // 3) + c.thin * (self.x % 9 - self.x // 3) + size * self.x
		y = c.border + c.thick * (1 + self.y // 3) + c.thin * (self.y % 9 - self.y // 3) + size * self.y
		if coordinates:
			if abs(x - coordinates[0]) <= 60 and coordinates[0] > c.border + c.thick:
				if abs(y - coordinates[1]) <= 60 and coordinates[1] > c.border + c.thick:
					return (self.x, self.y)
			return None

		pygame.draw.rect(window, self.color, (x, y, size, size))

		if self.marks:
			font = pygame.font.SysFont('Calibri', (size - 10) // 3 + 2)
			for number in list(self.marks):
				text = font.render(str(number), 1, color.BLACK)
				x_text = x + ((size // 3) * ((number-1) % 3 + 1)) - size // 6 - (text.get_width() // 2) - 1
				y_text = y + ((size // 3) * ((number-1) // 3 + 1)) - size // 6 - (text.get_height() // 2)
				window.blit(text, (x_text, y_text))

		elif self.number[0] != 0:
			font = pygame.font.SysFont('Calibri', size - 10, bold= True if self.lock else False)
			text = font.render(str(self.number[0]), 1, color.BLACK)
			x_text = x + size//2 - (text.get_width() // 2) - 1
			y_text = y + size//2 - (text.get_height() // 2) + 2
			window.blit(text, (x_text, y_text))
