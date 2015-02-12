import pygame
import random
pygame.init()

BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# --- Classes ---
class Virus(pygame.sprite.Sprite):
	
	def __init__(self):
		super(Virus, self).__init__()
		
		self.image = pygame.image.load("virus.png").convert()
		self.rect = self.image.get_rect()
	
	def reset_pos(self):
		# Reset pos to the top of the screen, at random x location.
		# Called by update() or the main program loop if there is a collision.
		self.rect.y = random.randrange(-300, -20)
		self.rect.x = random.randrange(0, SCREEN_WIDTH)
		
	def update(self):
		""" Called each frame. """
		
		# Move virus down one pixel
		self.rect.y += 1
		
		if self.rect.y > SCREEN_HEIGHT:
			self.reset_pos()

class Player(pygame.sprite.Sprite):
	# Player class #
	
	# Set speed vectors
	change_x = 0
	change_y = 0
	
	def __init__(self):
		super(Player, self).__init__()
		
		self.image = pygame.image.load("nano_warrior.png").convert()
		self.image.set_colorkey(BLACK)
		
		# make colliding rect sliiightly smaller
		self.rect = self.image.get_rect().inflate(-2, -2)
		
		self.rect.x = SCREEN_WIDTH/2
		self.rect.y = SCREEN_HEIGHT/2
	
	def changespeed(self, x, y):
		self.change_x += x
		self.change_y += y
	
	def update(self):
		self.rect.x += self.change_x
		self.rect.y += self.change_y
		
class Laser(pygame.sprite.Sprite):
	def __init__(self):
		super(Laser, self).__init__()
		
		self.image = pygame.Surface([3, 9])
		self.image.fill((0,221,255))
		
		self.rect = self.image.get_rect().inflate(2,2)
	
	def update(self):
		# Move the LAZOR
		self.rect.y -= 3

class Monster(pygame.sprite.Sprite):
	change_x = 4
	
	def __init__(self):
		super(Monster, self).__init__()
		
		self.image = pygame.image.load("monster.png").convert()
		self.rect = self.image.get_rect().inflate(-3, -3)
		
	def reset_pos(self):
		self.rect.y = random.randrange(-300, -20)
		self.rect.x = random.randrange(0, SCREEN_WIDTH)
		
	def update(self):
		self.rect.y += 3
		
		if self.rect.y > SCREEN_HEIGHT:
			self.reset_pos()
			
		self.rect.x += self.change_x
		
		if self.rect.x > SCREEN_WIDTH:
			self.change_x *= -1
		elif self.rect.x < 0:
			self.change_x *= -1
		
#~ def endscreen():
	#~ all_sprites_list.empty()
	#~ player.kill()
	#~ virus_list.empty()
	#~ screen.blit(gameover_disp, (270, 200))


def main():
	BLACK = (0, 0, 0)
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	game = True
	
	def endscreen():
		all_sprites_list.empty()
		player.kill()
		virus_list.empty()
		screen.blit(gameover_disp, (270, 200))

	size = (SCREEN_WIDTH, SCREEN_HEIGHT)
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("NANO WARRIOR")
		
	bg = pygame.image.load("nano_world.png").convert()

	scorefont = pygame.font.SysFont("monospace", 22)
	gameover = pygame.font.SysFont("monospace", 50, True)

	# --- Sound 
	
	laser_sound = pygame.mixer.Sound("laser.ogg")
	pygame.mixer.music.load("NTD11.mp3")
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.mixer.music.play()
	
	# --- Game stuff ---
	#game = True

	clock = pygame.time.Clock()
	
	pygame.mouse.set_visible(False)
	
	virus_list = pygame.sprite.Group()
	
	all_sprites_list = pygame.sprite.Group()
	
	laser_list = pygame.sprite.Group()
	
	monster_list = pygame.sprite.Group()
	
	# Create all the virus enemies
	for i in range(200):
		
		virus = Virus()
		
		virus.rect.x = random.randrange(SCREEN_WIDTH)
		virus.rect.y = random.randrange(-620, -20)
		
		virus_list.add(virus)
		all_sprites_list.add(virus)
		
		virus.image.set_colorkey(BLACK)
	
	for i in range(8):
		
		monster = Monster()
		
		monster.rect.x = random.randrange(SCREEN_WIDTH)
		
		monster.rect.y = random.randrange(-620, -20)
		monster_list.add(monster)
		all_sprites_list.add(monster)
		
		monster.image.set_colorkey(BLACK)
		
	
	# Create player
	player = Player()
	all_sprites_list.add(player)
	
	score = 0
	
	gameover_disp = gameover.render("GAME OVER", 1, (255, 255, 40))
	do_endscreen = False
	
	replay = False
	
	while game:
		# --- Main event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game = False
				
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_SPACE and not do_endscreen:
					laser = Laser()
					laser_sound.play()
					
					laser.rect.x = player.rect.x
					laser.rect.y = player.rect.y
					
					all_sprites_list.add(laser)
					laser_list.add(laser)
					
				elif event.key == pygame.K_a and not do_endscreen:
					player.changespeed(-2, 0)
				elif event.key == pygame.K_d and not do_endscreen:
					player.changespeed(2, 0)
				elif event.key == pygame.K_w and not do_endscreen:
					player.changespeed(0, -2)
				elif event.key == pygame.K_s and not do_endscreen:
					player.changespeed(0, 2)
					
				elif (event.key == pygame.K_RETURN) or (event.key == pygame.K_ESCAPE) and do_endscreen:
					game = False
				
				elif event.key == (pygame.K_r):
					game = False
					replay = True
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a and not do_endscreen:
					player.changespeed(2, 0)
				elif event.key == pygame.K_d and not do_endscreen:
					player.changespeed(-2, 0)
				elif event.key == pygame.K_w and not do_endscreen:
					player.changespeed(0, 2)
				elif event.key == pygame.K_s and not do_endscreen:
					player.changespeed(0, -2)
				
			
		
		# --- Game logic
		
		# Calls update() on every sprite
		all_sprites_list.update()
		score_disp = scorefont.render("Score: " + str(score), 1, (255, 255, 20))
		
		
		for laser in laser_list:
			
			# See if it hit a virus
			
			virus_hit_list = pygame.sprite.spritecollide(laser, virus_list, True)
			
			for virus in virus_hit_list:
				laser_list.remove(laser)
				all_sprites_list.remove(laser)
				score += 1
				
			if laser.rect.y < -10:
				laser_list.remove(laser)
				all_sprites_list.remove(laser)
				
		for virus in virus_list:
			player_hit_list = pygame.sprite.spritecollide(player, virus_list, False)
			
			if player_hit_list:
				do_endscreen = True
				
		if monster_list:
			for monster in monster_list:
				player_hit_list = pygame.sprite.spritecollide(player, monster_list, False)
			
				if player_hit_list:
					do_endscreen = True
				
		
		# --- Drawing code
		
		screen.blit(bg, [0, 0])
		
		screen.blit(score_disp, (100, 20))
		
		if do_endscreen:
			endscreen()
		
		
		
		# Draws all sprites
		all_sprites_list.draw(screen)
		
		pygame.display.flip()
		
		# --- Limit to 60 fps
		clock.tick(60)
	return replay

if __name__=="__main__":
	game_again = True
	while game_again:
		game_again = main()
	
pygame.quit()
