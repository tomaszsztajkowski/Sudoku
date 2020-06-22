with open('hard.txt', 'r') as f:
	puzzles = f.read().split('\n\n')

with open('hard.txt', 'w') as f:
	for i in puzzles:
		f.write(i+'\n')