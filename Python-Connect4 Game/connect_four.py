import turtle
from random import randint

class Board:

	def __init__(self, max_x = 10, max_y = 10, w = 500, h = 700):
		self.max_x = max_x
		self.max_y = max_y
		self.h = h
		self.w = w
		self.r1 = (8 * self.w) / (10 * 2 * self.max_x)
		self.grid = [[0 for i in range(self.max_y)] for j in range(self.max_x)] 
		self.graph = Graphics(self.w, self.h)
		self.slotX = -1

	def isValid(self, x, y):
		if(x < 0 or x >= self.max_x):
			return 0
		if(y < 0 or y >= self.max_y):
			return 0
		return 1

	def getEmptySlot(self, x):
		ans = -1
		y = 0
		while(self.isValid(x, y) and ans == -1):
			if(self.grid[x][y] == 0):
				ans = y
			y = y + 1
		return ans

	def checkWin(self, last_x, last_y):
		dirx = [0, 1, 1, 1, 0, -1, -1, -1]
		diry = [1, 1, 0, -1, -1, -1, 0, 1]
		diag1 = 1
		diag2 = 1
		horiz = 1
		vert = 1
		for i in range(8):
			j = 1
			while(self.isValid(last_x + j * dirx[i], last_y + j * diry[i]) and self.grid[last_x + j * dirx[i]][last_y + j * diry[i]] == self.grid[last_x][last_y]):
				if (i == 0 or i == 4):
					vert = vert + 1
				elif (i == 1 or i == 5):
					diag1 = diag1 + 1
				elif (i == 2 or i == 6):
					horiz = horiz + 1
				elif (i == 3 or i == 7):
					diag2 = diag2 + 1
				j = j + 1
		if(diag1 >= 4 or diag2 >= 4 or horiz >= 4 or vert >= 4):
			return 1
		return 0

	def drawBoard(self):
		for i in range(self.max_x):
			for j in range(self.max_y):
				self.graph.drawCircle(self.w/10 + (2*i + 1) * self.r1, self.h/10 + (2*j + 1) * self.r1, self.r1 - 1, 'white')
				self.graph.screen.update()

	def getSlotX(self, x, y):
		pt_x = x 
		pt_x = pt_x - (self.w/10)
		if((pt_x//self.r1) % 2 == 0):
			self.slotX = (pt_x//self.r1)/2
		else:
			self.slotX = ((pt_x//self.r1) - 1)/2

	def getActualX(self, x):
		return self.w/10 + (2*x + 1) * self.r1

	def getActualY(self, y):
		return self.h/10 + (2*y + 1) * self.r1

class Graphics:

	def __init__(self, width, height):
		self.screen = turtle.Screen()
		self.screen.screensize(width, height, 'blue')
		self.screen.setworldcoordinates(0, 0, width, height)
		self.screen.tracer(0)

	def drawCircle(self, x, y, r, color):
		turt = turtle.Turtle()
		turt.hideturtle()
		turt.width(1)
		turt.penup()
		turt.goto(x, y)
		turt.pendown()
		turt.fillcolor(color)
		turt.begin_fill()
		turt.speed(0)
		turt.circle(r)
		turt.end_fill()

	def dropPuck(self, height, x, y, last_x, last_y, r, color):
		turt = turtle.Turtle()
		turt.hideturtle()
		turt.width(1)
		turt.speed(0)
		turt.penup()
		turt.goto(x, height)
		turt.speed(0)
		self.screen.tracer(0)
		while(turt.ycor() >= y):
			turt.clear()
			turt.fillcolor(color)
			turt.begin_fill()
			turt.circle(r)
			turt.end_fill()
			self.screen.update()
			tx = turt.xcor()
			ty = turt.ycor()
			turt.right(90)
			turt.forward(10)
			turt.left(90)
		turt.clear()
		self.drawCircle(tx, y, r, color)

	def writeText(self, x, y, str, turt, color, sz):
		turt.clear()
		turt.color(color)
		turt.speed(0)
		turt.penup()
		turt.goto(x, y)
		turt.pendown()
		turtle.hideturtle()
		turt.write(str, align = 'center', font = ('courier', sz, 'bold',  'italic'))


class Game:

	def __init__(self, max_x = 10, max_y = 10, w = 500, h = 700, play_AI = 0):
		self.max_x = max_x
		self.max_y = max_y
		self.h = h
		self.w = w
		self.board = Board(self.max_x, self.max_y, self.w, self.h)
		self.turn = 1
		self.turt = turtle.Turtle()
		self.red_score_turtle = turtle.Turtle()
		self.yellow_score_turtle = turtle.Turtle()
		self.turt.hideturtle()
		self.red_score = 0
		self.yellow_score = 0
		self.readFile()
		self.play_AI = play_AI

	def readFile(self):
		try:
			f = open('scores.txt', 'r')
			self.red_score, self.yellow_score = [int(x) for x in next(f).split()]
			f.close()
		except:
			print('Game running first time')

	def writeFile(self):
		f = open('scores.txt', 'w')
		f.write(str(self.red_score) + ' ' + str(self.yellow_score))
		f.close()

	def play_turn(self, x, y):
		if(self.play_AI == 1 and self.turn == 2):
			last_x = randint(0, self.max_x - 1)
		else:
			self.board.getSlotX(x, y)
			print(x, y, self.board.slotX)
			last_x = int(self.board.slotX)

		if(last_x < 0):
			last_x = 0
		if(last_x >= self.max_x):
			last_x = self.max_x - 1
		last_y = self.board.getEmptySlot(last_x)
		if(last_y == -1):
			self.board.graph.writeText(250, 600, 'That column is full, please choose again', self.turt, 'yellow', 15)
			return 

		print(last_x, last_y)
		win = 0
		if(self.turn == 2):
			self.board.graph.dropPuck(self.board.h, self.board.getActualX(last_x), self.board.getActualY(last_y), last_x, last_y, self.board.r1 - 1, 'yellow')
			self.board.graph.writeText(250, 600, 'Red Turn, please choose slot', self.turt, 'red', 25)
		else:
			self.board.graph.dropPuck(self.board.h, self.board.getActualX(last_x), self.board.getActualY(last_y), last_x, last_y, self.board.r1 - 1, 'red')
			self.board.graph.writeText(250, 600, 'Yellow Turn, please choose slot', self.turt, 'yellow', 25)

		self.board.grid[last_x][last_y] = self.turn

		if(self.board.checkWin(last_x, last_y)):
			win = 1
			if(self.turn == 2):
				self.yellow_score = self.yellow_score + 1
				self.board.graph.writeText(250, 600, 'Yellow Wins! Click to play again', self.turt, 'yellow', 25)
			else:
				self.red_score = self.red_score + 1
				self.board.graph.writeText(250, 600, 'Red Wins! Click to play again', self.turt, 'Red', 25)
			self.board.graph.screen.onscreenclick(None)
			self.board.graph.screen.onscreenclick(self.play_game)
			self.writeFile()

		self.turn = 3 - self.turn
		if(self.turn == 2 and self.play_AI == 1 and win == 0):
			self.play_turn(0, 0)


	def play_game(self, *args):
		self.turn = 1
		self.board.graph.screen.clearscreen()
		self.board = Board(self.max_x, self.max_y, self.w, self.h)
		self.board.drawBoard()
		self.board.graph.writeText(250, 550, 'Red Score: ' + str(self.red_score), self.red_score_turtle, 'red', 15)
		self.board.graph.writeText(250, 525, 'Yellow Score: ' + str(self.yellow_score), self.yellow_score_turtle, 'yellow', 15)
		self.board.graph.writeText(250, 600, 'Red Turn, please choose slot', self.turt, 'red', 25)
		self.board.graph.screen.onscreenclick(self.play_turn)
		self.board.graph.screen.mainloop()

def new_game(*args):
	print('Enter board rows: ')
	rows = int(input())
	print('Enter board columns: ')
	cols = int(input())
	print('Do you want to play against random AI?(y/n): ')
	choice = input()
	if(choice == 'y'):
		play_AI = 1
	else:
		play_AI = 0
	game = Game(cols, rows, 500, 700, play_AI)
	game.play_game()

new_game()

