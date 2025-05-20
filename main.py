# Library loading
import pygame
import pygame.freetype
from rectangles import drawRect
from player import Player
from direction import Direction
pygame.init()
# Def draw everything to recalculate collisions
def draw(images):
    global floor, roof, plat1, win, plat2, plat3, plat4, jump
    window.fill((100,206,235))
    player.draw(window, scale)
    match player.level:
        case 1:
            floor = drawRect(window, (0, 810), (1920, 270), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            roof = drawRect(window, (720, 610), (1920/4, 10), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (2350, 810), (10, 270), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            win = drawRect(window, (2410, 810), (50,50), scale = scale, shift = shift, color = (255,255,0))
            for i in (floor, roof, plat1, win):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
        case 2:
            floor = drawRect(window, (0, 810), (1920, 270), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (640,0), (10, 620), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat2 = drawRect(window, (840,0), (10, 620), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat3 = drawRect(window, (640,620), (100, 10), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat4 = drawRect(window, (740,420), (100, 10), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            win = drawRect(window, (725, 100), (50,50), scale = scale, shift = shift, color = (255,255,0))
            for i in (floor, plat1, plat2, plat3, plat4, win):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
        case 3:
            floor = drawRect(window, (-100, 300), (2020, 100), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (0, 1080-20), (1920, 20), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat2 = drawRect(window, (1910, 0), (10, 300), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            win = drawRect(window, (1920/2-25, 1080-70), (50,50), scale = scale, shift = shift, color = (255,255,0))
            for i in (floor, plat1, plat2):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
        case 4:
            floor = drawRect(window, (-100, 300), (2020, 100), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (0, 1080-20), (1920, 20), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat2 = drawRect(window, (1910, 0), (10, 300), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat3 = drawRect(window, (-100, 0), (10, 300), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat4 = drawRect(window, (1900, 195), (10, 10), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            win = drawRect(window, (1920/2-25, 1080-70), (50,50), scale = scale, shift = shift, color = (255,255,0))
            for i in (floor, plat1, plat2, plat3, plat4):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
        case 5:
            floor = drawRect(window, (-100, 300), (2020, 100), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (0, 1080-20), (1920, 20), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat2 = drawRect(window, (1910, 0), (10, 300), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            plat3 = drawRect(window, (-100, 0), (10, 300), scale = scale, shift = shift, texture = "images\\dirt.jpg", cache = images)
            win = drawRect(window, (1920/2-25, 1080-70), (50,50), scale = scale, shift = shift, color = (255,255,0))
            if not collected:
                jump = drawRect(window, (500, 250), (50,50), scale = scale, shift = shift, color = (0,0,255))
            for i in (floor, plat1, plat2, plat3):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
        case 6:
            floor = drawRect(window, (0, 1080-300), (2020, 250), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            plat1 = drawRect(window, (100, 1080-405), (10, 10), scale = scale, shift = shift, texture = "images\\grass.jpg", cache = images)
            win = drawRect(window, (110+400, 1080-50), (50,50), scale = scale, shift = shift, color = (255,255,0))
            for i in (floor, plat1):
                if i.image:
                    if not (i.texture, i.size_scaled) in images:
                        images[(i.texture, i.size_scaled)] = i.image
    player.draw(window, scale)
# Scale window to screen
height = pygame.display.Info().current_h
scale = height/1080
window = pygame.display.set_mode([1920*scale,1080*scale])
shift = 0
# cache images
images = {
    "":""
}
# Get player
player = Player()
# Font
death_font = pygame.freetype.Font("ShareTech-Regular.ttf",200*scale)
start_font = pygame.freetype.Font("ShareTech-Regular.ttf",100*scale)
# Draw to stop crashes
draw(images)
# Main loop
drawing = True
game_over = False
tutorial = True
skip = False
collected = False
holding_w = False
while drawing:
    # for fps printing
    start_frame = pygame.time.get_ticks()
    # Quit if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False
    # Collide items
    match player.level:
        case 1:
            collide = [floor, roof, plat1,]
        case 2:
            collide = [floor, plat1, plat2, plat3, plat4]
        case 3:
            collide = [floor, plat1,plat2]
        case 4:
            collide = [floor, plat1, plat2, plat3, plat4]
        case 5:
            collide = [floor, plat1, plat2, plat3]
        case 6:
            player.jumplimit = 1
            collide = [floor, plat1]
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
                player.grav = -20
                holding_w = True
            else:
                if not holding_w:
                    if player.jumpcount > 0:
                        player.grav = -20
                        player.jumpcount -= 1
                    holding_w = True
        else:
            holding_w = False
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
    draw(images)
    move_frame = pygame.time.get_ticks() - start_frame
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
            y_move = 0
            x_move = 0
            if collide_side == Direction.LEFT or collide_side == Direction.RIGHT:
                player.x = player.center
                player.draw(window, scale)
            while player.rect.colliderect(i.rect):
                if collide_side == Direction.UP:
                    player.rect.move_ip(0,-1)
                    y_move -= 1
                    player.grounded = True
                    player.jumpcount = player.jumplimit
                elif collide_side == Direction.DOWN:
                    player.rect.move_ip(0,1)
                    y_move += 1
                    if player.grav < 0:
                        player.grav *= -1
                elif collide_side == Direction.LEFT:
                    i.rect.move_ip(1,0)
                    x_move -= 1
                elif collide_side == Direction.RIGHT:
                    i.rect.move_ip(-1,0)
                    x_move += 1
                elif not collide_side:
                    break
            player.y += y_move
            shift += x_move
    # Draw for graphics
    draw(images)
    collision_frame = (pygame.time.get_ticks() - start_frame)
    # Kill code
    if player.rect.top > window.get_size()[1]:
        game_over_rect = death_font.get_rect("Game Over!")
        restart_rect = start_font.get_rect("Press space to restart.")
        death_font.render_to(window, (window.get_size()[0]/2-game_over_rect.center[0], 100*scale), "Game Over!")
        start_font.render_to(window, (window.get_size()[0]/2-restart_rect.center[0], (game_over_rect.bottom+50)*scale), "Press space to restart.")
        game_over = True
    # Win code
    if player.rect.colliderect(win.rect) or (keys[pygame.K_p] and keys[pygame.K_f] and keys[pygame.K_l]):
        if not skip:
            player.x, player.y = (200,0)
            player.draw(window, scale)
            game_over = False
            shift = 0
            for i in collide:
                i.rect.topleft = (-2147483648, -2147483648)
            player.level += 1
            draw(images)
            skip = True
            collected = False
    else:
        skip = False
    # Jump booster
    if player.level == 5:
        if player.rect.colliderect(jump.rect):
            player.jumplimit += 1
            collected = True
            jump.rect.topleft = (1073741824, 1073741824)
    # tutorial
    if tutorial:
        start_rect = start_font.get_rect("WASD or arrow keys to move")
        start_font.render_to(window, (window.get_size()[0]/2-start_rect.center[0], 100*scale), "WASD or arrow keys to move")
        win_rect = start_font.get_rect("Touch Yellow to move on.")
        start_font.render_to(window, (window.get_size()[0]/2-win_rect.center[0], (start_rect.bottom+50)*scale), "Touch Yellow to move on.")
        jump_rect = start_font.get_rect("Blue lets you jump in the air")
        start_font.render_to(window, (window.get_size()[0]/2-jump_rect.center[0], (win_rect.bottom+150)*scale), "Blue lets you jump in the air")
        keys = pygame.key.get_pressed()
        for i in keys:
            if i:
                tutorial = False
    pygame.display.flip()
    print("Fps: " + str(int(1000/(pygame.time.get_ticks() - start_frame))), "Movement: " + str(move_frame), "Collision: " + str(collision_frame), sep = ", ")
    