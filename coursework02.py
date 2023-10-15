from tkinter import Tk, Canvas, Button, Menu, PhotoImage
from tkinter import Entry, Label, simpledialog, Text
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
import random
from random import randint
import time
from time import sleep
import sys
import os
import operator


# Before starting the game please read 'Help' section
# Resolution is 1280x720
# Changes snake size when eating food and determines the level of the game
def growSnake():

	global score, pause, doTick, winImage
	
	lastElement = len(snake) - 1
	lastElementPos = canvas.coords(snake[lastElement])
	snake.append(canvas.create_rectangle(
						0, 0, snakeSize, 
						snakeSize, fill="brown"))

	# Determine direction of snake
	if (direction == "left"):
		canvas.coords(
				snake[lastElement + 1], 
				lastElementPos[0] + snakeSize, 
				lastElementPos[1], 
				lastElementPos[2] + snakeSize, 
				lastElementPos[3])
				
	elif (direction == "right"):
		canvas.coords(
				snake[lastElement + 1], 
				lastElementPos[0] - snakeSize, 
				lastElementPos[1], 
				lastElementPos[2] - snakeSize, 
				lastElementPos[3]) 
	elif (direction == "up"):
		canvas.coords(
				snake[lastElement + 1], 
				lastElementPos[0], 
				lastElementPos[1] + snakeSize, 
				lastElementPos[2], 
				lastElementPos[3] + snakeSize)
	else:
		canvas.coords(
				snake[lastElement + 1], 
				lastElementPos[0], 
				lastElementPos[1] - snakeSize, 
				lastElementPos[2], 
				lastElementPos[3] - snakeSize)
	
	# Keeps track of score
	score += 10
	txt = "Score:" + str(score)
	canvas.itemconfigure(scoreText, text=txt)

	# Places a new star after every 100 points
	if (score % 100 == 0):
		placeStar()

	# Places bonus mouse after every 70 points	
	if (score % 70 == 0):
		removeBonusFood()
		bonusFood()
	
	# Winner label pops up if stars > 6 (win)
	if (len(stars) == 6):
		gameOver = True
		label = Label(window, image=winImage)
		label.place(x=400, y=200)
		
		leaderboard()
		doTick = False
		pause = True

	# Determining the level
	# Level 1
	if (score < 50):
		canvas.create_text(
					70, 690, fill="white", 
					font="Times 20 italic bold", 
					text="Level 1", 
					tag="first")
					
		if (score % 3 == 0):
			placeObstacles()

	# Level 2
	elif (score > 50 and score < 100):
		canvas.delete("first")
		canvas.create_text(
					70, 690, fill="white", 
					font="Times 20 italic bold", 
					text="Level 2", 
					tag="second")
					
		if (score % 3 == 0):
			placeObstacles()

	# Level 3
	elif (score > 100 and score < 150):
		canvas.delete("second")
		canvas.create_text(
					70, 690, fill="white", 
					font="Times 20 italic bold", 
					text="Level 3", 
					tag="third")
					
		if (score % 4 == 0):
			placeObstacles()
			placeObstacles()

	# Level 4
	elif (score > 150 and score < 250):
		canvas.delete("third")
		canvas.create_text(
					70, 690, fill="white", 
					font="Times 20 italic bold", 
					text="Level 4", 
					tag="forth")
		
		if (score % 3 == 0):
			deleteObstacles()
			placeObstacles()

	# Level 5		
	elif (score > 250 and score < 400):
		canvas.delete("forth")
		canvas.create_text(
					70, 690, fill="white", 
					font="Times 20 italic bold", 
					text="Level 5", 
					tag="next")
					
		if (score % 4 == 0):
			deleteObstacles()
			placeObstacles()

	# Level 6 and above
	elif (score > 400):	
		if (score % 50 == 0):
			canvas.delete("next")
			canvas.create_text(
						70, 690, fill="white", 
						font="Times 20 italic bold", 
						text="Level 6+", 
						tag="next")	
			
			placeObstacles()
			
		if (score % 70 == 0):
			deleteObstacles()
			placeObstacles()
			placeObstacles()	


# Removes mouse after it is eaten
def removeBonusFood():

	global mouse, mouseX, mouseY

	mouseX = 1300
	mouseY = 800

	canvas.move(mouse, mouseX, mouseY)


# Randomly moves food on canvas	
def moveFood():

	global apple, foodX, foodY
	canvas.move(apple, (foodX*(-1)), (foodY*(-1)))

	foodX = random.randint(2, 36) * 30
	foodY = random.randint(2, 21) * 30
	
	canvas.move(apple, foodX, foodY)
	

# In case food is too hard to eat
def moveFoodObstacle(event):
	moveFood()


# Checks for collision with other objects
def overlapping(a, b):

	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False


# Checks for collision with apple
def overlappingFood(a, b):

	x = foodX + 17/2
	y = foodY + 17/2
	if a[0] - 17/2 < b[2] and x > b[0] and a[1] - 17/2 < b[3] and y > b[1]:
		return True
	return False


# Checks for collision with mouse
def overlappingMouse(a, b):

	x = mouseX + 30/2
	y = mouseY + 25/2
	if a[0] - 30/2 < b[2] and x > b[0] and a[1] - 25/2 < b[3] and y > b[1]:
		return True
	return False


# How snake moves; collision checks
def moveSnake():

	global pause, score, doTick, difficultyLevel

	canvas.pack()
	positions = []
	positions.append(canvas.coords(snake[0]))

	if pause is False:
		# Movement
		if direction == "left":
			canvas.move(snake[0], -snakeSize, 0)
		elif direction == "right":
			canvas.move(snake[0], snakeSize, 0)
		elif direction == "up":
			canvas.move(snake[0], 0, -snakeSize)
		elif direction == "down":
			canvas.move(snake[0], 0, snakeSize)

		# Gets coordinates of objects
		sHeadPos = canvas.coords(snake[0])
		foodPos = canvas.coords(apple)
		mousePos = canvas.coords(mouse)

		# Checks for collision with apple - snake grows and apple is randomly moved
		if overlappingFood(foodPos, sHeadPos):
			moveFood()
			growSnake()

		# Checks for collision with mouse - snake grows and mouse is removed	
		if overlappingMouse(mousePos, sHeadPos):
			growSnake()
			growSnake()
			removeBonusFood()

		# Checks for collision with an obstacle - if true game ends				
		for i in range(0, len(obstacles)):
			if overlapping(sHeadPos, canvas.coords(obstacles[i])):
				gameOver = True
				canvas.create_text(
							width / 2, height / 2, fill="white", 
							font="Times 20 italic bold", text="Game Over!")
				leaderboard()
				doTick = False

		# Checks for collision with itself - if true game ends
		for i in range(1, len(snake)):
			if overlapping(sHeadPos, canvas.coords(snake[i])):
				gameOver = True
				canvas.create_text(
							width / 2, height / 2, fill="white", 
							font="Times 20 italic bold", text="Game Over!")
				leaderboard()
				doTick = False
	
		# Checks for collision with walls - if true game ends
		listCoords = canvas.coords(snake[0])	
		if (
			listCoords[0] == 0 or listCoords[1] == 0 
			or listCoords[2] == 1275 or listCoords[3] == 720):
			
			gameOver = True
			canvas.create_text(
						width / 2, height / 2, fill="white", 
						font="Times 20 italic bold", text="Game Over!")
			leaderboard()
			doTick = False
				
		# Get the coordinates of the remaining elements	
		for i in range(1, len(snake)):
			positions.append(canvas.coords(snake[i]))
		for i in range(len(snake) - 1):
			canvas.coords(
					snake[i + 1], positions[i][0], 
					positions[i][1], positions[i][2], 
					positions[i][3])
		
		# Determines the speed of the snake - difficulty level
		if (difficultyLevel == "easy"):
			# Test that the snakeshead is moving correctly
			if 'gameOver' not in locals():
				window.after(70, moveSnake)
		
		elif (difficultyLevel == "medium"):
			if 'gameOver' not in locals():
				window.after(60, moveSnake)
		
		elif (difficultyLevel == "hard"):
			if 'gameOver' not in locals():
				window.after(55, moveSnake)
	
	
# Places stars for every 100 points 
def placeStar():

	global star, starX, starY, stars

	star = canvas.create_image(0, 0, image=starImage)

	starX = 1240 - 40 * len(stars)
	starY = 690 

	canvas.move(star, starX, starY)
	stars.append(star)

	return star, starX, starY, stars


# Randomply places the food on canvas
def placeFood():

	global apple, foodX, foodY

	apple = canvas.create_image(0, 0, image=appleFood)

	foodX = random.randint(2, 36) * 30
	foodY = random.randint(2, 21) * 30

	canvas.move(apple, foodX, foodY)


# Randomply places obstacles on canvas
def placeObstacles():   

	global obstacles, obstacleX, obstacleY

	for i in range(0, 1200, 400):
		obstacleX = random.randint(2, 36) * 30 - 15
		obstacleY = random.randint(2, 21) * 30 - 15
		size = 15
		
		obstacle = canvas.create_rectangle(
							obstacleX, obstacleY, obstacleX + size, 
							obstacleY + size, fill="black")

		obstacles.append(obstacle)


# Removes some of the obstacles	from playing field
def deleteObstacles():

	global obstacles, obstacleX, obstacleY

	obstacleX = 1300
	obstacleY = 800

	for i in range(len(obstacles) - 4, len(obstacles) - 1):
		canvas.move(obstacles[i], obstacleX, obstacleY)
	
	
# Adds a bonus food - mouse - on the field 		
def bonusFood():

	global mouse, mouseX, mouseY

	mouse = canvas.create_image(0, 0, image=mouseImage)

	mouseX = random.randint(2, 36) * 30
	mouseY = random.randint(2, 21) * 30

	canvas.move(mouse, mouseX, mouseY)


# Movement functions - left, right, up, down - when keys are pressed
def leftKey(event):

	global direction
	direction = "left"


def rightKey(event):

	global direction
	direction = "right"


def upKey(event):

	global direction
	direction = "up"


def downKey(event):

	global direction
	direction = "down"


# Pausing the gameplay	
def stop():

	global pause, pauseText, doTick
	doTick = False
	refreshLabel()
	pause = True
	moveSnake()
	pauseText = canvas.create_text(
					640, 360, fill="white", 
					font="Times 20 italic bold", text="GAME PAUSED!")
	return pause, pauseText


# Starting the gameplay
def start():

	global pause, pauseText, doTick
	doTick = True
	refreshLabel()
	pause = False
	canvas.delete(pauseText)
	moveSnake()
	return pause


# Resets the current game
def reset():

	python = sys.executable
	os.execl(python, python, * sys.argv)


# Cheat code 'CTRL + sss' 
# removes everything except head if length > 15
def onClick(event):

	global snake

	if (len(snake) > 15):
		i = len(snake) - 1
		while i > 0:
			canvas.delete(snake[i])
			del snake[i]		
			i = i - 1
	return snake


# Saves data from game in a file 
# Asks user for filename
def saveFile():

	global snake, obstacles, score, sHeadPos, stars, difficultyLevel

	sHeadPos = canvas.coords(snake[0])
	foodPos = canvas.coords(apple)
	mousePos = canvas.coords(mouse)

	file = asksaveasfile(mode='w', defaultextension=".txt")
	file.write(str(snake))
	file.write("  ")	
	file.write(str(score))
	file.write("  ")
	file.write(str(sHeadPos))
	file.write("  ")
	file.write(str(foodPos))
	file.write("  ")
	file.write(str(mousePos))
	file.write("  ")
	file.write(str(stars))
	file.write("  ")
	file.write(str(difficultyLevel))
	file.write("  ")
	
	for i in range(1, len(snake)):
		file.write(str(canvas.coords(snake[i])))
		file.write("  ")
		
	for i in range(0, len(obstacles)):
		file.write(str(canvas.coords(obstacles[i])))
		file.write("  ")


# Loads data from file - does not work 
def loadFile():

	fileOpened = askopenfile(mode='r', defaultextension=".txt")
	notYet = Toplevel(window)
	notYet.title("Load file")

	notYet.geometry('%dx%d+%d+%d' % (400, 40, 550, 550))
	
	label = Label(notYet, text="This feature is still work in progress...")
	label.pack()


# Writes data to file and shows leaderboard afterwards 
# reads it from the file called leaderboard.txt
def leaderboardShow():

	global newWindow, userName, button5, label

	textField = Text(newWindow)
	textField.insert(INSERT, userName.get())
	textField.insert(INSERT, " - ")
	textField.insert(INSERT, score)

	filename = "leaderboard.txt"
	with open(filename, "a") as f:
		text2 = str(textField.get(0.0, END))
		f.write(text2)
	
	userName.destroy()
	button5.destroy()
	label.destroy()

	# Showing leaderboard when user played the game, lost and entered the initials
	newWindow.geometry('%dx%d+%d+%d' % (200, 200, 550, 550))     # window size
	textField1 = Text(newWindow)
	textField1.pack()
	leaderboardData = []

	with open(filename, "r") as f:
		leaderboardData1 = f.read().split("\n")

		textField1.insert(INSERT, "Place  " + "  Name  " + "  Score" + '\n\n')

		# Information from the file turned into an array
		for i in range(len(leaderboardData1) - 1):
			leaderboardData1[i] = leaderboardData1[i].split(" - ")
			leaderboardData.append(leaderboardData1[i])

		# Turning results from file into integers so they can be sorted
		for i in range(len(leaderboardData)):
			leaderboardData[i][1] = int(leaderboardData[i][1])

		# Sorting results
		leaderboardData = sorted(
						leaderboardData, key=operator.itemgetter(1), 
						reverse=True
					)

		# Styling the leaderboard
		for i in range(len(leaderboardData)):
			leaderboardData[i] = str(leaderboardData[i]).strip('[]')
			leaderboardData[i] = leaderboardData[i].replace(',', '     ')
			leaderboardData[i] = leaderboardData[i].replace("'", " ")
			textField1.insert(
						INSERT, str(i + 1) + "        " 
						+ leaderboardData[i] + '\n')


# Connected to the menu option "Leaderboard". 
# User can only see the leaderboard.
def onlyShowLeaderboard():

	newWindowLeaderboard = Toplevel(window)
	newWindowLeaderboard.title("Leaderboard")

	newWindowLeaderboard.geometry('%dx%d+%d+%d' % (200, 200, 550, 550))
	textField1 = Text(newWindowLeaderboard)
	textField1.pack()
	leaderboardData = []

	with open("leaderboard.txt", "r") as f:
		leaderboardData1 = f.read().split("\n")

		textField1.insert(INSERT, "Place  " + "  Name  " + "  Score" + '\n\n')

		for i in range(len(leaderboardData1) - 1):
			leaderboardData1[i] = leaderboardData1[i].split(" - ")
			leaderboardData.append(leaderboardData1[i])

		for i in range(len(leaderboardData)):
			leaderboardData[i][1] = int(leaderboardData[i][1])
			
		leaderboardData = sorted(
						leaderboardData, key=operator.itemgetter(1), 
						reverse=True
					)

		for i in range(len(leaderboardData)):
			leaderboardData[i] = str(leaderboardData[i]).strip('[]')
			leaderboardData[i] = leaderboardData[i].replace(',', '     ')
			leaderboardData[i] = leaderboardData[i].replace("'", " ")
						
			textField1.insert(
						INSERT, str(i + 1) + "       " + leaderboardData[i] + '\n'
					)


# Asks user for initials in order to save result in leaderboard
def leaderboard():

	global newWindow, userName, button5, label

	newWindow = Toplevel(window)
	newWindow.title("Leaderboard")

	newWindow.geometry('%dx%d+%d+%d' % (200, 80, 550, 550))    # new window size

	label = Label(newWindow, text="Enter your initials in the box:")
	label.pack()

	userName = Entry(newWindow)
	userName.pack()

	button5 = Button(newWindow, text='Show leaderboard', command=leaderboardShow)
	button5.place(x=30, y=50)


# Boss key - picture comes up over window when "b" is pressed
def bossKey(event):

	global bossKey, button, button2, button3, menubar, pauseText, pause

	window.title("Oracle VM VirtualBox")
	bossKey = canvas.create_image(640, 360, image=bossKeyImage, tag="image")
	canvas.tag_raise(bossKey)
	button.destroy()
	button2.destroy()
	button3.destroy()
	menubar.destroy()
	
	if pause is False:
		stop()
	canvas.delete(pauseText)


# Buttons for pause, start, restart
def buttons():
	
	global button, button2, button3
	
	button = Button(window, text='Pause', command=stop)
	button.place(x=450, y=670)

	button2 = Button(window, text='Start', command=start)
	button2.place(x=600, y=670)

	button3 = Button(window, text='Reset', command=reset)
	button3.place(x=735, y=670)


# Exiting boss key and resuming the game - press 'e'
def exitBossKey(event):

	canvas.delete(bossKey)
	window.title("Snake Game")
	buttons()
	menu()	
	stop()


# New difficulty saved and shown on canvas
def saveDifficulty():
	global difficultyControl, newDifficulty, difficultyLevel
	
	difficultyLevel = newDifficulty.get()
	canvas.itemconfigure(
				difficulty, text="Difficulty: " + difficultyLevel, 
				font="Times 20 italic bold", fill="white")
				
	difficultyControl.destroy()
	
	return difficultyLevel, difficultyLevel


# Takes user choice for difficulty level
def changeKeyDifficulty():
	
	global difficultyControl, newDifficulty
	
	difficultyControl = Tk()
	difficultyControl.title("Change of difficulty")
	difficultyControl.geometry("300x100")    # new window size
	
	upInput = Label(
			difficultyControl, 
			text="Choose difficulty: easy, medium or hard")
	upInput.pack()
	
	newDifficulty = Entry(difficultyControl)  
	newDifficulty.pack()
	
	difficultyButtton = Button(
					difficultyControl, text='Save difficulty', 
					command=saveDifficulty)
	difficultyButtton.pack()


# Saves user input for new controls in controls.txt 
# overwrites old controls stored in file
def saveControls():

	global windowControls, e1, e2, e3, e4
	
	textField = Text(windowControls)
	textField.insert(INSERT, e1.get())
	textField.insert(INSERT, " ")
	textField.insert(INSERT, e2.get())
	textField.insert(INSERT, " ")
	textField.insert(INSERT, e3.get())
	textField.insert(INSERT, " ")
	textField.insert(INSERT, e4.get())
	
	filename1 = "controls.txt"
	with open(filename1, "w") as f:
		text2 = str(textField.get(0.0, END))
		f.write(text2)
		
	with open(filename1, "r") as f:
		saveControlsInput = f.read().split(" ")	
		
	keyControls()	
	windowControls.destroy()	


# Asks user for new controls - all fields should be filled
def changeKeyControls():

	global windowControls, e1, e2, e3, e4, buttonControls
	
	windowControls = Tk()
	windowControls.title("Change of snake movement controls")
	windowControls.geometry("400x300")    # new window size
	
	upInput = Label(windowControls, text="Movement up")
	upInput.pack()
	e1 = Entry(windowControls)  
	e1.pack()
	
	downInput = Label(windowControls, text="Movement down")
	downInput.pack()
	e2 = Entry(windowControls)
	e2.pack()
	
	leftInput = Label(windowControls, text="Movement left")
	leftInput.pack()
	e3 = Entry(windowControls)
	e3.pack()
	
	rightInput = Label(windowControls, text="Movement right")
	rightInput.pack()
	e4 = Entry(windowControls)
	e4.pack()
	
	buttonControls = Button(
				windowControls, text='Save controls', 
				command=saveControls)
	buttonControls.pack()
	
	labelControls = Label(
				windowControls, 
				text="\nAll fields should be filled!" 
				+ "\nIf you want to use arrows please type: Up, Down, Left, Right.\n")
	labelControls.pack()
	
	
# Help menu - information about the game
# Reads in from file called help.txt
def instructions():

	instrWindow = Tk()
	instrWindow.title("Help")
	instrWindow.geometry("800x450")    # new window size
	
	with open("help.txt", "r") as f:
		instr = f.read().split("\n")
		
	movement = Label(instrWindow, text=instr[0] + "\n")
	movement.pack()
	
	txtInstr = instr[1].split("  ")
	bosskey = Label(instrWindow, text=txtInstr[0] + "\n" + txtInstr[1] + "\n")
	bosskey.pack()
	
	txtInstr = instr[2].split("  ")
	cheatCode = Label(instrWindow, text=txtInstr[0] + "\n" + txtInstr[1] + "\n")
	cheatCode.pack()
	
	appleFood = Label(instrWindow, text=instr[3] + "\n")
	appleFood.pack()
	
	mouseFood = Label(instrWindow, text=instr[4] + "\n")
	mouseFood.pack()
	
	txtInstr = instr[5].split("  ")
	obstacles = Label(instrWindow, text=txtInstr[0] + "\n" + txtInstr[1] + "\n")
	obstacles.pack()
	
	txtInstr = instr[6].split("  ")
	walls = Label(instrWindow, text=txtInstr[0] + "\n" + txtInstr[1] + "\n")
	walls.pack()
	
	txtInstr = instr[7].split("  ")
	stars = Label(instrWindow, text=txtInstr[0] + "\n" + txtInstr[1] + "\n")
	stars.pack()
	
	stars = Label(instrWindow, text=instr[8] + "\n")
	stars.pack()
	
	
# Menu shown - options for the user to choose from
def menu():

	global menubar
	
	menubar = Menu(window)

	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=loadFile)
	filemenu.add_command(label="Save", command=saveFile)
	filemenu.add_command(label="Control settings", command=changeKeyControls)
	filemenu.add_command(label="Difficulty settings", command=changeKeyDifficulty)
	filemenu.add_command(label="Leaderboard", command=onlyShowLeaderboard)
	filemenu.add_command(label="Help", command=instructions)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=window.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	window.config(menu=menubar)
	
	
# Keys for controlling the snake movements
# reads them from file called controls.txt
def keyControls():

	with open("controls.txt", "r") as f:
		saveControlsInput = f.read().split(" ")
		
	key = []
	for i in range(0, len(saveControlsInput)):
		key.append(saveControlsInput[i])
		
	canvas.bind("<" + str(key[0]) + ">", upKey)
	canvas.bind("<" + str(key[1]) + ">", downKey)
	canvas.bind("<" + str(key[2]) + ">", leftKey)
	canvas.bind("<" + str(key[3]) + ">", rightKey)
	canvas.focus_set()


# Refreshing timer constantly
def refreshLabel():

	global s, m, h, doTick

	if doTick is True:
		canvas.itemconfigure(
					timer, text="Time played: " + "%s:%s:%s" % (h, m, s), 
					fill="white")

		s += 1
		if (s == 60):
			m += 1
			s = 0
		elif (m == 60):
			h += 1
			m = 0

		# After 1 second, call refreshLabel again (start an infinite recursive loop)
		window.after(1000, refreshLabel)


def startGame():

	global pause, pauseText, doTick, buttonStart
	
	doTick = True
	refreshLabel()
	pause = False
	moveSnake()
	buttonStart.destroy()
	
	return pause


# Setting window dimensions and name
def setWindowDimensions(w, h):

	window = Tk()                     # create window
	window.title("Snake Game")        # title of window
	
	ws = window.winfo_screenwidth()   # computers screen size
	hs = window.winfo_screenheight()
	
	x = (ws/2) - (w/2)                # calculate center
	y = (hs/2) - (h/2)
	
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))    # window size
	return window


width = 1280    # width of snake’s world
height = 720   # height of snake’s world

window = setWindowDimensions(width, height)

canvas = Canvas(window, bg="#008000", width=width, height=height) 

snake = []      # create snake
snakeSize = 15

# Used for starting and pausing the game
pause = True
buttonStart = Button(
				window, text='START GAME', 
				command=startGame)
buttonStart.place(x=600, y=350)

# Create snake head
snake.append(canvas.create_rectangle(
					snakeSize, snakeSize, snakeSize * 2, 
					snakeSize * 2, fill="#800000"))

# Keeping track of the score
score = 0
txt = "Score:" + str(score)
scoreText = canvas.create_text(
					width / 2, 15, fill="white", 
					font="Times 20 italic bold", text=txt)

# Keys for using boss key and cheat code
canvas.bind("<Control-Triple-s>", onClick)
canvas.bind("<b>", bossKey)
canvas.bind("<e>", exitBossKey)
canvas.bind("<m>", moveFoodObstacle)
canvas.focus_set()
direction = "right"
keyControls()

# Buttons menu
buttons()

# Array of obstacles
obstacles = []

# Array of stars
stars = []

# variable storing time
s = 0
m = 0
h = 0

timer = canvas.create_text(
				1150, 20, text="Time played: " + "%s:%s:%s" % (h, m, s), 
				font="Times 20 italic bold", fill="white")
doTick = False
refreshLabel()

# Difficulty level - easy, medium, hard
difficultyLevel = "easy"

difficulty = canvas.create_text(
				120, 20, text="Difficulty: " + difficultyLevel, 
				font="Times 20 italic bold", fill="white")

# Images used in game
appleFood = PhotoImage(file="apple.png")
mouseImage = PhotoImage(file="mouse.png")
bossKeyImage = PhotoImage(file="screen.png")
starImage = PhotoImage(file="star.png")
winImage = PhotoImage(file="winner.png")
	
# Create a pulldown menu, and add it to the menu bar
menu()

# Calling functions here
bonusFood()
placeObstacles()
placeFood()
moveSnake()

window.mainloop()
