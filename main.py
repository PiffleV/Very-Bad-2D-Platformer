# Library loading
import pygame
from rectangles import drawRect
from player import Player
pygame.init()
# Def draw everything to recalculate collisions
def draw():
    global floor
    global roof
    window.fill((0,155,0))
    floor = drawRect(window, (0 - shift, 1080*scale/4*3), (1920*scale, 1080*scale/4), texture = 'images\\drit.jpg')
    roof = drawRect(window, (1920*scale/4*1.5 - shift, 1080*scale/4*2), (1920*scale/4, 1080*scale/8), texture = 'images\\drit.jpg')
    player.draw(window, scale)
# Scale window to screen
height = pygame.display.Info().current_h
scale = height/1080
window = pygame.display.set_mode([1920*scale,1080*scale])
shift = 0
# Get player
player = Player()
# Clock
c = pygame.time.Clock()
# Draw to stop crashes
draw()
# Main loop
drawing = True
while drawing:
    # Quit if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False
    # Collide items
    collide = [floor, roof]
    # Interactions
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        drawing = False
    # Movement 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        shift -= 10
        # Help the illusion
        if player.x > player.center - 10:
            player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        shift += 10
        # Help the illusion
        if player.x < player.center + 10:
            player.x += 5
    # Jump
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if player.grounded:
            player.grav = -15
    # Send player to center
    if player.x > player.center and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player.x -= 5
    if player.x < player.center and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        player.x += 5
    # Gravity
    player.y += player.grav
    if not player.grounded:
        if player.grav < 10:
            player.grav += 1
    # Draw to get movement hitboxes
    draw()
    # Grounded check
    for i in collide:
        if not player.rect.colliderect(i.rect):
            player.grounded = False
    # Collision
    saved_gravity = player.grav
    player.grav = 0        
    for i in collide:
        while player.rect.colliderect(i.rect):
            player.y -= 10
            player.draw(window, scale)
            player.grounded = True
    player.grav = saved_gravity
    # Draw for graphics
    draw()
    pygame.display.flip()
    c.tick(40)