sqr_indexes = {str(i // 3) + str(i % 3): i for i in range(9)}           # dictionary for square indexes keys: '00' to '22', values: 0 to 8

class Sudoku:
    def __init__(self, data = None):
        if data: self.data = [[int(i)] for i in data]                               # convert string data to indexed pointers
        else: self.data = [[0] for i in range(81)]                                  # if no data is provided makes an empty board

        self.board = [[self.data[i*9 + j] for j in range(9)] for i in range(9)]     # 9x9 matrix of pointers from data

        self.board_t = list(map(list, zip(*self.board)))                            # matrix with the same pointers as in board but transposed

        self.board_sqr = [list() for i in range(9)]                                 # matrix with the same pointers as in board but arranged into squares like in sudoku
        for i in range(81):
            self.board_sqr[sqr_indexes[str((i//9) // 3) + str((i%9) // 3)]].append(self.data[i])


    def validate_target(self, index):
        boards = [self.board, self.board_t, self.board_sqr]                                             # regular, transposed, squares
        indexes = [index//9, index%9, sqr_indexes[str((index//9) // 3) + str((index%9) // 3)]]          # regular, transposed, squares

        for b, i in zip(boards , indexes):
            check = {r: False for r in range(1, 10)}

            for n in b[i]:
                if n[0] == 0: continue
                if check[n[0]] == True: return False
                else: check[n[0]] = True

        return True


    counter = 0
    delay = 1
    def solve_backtracking(self, index= 0, events= None, display= None):
        if events:                                                                          # this if and the one below are used for displaying
            e = events()                                                                    # the number on screen while solving the sudoku
            if e == True: return True                                                       # nothing to do with the solving itself
            elif type(e) == int:
                self.delay += e
                if self.delay < 1: self.delay = 1

        if display:                                                                         # 'the one below'
            if self.counter == self.delay:
                        display()
                        self.counter = 0
            else: self.counter += 1

        if self.board[index//9][index%9][0] != 0:                                           # handles prefilled numbers
            if index == 80: return True                                                     # -||-
            return self.solve_backtracking(index + 1, events=events, display=display)       # -||-
        
        while True:
            self.board[index//9][index%9][0] += 1                                           # adds 1 to the number in the current position
            if self.board[index//9][index%9][0] > 9:                                        # backtracking system, if there are no numbers left:
                self.board[index//9][index%9][0] = 0                                        #  resets previously changed numbers
                return False                                                                #  returns wrong number flag
            if not self.validate_target(index): continue                                    # validity check
            if index == 80: return True                                                      # if reached the end of sudoku returns completion flag
            if self.solve_backtracking(index + 1, events=events, display=display) == True: return True  # recursion
