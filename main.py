# Library loading
import pygame
import pygame.freetype
from rectangles import drawRect
from player import Player
from direction import Direction
pygame.init()
# cache images
images = {
    "grass": pygame.image.load('images\\grass.jpg'),
    "dirt": pygame.image.load('images\\dirt.jpg')
}
# Def draw everything to recalculate collisions
def draw():
    global floor, roof, plat1, win, plat2, plat3, plat4
    window.fill((100,206,235))
    player.draw(window, scale)
    if player.level == 1:
        floor = drawRect(window, (0, 1080/4*3), (1920, 1080/4), scale = scale, shift = shift, texture = images["grass"])
        roof = drawRect(window, (720, 610), (1920/4, 10), scale = scale, shift = shift, texture = images["grass"])
        plat1 = drawRect(window, (2350, 1080/4*3), (10, 1080/4), scale = scale, shift = shift, texture = images["grass"])
        win = drawRect(window, (2410, 1080/4*3), (50,50), scale = scale, shift = shift, color = (255,255,0))
    elif player.level == 2:
        floor = drawRect(window, (0, 1080/4*3), (1920, 1080/4), scale = scale, shift = shift, texture = images["grass"])
        plat1 = drawRect(window, (1920/3,0), (10, 620), scale = scale, shift = shift, texture = images["dirt"])
        plat2 = drawRect(window, (1920/3+200,0), (10, 620), scale = scale, shift = shift, texture = images["dirt"])
        plat3 = drawRect(window, (1920/3,620), (100, 10), scale = scale, shift = shift, texture = images["dirt"])
        plat4 = drawRect(window, (1920/3+100,420), (100, 10), scale = scale, shift = shift, texture = images["dirt"])
        win = drawRect(window, (1920/3+85, 100), (50,50), scale = scale, shift = shift, color = (255,255,0))
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
        collide = [floor, plat1, plat2, plat3, plat4]
    # Interactions
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        drawing = False
    # Movement 
    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shift -= 10*scale
            # Help the illusion
            if player.x > player.center - 10:
                player.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shift += 10*scale
            # Help the illusion
            if player.x < player.center + 10:
                player.x += 5
        # Jump
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if player.grounded:
                if player.jumpcount > 0:
                    player.grav = -20
                    player.jumpcount -= 1
            else:
                if player.jumpcount > 1:
                    player.grav = -20
                    player.jumpcount -= 1
        # Send player to center
        if player.x > player.center and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.x -= 5
        if player.x < player.center and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.x += 5
        # Gravity
        player.y += player.grav
        if not player.grounded:
            if player.grav < 15:
                player.grav += 1
    # Restart
    if game_over:
            if keys[pygame.K_SPACE]:
                player.x, player.y = (200,0)
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
    y_move = 0
    for i in collide:
        if player.rect.colliderect(i.rect):
            # Check which side it is colliding with by moving the player
            
            if not player.rect.move(-20,0).colliderect(i.rect):
                collide_side = Direction.LEFT

            if not player.rect.move(20,0).colliderect(i.rect):
                collide_side = Direction.RIGHT

            if not player.rect.move(0,-20).colliderect(i.rect):
                collide_side = Direction.UP

            if not player.rect.move(0,20).colliderect(i.rect):
                collide_side = Direction.DOWN
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
                shift -= 1*scale
                player.x = player.center
                if i.texture:
                    i = drawRect(window, i.pos, i.size, scale = scale, shift = shift, texture = i.texture)
                elif i.color:
                    i = drawRect(window, i.pos, i.size, scale = scale, shift = shift, color = i.color)
                player.draw(window, scale)
            elif collide_side == Direction.RIGHT:
                shift += 1*scale
                player.x = player.center
                if i.texture:
                    i = drawRect(window, i.pos, i.size, scale = scale, shift = shift, texture = i.texture)
                elif i.color:
                    i = drawRect(window, i.pos, i.size, scale = scale, shift = shift, color = i.color)
                player.draw(window, scale)
            elif not collide_side:
                break
        player.y += y_move
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
        player.x, player.y = (200,0)
        player.draw(window, scale)
        game_over = False
        shift = 0
        for i in collide:
            i.rect.topleft = (-2147483648, -2147483648)
        player.level += 1
        draw()
    # tutorial
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