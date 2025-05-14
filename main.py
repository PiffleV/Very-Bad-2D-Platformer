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
    global win
    window.fill((100,206,235))
    player.draw(window, scale)
    if player.level == 1:
        floor = drawRect(window, (0, 1080/4*3), (1920, 1080/4), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
        roof = drawRect(window, (720, 610), (1920/4, 10), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
        plat1 = drawRect(window, (2400, 1080/4*3), (10, 1080/4), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
        win = drawRect(window, (2410, 1080/4*3), (50,50), scale = scale, shift = shift, color = (255,255,0))
    elif player.level == 2:
        floor = drawRect(window, (0, 1080/4*3), (1920, 1080/4), scale = scale, shift = shift, texture = 'images\\dirt.jpg')
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
start_font = pygame.freetype.Font("ShareTech-Regular.ttf",100*scale)
# Draw to stop crashes
draw()
# Main loop
drawing = True
game_over = False
tutorial = True
while drawing:
    # Quit if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False
    # Collide items
    if player.level == 1:
        collide = [floor, roof, plat1,]
    elif player.level == 2:
        collide = [floor]
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
                if player.jumpcount > 0:
                    player.grav = -20*scale
                    player.jumpcount -= 1
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
                player.jumpcount = player.jumplimit
            elif collide_side == Direction.DOWN:
                player.y += 1
                player.draw(window, scale)
                if player.grav < 0:
                    player.grav *= -1
            elif collide_side == Direction.LEFT:
                while player.rect.colliderect(i.rect):
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
            elif not collide_side:
                break
    # Draw for graphics
    draw()
    # Kill code
    x, y = window.get_size()
    if player.rect.top > y:
        game_over_rect = death_font.get_rect("Game Over!")
        restart_rect = start_font.get_rect("Press space to restart.")
        x1, y1 = game_over_rect.center
        death_font.render_to(window, (x/2-x1, 100*scale), "Game Over!")
        x2, y2 = restart_rect.center
        start_font.render_to(window, (x/2-x2, (game_over_rect.bottom+50)*scale), "Press space to restart.")
        game_over = True
    # Win code
    if player.rect.colliderect(win.rect):
        player.x, player.y = (200*scale,0)
        player.draw(window, scale)
        game_over = False
        shift = 0
        for i in collide:
            i.rect.topleft = (-2147483648, -2147483648)
            draw()
        player.level += 1
    if tutorial:
        draw()
        start_rect = start_font.get_rect("WASD or arrow keys to move")
        x3, y3 = start_rect.center
        x, _ = window.get_size()
        start_font.render_to(window, (x/2-x3, 100*scale), "WASD or arrow keys to move")
        keys = pygame.key.get_pressed()
        for i in keys:
            if i:
                tutorial = False
        pygame.display.flip()
    pygame.display.flip()
    c.tick(40)