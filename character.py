import pygame 

pygame.init()

# window dimensions
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height)) 

# screen caption
pygame.display.set_caption('Sky Hop') 

# background color (RGB) 
background_colour = (234, 212, 252) 

# insert character image
character_image = pygame.image.load("character.png")

# scale smoothly the image
character_image = pygame.transform.smoothscale(character_image, (100, 100))

# take the image's coordinates
character_width, character_height = character_image.get_size()
character_x = (screen_width // 2) - (character_width // 2)
character_y = screen_height - character_height - 10

# keeps the value of the ground for the character
initial_y = character_y

# fill the window with the created color
screen.fill(background_colour) 

#font = pygame.font.SysFont('Comic Sans MS', 24, bold = True)
#title_text = font.render("Sky Hop", True, (255, 255, 255))
#title_position = (screen_width // 2 - title_text.get_width() // 2, 10)

# add the character to the window to the calculated coordinates
screen.blit(character_image, (character_x, character_y))

# update the modifications 
pygame.display.flip() 

# variable to keep the game loop running
running = True

# variables for jumping
velocity_y = 0      # the vertical speed of the character
gravity = 0.15		# gravitationsl acceleration
jump_force = -8		# checks how high can the character jump

# distance to move left or right (the horizontal speed of the character)
speed_x = 5

# game loop 
while running: 
	
	# keep the background the desired color
	screen.fill(background_colour)

	# checks if the game is stopped
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			running = False

	keys = pygame.key.get_pressed()

	# moves the character to left if the left arrow key is pressed
	if keys[pygame.K_LEFT]:
		character_x = character_x - speed_x
	# moves the character to the right if the right arrow key is pressed
	if keys[pygame.K_RIGHT]:
		character_x = character_x + speed_x

	# checks if the character exists the screen
	if character_x < 0:
		character_x = 0
	if character_x > screen_width - character_width:
		character_x = screen_width - character_width

	# updates the variables for jumping continuously
	character_y = character_y + velocity_y
	
	# updates the velocity using gravity
	velocity_y = velocity_y + gravity
	velocity_y = min(velocity_y, 5)

	# stop jumping when getting back on the ground
	if character_y >= initial_y:
		character_y = initial_y
		velocity_y = -8

	# draw the character (to update its new position on the screen)
	screen.blit(character_image, (character_x, character_y))

	# update the display
	pygame.display.flip()

	pygame.time.delay(10) 
