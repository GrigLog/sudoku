from pprint import pprint
from copy import deepcopy


class WrongInputError(Exception):
	pass


class SudokuSolver:
	def __init__(self, board):
		self.board = deepcopy(board)
		self.map = [[set(range(1, 10)) for i in range(9)] for i2 in range(9)]
		show(self.board)

	def solve(self, main=True):
		if main:
			if not self.pre_check():
				return False
		while self.clear():
			continue
		if self.check_completed():
			return self.board
		if self.check_problem():
			return False
		# pprint(self.map)
		weak = self.find_weakest()
		for e in list(self.map[weak[1]][weak[2]]):
			new_board = deepcopy(self.board)
			new_board[weak[1]][weak[2]] = e
			# pprint(new_board)
			s = SudokuSolver(new_board)
			res = s.solve(False)
			if res:
				return res
		return False

	def find_weakest(self):
		mn = (9, 0, 0)
		for y in range(9):
			for x in range(9):
				if self.board[y][x] == 0 and len(self.map[y][x]) < mn[0]:
					mn = (len(self.map[y][x]), y, x)
		return mn

	def get_raw(self, y, x):
		return set(self.board[y])

	def get_column(self, y, x):
		return set(map(lambda e: e[x], self.board))

	def get_square(self, y, x):
		arr = list(map(lambda e: e[x // 3 * 3: x // 3 * 3 + 3], self.board[y // 3 * 3: y // 3 * 3 + 3]))
		return set(arr[0] + arr[1] + arr[2])

	def clear(self):
		efficient = False
		for y in range(9):
			for x in range(9):
				if self.board[y][x] == 0:  # empty cell
					self.map[y][x] -= (self.get_raw(y, x) | self.get_column(y, x) | self.get_square(y, x))  # update map
					if len(self.map[y][x]) == 0:
						return False
					if len(self.map[y][x]) == 1:
						self.board[y][x] = list(self.map[y][x])[0]
						efficient = True
				else:  # something is already here
					self.map[y][x] = {self.board[y][x]}
		# show(self.board)
		# pprint(self.map)
		# print()
		return efficient  # any cell was filled

	def check_completed(self):
		return all(map(lambda e: all(e), self.board))

	def check_problem(self):
		for e in self.map:
			for e2 in e:
				if len(e2) == 0:  # cell cant be filled
					return True
		return False

	def pre_check(self):
		for n in range(1, 10):
			for i in range(9):
				if self.board[i].count(n) > 1:  # raws
					return False
				if list(map(lambda e: e[i], self.board)).count(n) > 1:  # columns
					return False
			for y in range(3):
				for x in range(3):
					arr = list(map(lambda e: e[x * 3: x * 3 + 3], self.board[y * 3: y * 3 + 3]))
					if (arr[0] + arr[1] + arr[2]).count(n) > 1:
						return False
		return True


def show(arr):
	for e in arr:
		for e2 in e:
			if e2 != 0:
				print(e2, end=' ')
			else:
				print(' ', end=' ')
		print()
	print()


def main():
	try:
		board = [list(map(lambda e: int(e), input().split())) for i in range(9)]
		s = SudokuSolver(board)
		res = s.solve()
		if res:
			print('Solution exists:')
			show(res)
		else:
			print("No solutions.")
	except WrongInputError:
		print("No solutions.")
	except Exception:
		print("Wrong data input.")
	input()





'''
0 0 9 0 8 1 0 0 0
0 7 0 2 0 0 0 4 0
0 5 0 0 0 3 0 0 0
0 3 0 0 6 0 4 0 9
0 0 8 0 0 0 0 0 2
0 0 0 0 0 9 0 0 0
4 0 0 6 0 0 0 1 0
0 0 0 4 0 0 0 8 7
0 0 0 0 0 0 0 5 0
'''
'''
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0
'''