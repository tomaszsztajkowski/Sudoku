sqr_indexes = {str(i // 3) + str(i % 3): i for i in range(9)}           # dictionary for square indexes keys: '00' to '22', values: 0 to 8

class Sudoku:
    def __init__(self, data=None):
        # convert string data to indexed pointers
        if data: self.data = [[int(i)] for i in data]
        # if no data is provided makes an empty board
        else: self.data = [[0] for i in range(81)]

        # 9x9 matrix of pointers from data
        self.board = [[self.data[i*9 + j] for j in range(9)] for i in range(9)]

        # matrix with the same pointers as in board but transposed
        self.board_t = list(map(list, zip(*self.board)))

        # matrix with the same pointers as in board but arranged into squares like in sudoku
        self.board_sqr = [list() for i in range(9)]
        for i in range(81):
            self.board_sqr[sqr_indexes[str((i//9) // 3) + str((i%9) // 3)]].append(self.data[i])


    def validate_target(self, index):
                # 0: regular  1: transposed 2: squares
        boards = [self.board, self.board_t, self.board_sqr]
        indexes = [index//9, index%9, sqr_indexes[str((index//9) // 3) + str((index%9) // 3)]]

        for b, i in zip(boards , indexes):
            check = {r: False for r in range(1, 10)}

            for n in b[i]:
                if n[0] == 0: continue
                if check[n[0]] == True: return False
                else: check[n[0]] = True

        return True

    def solve_backtracking_step(self, index):
        # looking for a legal number
    	while self.data[index][0] < 9:
    		self.data[index][0] += 1
    		if self.validate_target(index):
    			return True

        # no number fits the spot -> backtrack
    	self.data[index][0] = 0
    	return False
