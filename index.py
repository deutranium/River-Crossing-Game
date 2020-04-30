import pygame as pg
import random
import time
from config import *


win = pg.display.set_mode((win_width, win_height))
key_enable = True


clock = pg.time.Clock()
start_time = pg.time.get_ticks()

all_sprites = pg.sprite.Group()
obstacle_group = pg.sprite.Group()
mobs = pg.sprite.Group()
poppp = pg.sprite.Group()
mobs = pg.sprite.Group()




# the popup windows
class Popup(pg.sprite.Sprite):
	def __init__(self, pos, width, height, color, alpha, text, win_text, \
		*groups):
		super().__init__(*groups)
		
		self.image = pg.Surface((width, height))
		self.image.set_alpha(alpha)
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.text = text
		self.font = pg.font.Font('freesansbold.ttf', 35)
		self.text_image = self.font.render(text, True, (0, 0, 0))
		self.text_rect = self.text_image.get_rect(center=((240, 150)))
		self.image.blit(self.text_image, self.text_rect)
		
		self.text_restart_image = self.font.render(win_text, True, (0, 0, 0))
		self.text_restart_rect = self.text_image.get_rect(center=(240, 300))
		self.image.blit(self.text_restart_image, self.text_restart_rect)
		
		self.rect.center = pos



# PLAYER
# the player sprite
class Player(pg.sprite.Sprite):
	def __init__(self, pos, img, *groups):
		super().__init__(*groups)
		self.image = pg.transform.scale(pg.image.load(img), (40, 60))
		self.rect = self.image.get_rect(center=pos)


# OBSTACLES
# Make stationary obstacles
class Obstacle(pg.sprite.Sprite):
	def __init__(self, pos, *groups):
		super().__init__(*groups)
		self.image = pg.transform.scale(pg.image.load('danger.png'), (40, 50))
		self.rect = self.image.get_rect(center=pos)

# Make moving obstacles
class Move_obstacle(pg.sprite.Sprite):
	def __init__(self, pos, *groups):
		super().__init__(*groups)
		self.image = pg.transform.scale(pg.image.load('happy.png'), (50, 50))
		self.rect= self.image.get_rect(center=pos)


# FUNCTIONS FOR COMPUTING

# calculate the score of the player
def calculate_score(y, one_or_two):
	global score, y_score_1
	
	if one_or_two == 1:
		for i in y_score_1:
			if i[0] >= y:
				score[0] = i[1]

	elif one_or_two == 2:
		for i in y_score_2:
			if i[0] <= y:
				score[1] = i[1]

# display player's score
def display_score(player):
	text_font = pg.font.Font('freesansbold.ttf', 25)
	text = "Scores: " + str(score[0]) + " - " + str(score[1])

	text_image = text_font.render(text, False, (0, 10, 20))
	win.blit(text_image, (10,20))

# display the player number on screen
def display_player():
	text_font = pg.font.Font('freesansbold.ttf', 25)
	text = "Current Player: " + str(player_no)

	text_image = text_font.render(text, False, (0, 10, 20))
	win.blit(text_image, (10,50))

# display current level on screen
def display_level():
	text_font = pg.font.Font('freesansbold.ttf', 25)
	text = "Level: " + str(level)

	text_image = text_font.render(text, False, (0, 10, 20))
	win.blit(text_image, (10,90))

def display_time():
	text_font = pg.font.Font('freesansbold.ttf', 25)
	text = "Time: " + str(cur_time)

	text_image = text_font.render(text, False, (0, 10, 20))
	win.blit(text_image, (800,40))

# move the obstacles
def move_obstacle(speed):
	global mobs
	mobs = pg.sprite.Group()
	for i in range(6):
		Move_obstacle((xArr[i], yArr[i]), mobs)
		xArr[i] = (xArr[i] + speed) % win_width if key_enable else xArr[i]
	return mobs



# draw the rivers
def drawRiver():
	for i in range(5):
		pg.draw.rect(win, blue, (0, i  * 120 + 160, win_width, 60))


# add the obstacle to the screen
def addObstacle(y):
	global obstacle_group
	rand_numbers = random.sample(range(1, (win_width - 64)//50), 2)
	obst1 = Obstacle((rand_numbers[0]*50, y))
	obst2 = Obstacle((rand_numbers[1]*50, y))
	obstacle_group.add(obst1, obst2)

# show the popup for end game
def show_popup(meh):

	global popup_end
	if(score[0] > score[1]):
		popup_end = Popup((540, 425), 500, 500, red, 255, 'Your score is ' \
			+ str(score[player_no-1]) + '!', "Player 1 wins", poppp)
	elif(score[0] < score[1]):
		popup_end = Popup((540, 425), 500, 500, red, 255, 'Your score is ' \
			+ str(score[player_no-1]) + '!', "Player 2 wins", poppp)
	else:
		popup_end = Popup((540, 425), 500, 500, red, 255, 'Your score is ' \
			+ str(score[player_no-1]) + '!', "It's a draw!", poppp)

	if not meh:
		popup_end = Popup((540, 425), 500, 500, red, 255, 'Game ended!!!', \
			"It's a draw!", poppp)
		print("tada!")

	disable_keys()
	poppp.draw(win)

# disable the keys when game ends
def disable_keys():
	global key_enable, dx, dy
	key_enable = 0
	dx = 0
	dy = 0


player = Player((x, y), 'player1.png', all_sprites)


# main game loop
def main():	

	# make the variables global
	global obstacle_group, key_enable, x, y, dx, dy, player, score, \
	popup_end, player, player_no, speed, level, cur_time
	final_score = score[0]

	popup_cover = Popup((540, 425), win_width, win_height, translucent, \
		128, '', '', poppp)
	

	# add obstacle to the screen
	tada = False
	for i in range(6):
		addObstacle(i * 2 * 60 + 130)

	# add the obstacles to all_sprites group
	all_sprites.add(obstacle_group)

	while not tada:
		pg.draw.rect(win, blue, (20, 30, 100, 100))
		k = pg.key.get_pressed()

		# increase the speed depending on the level
		speed = 10 + 10 * level
		cur_time = pg.time.get_ticks() - start_time
		cur_time = str(round((cur_time % 60000)/1000))

		# Check boundary conditions
		# Check left and right condition
		if(x < 32 or x > win_width - 32):
			if key_enable:
				if(x < 32):
					dx = speed if k[pg.K_RIGHT] else 0
				else:
					dx = -speed if k[pg.K_LEFT] else 0

				# if the player is at the vertical boundaries too
				if y >= 50 and y < win_height - 50:
					dy = speed if k[pg.K_DOWN] else (-speed if k[pg.K_UP] else 0)

			# check the exit condition
			for e in pg.event.get():
				if e.type == pg.QUIT:
					tada = True


		# Check top and bottom condition
		if(y < 50 or y >= win_height - 50):
			if key_enable:
				if(y < 50):
					dy = speed if k[pg.K_DOWN] else 0
				else:
					dy = -speed if k[pg.K_UP] else 0

				# if the player is at the horizotal boundaries too
				if x >= 32 and x < win_width - 32:
					dx = speed if k[pg.K_RIGHT] else (-speed if k[pg.K_LEFT] \
						else 0)

			# check the exit condition
			for e in pg.event.get():
				if e.type == pg.QUIT:
					tada = True


		# if not at boundary
		else:
			for e in pg.event.get():
				k = pg.key.get_pressed()
				
				# exit condition
				if e.type == pg.QUIT:
					tada = True

				elif key_enable:
					# horizontal movement
					if k[pg.K_LEFT]:
						dx = -speed
					elif k[pg.K_RIGHT]:
						dx = speed
					else:
						dx = 0
					# vertical movement
					if k[pg.K_UP]:
						dy = -speed
					elif k[pg.K_DOWN]:
						dy = speed
					else:
						dy = 0

		# update the coordinates of the player
		x += dx
		y += dy
		

		player.rect.center = (x, y)


		all_sprites.update()
		# Check which enemies collided with the player.
		# spritecollide returns a list of the collided sprites.
		collided_stationary_enemies = pg.sprite.spritecollide(player, \
			obstacle_group, False)
		collided_moving_enemies = pg.sprite.spritecollide(player, mobs, \
			False)


		# change player 1 to 2 when player one reaches the finish line
		if(y < 100 and player_no == 1):
			player_no = 2
			player.kill()
			player = Player((win_width/2, y), 'player2.png', all_sprites)

		# change player 2 to 1 when player two reaches the finish line
		elif(y > 700 and player_no == 2):
			player_no = 1
			player.kill()
			player = Player((win_width/2, y), 'player1.png', all_sprites)
			level += 1
			if level == 3:
				show_popup(0)
		

		# update the screen
		win.fill(green)
		drawRiver()
		all_sprites.draw(win)
		move_obstacle(speed//3).draw(win)
		calculate_score(y, player_no)
		display_score(player_no)
		display_player()
		display_level()
		display_time()

		# check collisions with the stationary enemies
		for enemy in collided_stationary_enemies:
			# Draw rects around the collided enemies.
			pg.draw.rect(win, (0, 190, 120), enemy.rect, 4)
			if player_no == 2:
				show_popup(1)
			else:
				player_no = 1
				player.kill()
				y = 30
				x = win_width/2
				player = Player((x, y), 'player2.png', all_sprites)
				all_sprites.draw(win)

		# check the collisions with the moving enemies
		for enemy in collided_moving_enemies:
			# Draw rects around the collided enemies.
			pg.draw.rect(win, (255, 250, 120), enemy.rect, 4)
			if player_no == 2:
				show_popup(1)
			else:
				player_no = 1
				player.kill()
				y = 30
				x = win_width/2
				player = Player((x, y), 'player2.png', all_sprites)
				all_sprites.draw(win)



		pg.display.flip()
		clock.tick(30)

pg.init()
main()
pg.quit()
quit()

# all the images are a copyright of Mario Bros
