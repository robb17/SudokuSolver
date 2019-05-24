import sys
from copy import deepcopy

''' generate sudoku boards:
		Fill in a board correctly and randomly k times
		While there is more than 1 valid solution:
			Find all possible solutions (terminate upon finding a position that can accept all 9 values)
			Assign a value to the position that can accept the most values
'''


class Board:
	def __init__(self, boardlst):
		self.board = boardlst
		self.size = len(boardlst[0])

	def all_valid_values(self, coordinate):
		values = []
		for item in range(1, self.size + 1):
			if self._is_valid(coordinate, item):
				values.append(item)
		return values

	def _is_valid(self, coordinate, value):
		return self._valid_for_row(coordinate[0], value) \
				and self._valid_for_column(coordinate[1], value) \
				and self._valid_for_region((coordinate[0] // 3) * 3, \
						(coordinate[1] // 3) * 3, value)

	def _valid_for_row(self, x, item):
		for y in range(0, self.size):
			if self.board[x][y] == item:
				return False
		return True

	def _valid_for_column(self, y, item):
		for x in range(0, self.size):
			if self.board[x][y] == item:
				return False
		return True

	def _valid_for_region(self, x, y, item):
		for x_index in range(x, x + 3):
			for y_index in range(y, y + 3):
				if self.board[x_index][y_index] == item:
					return False
		return True

	def is_marked(self, coordinate):
		return not self.board[coordinate[0]][coordinate[1]] == 0

	def mark(self, coordinate, value):
		self.board[coordinate[0]][coordinate[1]] = value

	def is_solved(self):
		for x in range(0, self.size):
			for y in range(0, self.size):
				if self.board[x][y] == 0:
					return False
		return True

	def print(self):
		for x in range(0, self.size):
			print(self.board[x])

''' Not needed, but implemented for fun
'''
#class Coordinate():
#	def __init__(self, pair):
#		self.coordinate = pair
#
#	def __hash__(self):
#		return self.coordinate[0] * 10 + self.coordinate[1]
#
#	def __getitem__(self, key):
#		return self.coordinate[key]
#
#	def __repr__(self):
#		return "(" + str(self.coordinate[0]) + ", " + str(self.coordinate[1]) + ")"

def solve_by_constraint(board):
	unsolved_tiles = 0
	unsolved_coordinates = []
	for x in range(0, board.size):
		for y in range(0, board.size):
			if board.is_marked((x, y)):
				continue
			valid_moves = board.all_valid_values((x, y))
			if len(valid_moves) == 1:
				board.mark((x, y), valid_moves[0])
			else:
				unsolved_tiles += 1
				unsolved_coordinates.append((x, y))
	return (unsolved_tiles, unsolved_coordinates)

def parse_board_as_text(board_file):
	board = []
	for line in board_file.readlines():
		row = line.split(" ")
		for x in range(0, len(row)):
			row[x] = int(row[x][0])
		if not len(row) == 9:
			board = []
			break
		board.append(row)
	if not len(board) == 9:
		print("Error: malformed board")
		exit()
	return board

def recursive_solver(board):
	''' Solve via solve_by_constraint until a guess is needed, then
		make a guess and push the new board onto the stack
	'''
	unsolved_tiles = float("inf")
	unsolved_coordinates = []
	while True:
		new_n_unsolved_tiles, unsolved_coordinates = solve_by_constraint(board)
		if new_n_unsolved_tiles == unsolved_tiles:
			break
		unsolved_tiles = new_n_unsolved_tiles
	if not len(unsolved_coordinates) == 0:
		guess_coordinate = min(unsolved_coordinates, \
				key = lambda x: len(board.all_valid_values(x)))	# pick the most contrained variable
		for value in board.all_valid_values(guess_coordinate):
			guess_board = deepcopy(board)
			guess_board.mark(guess_coordinate, value)
			guess_board = recursive_solver(guess_board)
			if guess_board.is_solved():
				board = guess_board
				break
	return board

def main():
	if not len(sys.argv) == 2:
		print("Usage: python3 sudoku.py board")
		exit()

	board_filename = sys.argv[1]
	board_file = open(board_filename, "r")

	input_board = parse_board_as_text(board_file)

	board = Board(input_board)

	board = recursive_solver(board)

	if board.is_solved():
		board.print()
	else:
		print("Unsolvable board")

if __name__ == "__main__":
    main()