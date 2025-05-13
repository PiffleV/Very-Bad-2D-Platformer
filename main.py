# Library loading
import pygame
import pygame.freetype
from rectangles import drawRect
from player import Player
from direction import Direction
pygame.init()
# Def draw everything to recalculate collisions
def draw():
    global floor
    global roof
    global plat1
    window.fill((100,206,235))
    floor = drawRect(window, (0, 1080/4*3), (1920, 1080/4), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
    roof = drawRect(window, (1920/4*1.5, 610), (1920/4, 10), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
    plat1 = drawRect(window, (2000, 1080/4*3), (10, 1080/4), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
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
# Font
death_font = pygame.freetype.Font("ShareTech-Regular.ttf",200*scale)
restart_font = pygame.freetype.Font("ShareTech-Regular.ttf",100*scale)
# Draw to stop crashes
draw()
# Main loop
drawing = True
game_over = False
while drawing:
    # Quit if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False
    # Collide items
    collide = [floor, roof, plat1,]
    # Interactions
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        drawing = False
    # Movement 
    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shift -= 10*scale
            # Help the illusion
            if player.x > player.center*scale - 10*scale:
                player.x -= 5*scale
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shift += 10*scale
            # Help the illusion
            if player.x < player.center*scale + 10*scale:
                player.x += 5*scale
        # Jump
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if player.grounded:
                player.grav = -20*scale
        # Send player to center
        if player.x > player.center*scale and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.x -= 5*scale
        if player.x < player.center*scale and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.x += 5*scale
        # Gravity
        player.y += player.grav
        if not player.grounded:
            if player.grav < 15*scale:
                player.grav += 1*scale
    # Restart
    if game_over:
            if keys[pygame.K_SPACE]:
                player.x, player.y = (200*scale,0)
                player.draw(window, scale)
                game_over = False
                shift = 0
    # Draw to get movement hitboxes
    draw()
    # Grounded check
    for i in collide:
        if not player.rect.colliderect(i.rect):
            player.grounded = False
    # Collision
    collide_side = None
    for i in collide:
        if player.rect.colliderect(i.rect):
            # Check which side it is colliding with by moving the player
            original_x, original_y = player.x, player.y
            
            player.x = original_x - 20*scale
            player.draw(window, scale)
            if not player.rect.colliderect(i.rect):
                collide_side = Direction.LEFT

            player.x = original_x + 20*scale
            player.draw(window, scale)
            if not player.rect.colliderect(i.rect):
                collide_side = Direction.RIGHT
            player.x = original_x

            player.y = original_y - 20*scale
            player.draw(window, scale)
            if not player.rect.colliderect(i.rect):
                collide_side = Direction.UP

            player.y = original_y + 20*scale
            player.draw(window, scale)
            if not player.rect.colliderect(i.rect):
                collide_side = Direction.DOWN
            player.y = original_y
            player.draw(window, scale)
        while player.rect.colliderect(i.rect):
            if collide_side == Direction.UP:
                player.y -= 1
                player.draw(window, scale)
                player.grounded = True
            elif collide_side == Direction.DOWN:
                player.y += 1
                player.draw(window, scale)
                if player.grav < 0:
                    player.grav *= -1
            elif collide_side == Direction.LEFT:
                shift -= 10*scale
                player.x = player.center *scale
                i_x, i_y = i.pos
                if i.texture:
                    i = drawRect(window, (i_x - shift, i_y), i.size, texture = i.texture)
                elif i.color:
                    i = drawRect(window, (i_x - shift, i_y), i.size, color = i.texture)
                player.draw(window, scale)
            elif collide_side == Direction.RIGHT:
                shift += 10*scale
                player.x = player.center*scale
                i_x, i_y = i.pos
                if i.texture:
                    i = drawRect(window, (i_x - shift, i_y), i.size, texture = i.texture)
                elif i.color:
                    i = drawRect(window, (i_x - shift, i_y), i.size, color = i.texture)
                player.draw(window, scale)
            else:
                break
    # Draw for graphics
    draw()
    # Kill code
    x, y = window.get_size()
    if player.rect.top > y:
        game_over_rect = death_font.get_rect("Game Over!")
        restart_rect = restart_font.get_rect("Press space to restart.")
        x1, y1 = game_over_rect.center
        death_font.render_to(window, (x/2-x1, 100*scale), "Game Over!")
        x2, y2 = restart_rect.center
        restart_font.render_to(window, (x/2-x2, (game_over_rect.bottom+50)*scale), "Press space to restart.")
        game_over = True
    pygame.display.flip()
    c.tick(40)