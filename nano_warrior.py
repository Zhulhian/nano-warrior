import pygame
import random
pygame.init()


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
		# Move virus down
		# Öka 2 för att få fiender att flyga ned fortare, och vice verse
		self.rect.y += 2
		
		# Om de åker längst ned så reset:ar vi dem till ovanför skärmen
		if self.rect.y > SCREEN_HEIGHT:
			self.reset_pos()
			
class Monster(pygame.sprite.Sprite):
	change_x = 4
	
	def __init__(self):
		super(Monster, self).__init__()
		
		self.image = pygame.image.load("monster.png").convert()
		self.rect = self.image.get_rect()
		
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

class Player(pygame.sprite.Sprite):
	# Player class #
	# Set speed vectors
	change_x = 0
	change_y = 0
	
	def __init__(self):
		super(Player, self).__init__()
		
		self.image = pygame.image.load("nano_warrior.png").convert()
		self.image.set_colorkey(BLACK)
		
		# Få en rektangel av bilden, viktigt för kollision detection
		# och för att förflytta karaktären
		self.rect = self.image.get_rect()
		
		self.rect.x = SCREEN_WIDTH/2
		self.rect.y = SCREEN_HEIGHT/2
	
	# Funktionen för att röra på sig
	def changespeed(self, x, y):
		self.change_x += x
		self.change_y += y
		
	# Funktionen för att skjuta
	def shoot(self):
		laser = Laser()
		laser_sound.play()
		
		laser.rect.x = player.rect.x
		laser.rect.y = player.rect.y
			
		all_sprites_list.add(laser)
		laser_list.add(laser)
	
	# Kallas varje gång "all_sprites_list(update)" kallas
	def update(self):
		self.rect.x += self.change_x
		self.rect.y += self.change_y
		
# Klass för lasern, skotten
class Laser(pygame.sprite.Sprite):
	def __init__(self):
		super(Laser, self).__init__()
		
		# Använder ingen bild, bara pygame inbyggda funktioner för att
		# skapa rektanglar.
		self.image = pygame.Surface([2, 5])
		self.image.fill(CYAN)
		
		self.rect = self.image.get_rect()
	
	def update(self):
		# Move the LAZOR
		# Öka på 3 för att öka hastigheten av skotten
		self.rect.y -= 3
		
# Funktion för att display:a GAMEOVER,
# Tar även bort spelaren och virusen.
def gameoverscreen():
	all_sprites_list.empty()
	player.kill()
	screen.blit(gameover_disp, (270, 200))

def gamewinscreen():
	all_sprites_list.empty()
	player.kill()
	screen.blit(gamewin_disp, (270, 200))
	
def game_clean():
	for entity in all_sprites_list:
		all_sprites_list.remove(entity)

# Färger => deras RGB värden
BLACK 	= (  0,   0,   0)
YELLOW 	= (255, 255,  40)
CYAN 	= (  0, 221, 255)

#Skärm dimensioner
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NANO WARRIOR")
	
# Laddar bakgrundsbilden
bg = pygame.image.load("nano_world.png").convert()

# Fonts för Gameover och Score
scorefont = pygame.font.SysFont("Arial", 22)
resultfont = pygame.font.SysFont("Arial", 50, True)

# --- Sound ---

laser_sound = pygame.mixer.Sound("laser.ogg")
pygame.mixer.music.load("NTD11.mp3")
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT) # Signalerar när musiken tagit slut, startar om
pygame.mixer.music.play()

# --- Game stuff ---
game = True

clock = pygame.time.Clock()

# Gömmer musen
pygame.mouse.set_visible(False)

# Grupper för virus, alla sprites, och laser
# Grupper är del av Sprite klassen i pygame,
# gör det mycket lättare att kolla kollisioner 
# och att ta bort sprites när man är klar med dem.

virus_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()

#~ 
# Create all the virus enemies
# Byt argumentet i range för att ändra hur många fiender som skapas
# 200 är alltså max score man kan få, om man dödar alla.
for i in range(200):
	
	virus = Virus()
	
	virus.rect.x = random.randrange(SCREEN_WIDTH)
	# Virusen skapas ovanför skärmen5
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


gameover_disp = resultfont.render("GAME OVER", 1, YELLOW)
gamewin_disp = resultfont.render("YOU WIN!", 1, CYAN)

score = 0

while game:
	# --- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game = False
			
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_SPACE and not do_endscreen:
				player.shoot()
				
			elif event.key == pygame.K_a and not do_endscreen:
				player.changespeed(-2, 0)
			elif event.key == pygame.K_d and not do_endscreen:
				player.changespeed(2, 0)
			elif event.key == pygame.K_w and not do_endscreen:
				player.changespeed(0, -2)
			elif event.key == pygame.K_s and not do_endscreen:
				player.changespeed(0, 2)
				
			elif event.key == (pygame.K_RETURN or pygame.K_ESCAPE) and do_endscreen:
				game = False
				
			elif event.key == pygame.K_r:
				game_clean()
				
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
	score_disp = scorefont.render("Score: " + str(score), 1, YELLOW)
	
	
	if laser_list:
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
			
	if virus_list:
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
		gameoverscreen()
		
	if not virus_list:
		gamewinscreen()
	
	# Draws all sprites
	all_sprites_list.draw(screen)
	pygame.display.flip()
	
	# --- Limit to 60 fps
	clock.tick(60)
	
pygame.quit()
