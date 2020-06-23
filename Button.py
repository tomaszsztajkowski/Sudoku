import constants as con
import pygame

class Button():
	def __init__(self, color, coor, size, number, locked=False):
		self.color = color
		self.x = 10 + (size + 2) * coor[0]
		self.y = 10 + (size + 2) * coor[1]
		self.size = size
		self.number = number
		self.locked = locked
		self.mark = set()


	def draw(self, win):
		pygame.draw.rect(win, con.BLACK, (self.x-2, self.y-2, self.size+4, self.size+4), 0)
		pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 0)
		
		if self.number[0] != 0:
			font = pygame.font.SysFont('Calibri', self.size - 10, bold= True if self.locked else False)
			text = font.render(str(self.number[0]), 1, con.BLACK)
			win.blit(text, (self.x + (self.size//2 - text.get_width()//2 - 1), self.y + (self.size//2 - text.get_height()//2 + 2)))

		if self.mark:
			for i in list(self.mark):
				font = pygame.font.SysFont('Calibri', int((self.size - 10) / 2.5))
				text = font.render(str(i), 1, con.BLACK)
				win.blit(text, (self.x + (i-1)%3 * (self.size//3 + 3) + 1, self.y + (i-1)//3 * (self.size//3 + 1)))

	def is_over(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.size:
			if pos[1] > self.y and pos[1] < self.y + self.size:
				return True
		return False