import pygame
import random
import sys
import time
from math import sqrt

pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("tnfsh running!!")

#variable
OBSTACLE_MIN_INTERVAL = 5000 
OBSTACLE_MAX_INTERVAL = 10000 
S_OBSTACLE_MIN_INTERVAL = 5000 
S_OBSTACLE_MAX_INTERVAL = 10000 
FRONT_VIEW_MIN_INTERVAL = 8000
FRONT_VIEW_MAX_INTERVAL = 13000
COIN_MIN_INTERVAL = 1000 
COIN_MAX_INTERVAL = 5000
MAX_SKYOB_HEIGHT = 80
MAX_SKYOB_BOTTOM = 130
front_view_timer = 0
obstacle_timer = 0
s_obstacle_timer = 0
Is_boss=False
Is_first=True
Boss_defeated1=False
Boss_defeated2=False
STATE1=False
STATE2=False
coin_timer = 0
active=False

#draw bar function

def draw_bar(surface, x, y, value, max_value, bar_width=150, bar_height=15):
    percentage = value / max_value
    bar_fill_width = int(bar_width * percentage)
    if percentage <= 0.3:
        bar_color = (255, 0, 0)  # red
    else:
        bar_color = (0, 255, 0)  # green
    bg_rect = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(surface, (255, 255, 255), bg_rect)
    fill_rect = pygame.Rect(x, y, bar_fill_width, bar_height)
    pygame.draw.rect(surface, bar_color, fill_rect)
    border_rect = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(surface, (0, 0, 0), border_rect, 1)

# Load game assets
coin_type_1_image = pygame.image.load("images/coin_gold.png").convert_alpha()
coin_type_2_image = pygame.image.load("images/coin_diamond.png").convert_alpha()
coin_type_3_image = pygame.image.load("images/bullet_coin.png").convert_alpha()
bullet_image = pygame.image.load("images/bullet.png").convert_alpha()
#button
start_button_image = pygame.image.load("images/start__button.png").convert_alpha()
restart_button_image = pygame.image.load("images/restart__button.png").convert_alpha()
quit_button_image = pygame.image.load("images/quit_button.png").convert_alpha()
#menu
title_image = pygame.image.load("images/title.png").convert_alpha()
menu_image = pygame.image.load("images/background_2.png").convert_alpha()
#boss fight
fireball_image=pygame.image.load("images/fireball.png").convert_alpha()
boss_image=pygame.image.load("images/boss.png").convert_alpha()
boss_fire_image=pygame.image.load("images/boss2.png").convert_alpha()
#bg
ground_image = pygame.image.load("images/ground.png").convert_alpha()
background_image = pygame.image.load("images/background.png").convert()
#player
player_image1 = pygame.image.load("images/player4_1.png").convert_alpha()
player_image2 = pygame.image.load("images/player2_1.png").convert_alpha()
player_image3 = pygame.image.load("images/player3.png").convert_alpha()
player_image4 = pygame.image.load("images/player4_1.png").convert_alpha()
player_jump_image1 = pygame.image.load("images/player.png").convert_alpha()
player_jump_image2 = pygame.image.load("images/player_jump.png").convert_alpha()
jump_air_image = pygame.image.load("images/jump_air.png").convert_alpha()
#obstacles
obstacle_image1 = pygame.image.load("images/obstacle1.png").convert_alpha()
obstacle_image2 = pygame.image.load("images/obstacle2.png").convert_alpha()
obstacle_image3 = pygame.image.load("images/obstacle4.png").convert_alpha()
obstacle_image4 = pygame.image.load("images/obstacle3.png").convert_alpha()
s_obstacle_image = pygame.image.load("images/obstacle_fly.png").convert_alpha()
obstacle_images = [obstacle_image1, obstacle_image2, obstacle_image3,obstacle_image4]
#frontviews
front_view_image1 = pygame.image.load("images/front.png").convert_alpha()
front_view_image2 = pygame.image.load("images/front.png").convert_alpha()
front_view_image3 = pygame.image.load("images/front.png").convert_alpha()
front_view_image4 = pygame.image.load("images/front.png").convert_alpha()
front_view_images = [front_view_image1,front_view_image2,front_view_image3,front_view_image4]

#font and sound effect
font = pygame.font.Font(None, 24)
font2 = pygame.font.Font('04B_19.TTF', 20)
#bgm
pygame.mixer.music.load('sound_effects/BGM.mp3')
pygame.mixer.music.set_volume(0.25)
#jumpsound
jump_sound = pygame.mixer.Sound('sound_effects/flap.ogg')
jump_sound.set_volume(0.5)
#button pressing sound
button_sound = pygame.mixer.Sound('sound_effects/button.wav')
button_sound.set_volume(1)
#bullet shot sound
bullet_shot_sound = pygame.mixer.Sound('sound_effects/bullet.mp3')
bullet_shot_sound.set_volume(0.3)
#boss fire sound
boss_fire_sound = pygame.mixer.Sound('sound_effects/boss.mp3')
boss_fire_sound.set_volume(0.2)
#gameoversound
game_over_sound = pygame.mixer.Sound('sound_effects/gameover.mp3')
game_over_sound.set_volume(1)
#crash
crash_sound = pygame.mixer.Sound('sound_effects/hit.ogg')
crash_sound.set_volume(1)

#coin
coin_sound = pygame.mixer.Sound('sound_effects/point.ogg')
coin_sound.set_volume(1)

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.standing_images = [player_image2, player_image3,player_image4] 
        self.jumping_images = [player_jump_image1, player_jump_image2]  
        self.current_frame = 0
        self.image = self.standing_images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.velocity = 10
        self.score = 0
        self.gravity = 1
        self.rect.x = 80
        self.jump_power = -14     
        self.max_jumps = 10 
        self.jumps = 0 
        self.space_pressed = False  
        self.animation_timer = 0 
        self.is_jumping = False 
        self.bullet=0
        self.bullets_group = pygame.sprite.Group()
        self.last_bullet_time=time.time()
        self.bullet_cooldown=0.001
        self.bullet_fired = False
        self.max_ammo=25
        self.sky_random_post =0

    def update(self):

        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.bottom > WINDOW_HEIGHT - 20:
            self.rect.bottom = WINDOW_HEIGHT - 20
            self.velocity = 10
            self.jumps = 0  
            self.is_jumping = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and not self.space_pressed and self.jumps < self.max_jumps:
            jump_sound.play()
            self.sky_random_post=random.choice([0,1])
            self.is_jumping = True
            jump_air = JumpObject(jump_air_image,self.rect)
            all_sprites.add(jump_air)
            self.velocity = self.jump_power
            self.jumps += 1
            self.current_frame = 0
        self.space_pressed = keys_pressed[pygame.K_SPACE] 

        if keys_pressed[pygame.K_f] and not self.bullet_fired and time.time() - self.last_bullet_time > self.bullet_cooldown and self.bullet > 0:
            bullet = Bullet(self.rect)
            bullet_shot_sound.play()
            bullets.add(bullet)
            all_sprites.add(bullet)
            self.bullet -= 1
            self.last_bullet_time = time.time()
            self.bullet_fired = True
        if not keys_pressed[pygame.K_f]:
            self.bullet_fired = False

        coins_collected = pygame.sprite.spritecollide(self, coins, True)
        for coin in coins_collected:
            self.score +=coin.score
            if coin.type==3 and self.bullet+1<=25:
                self.bullet+=1

        # Update animation
        if not self.is_jumping:
            self.animation_timer += 1.85
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.standing_images)
                self.image = self.standing_images[self.current_frame]
        else:
            self.image = self.jumping_images[self.sky_random_post]
            if active==False:
                self.kill()

#air class
class JumpObject(pygame.sprite.Sprite):
    def __init__(self,image,player_rect):
        super().__init__()
        self.image = image
        self.image.set_alpha(255)  
        self.rect = self.image.get_rect()
        self.rect.bottom = player_rect.bottom+15
        self.rect.centerx = player_rect.centerx+15
        self.velocity = 2
        self.creation_time = pygame.time.get_ticks() / 1000  
        self.lifetime = 0.3

    def update(self):
        elapsed_time = pygame.time.get_ticks() / 1000 - self.creation_time  
        if elapsed_time < self.lifetime:
            self.rect.y += self.velocity
            opacity = int(255-(elapsed_time / self.lifetime * 255)) 
            self.image.set_alpha(opacity)
        else:    
            self.kill()

#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.x
        self.rect.centery = player_rect.y
        self.speed = 15

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WINDOW_WIDTH:
            self.kill()

# Define the coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_type):
        super().__init__()
        self.type=coin_type
        if coin_type == 1:
            # For coin type 1
            self.image = coin_type_1_image
            self.score = 80
        elif coin_type == 2:
            # For coin type 2
            self.image = coin_type_2_image
            self.score = 300
        else:
            # For fighting boss item
            self.image = coin_type_3_image
            self.score = 0

        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + self.rect.width
        self.rect.y = random.randrange(250, WINDOW_HEIGHT - 80)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0 or active==False:
            self.kill()

# front view
class Front_view(pygame.sprite.Sprite):
    def __init__(self, image_type):
        super().__init__()
        self.reduction=125
        self.image = front_view_images[image_type]
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.y = WINDOW_HEIGHT-self.reduction
        self.rect.x = WINDOW_WIDTH + self.rect.width
        self.speed = 5
        self.opacity = 255

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0 or active==False:
            self.kill()

        player_collisions = pygame.sprite.spritecollide(self, player_group, False)
        if player_collisions:
            distance = pygame.math.Vector2(player_collisions[0].rect.center) - pygame.math.Vector2(self.rect.center)
            distance_length = distance.length()
            max_distance = 150
            min_distance = 0
            if distance_length > max_distance:
                self.opacity = 255
            elif distance_length < min_distance:
                self.opacity = 50
            else:
                self.opacity = int((distance_length / max_distance) * 255)
            self.image = self.original_image.copy()
            self.image.fill((255, 255, 255, self.opacity), special_flags=pygame.BLEND_RGBA_MULT)

# Define the obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_type):
        super().__init__()
        if image_type==0:
            self.reduction=180
        elif image_type==1:
            self.reduction=200
        elif image_type==2:
            self.reduction=80
        else:
            self.reduction=110
        self.image = obstacle_images[image_type]
        self.rect = self.image.get_rect()
        self.rect.y = WINDOW_HEIGHT-self.reduction
        self.rect.x = WINDOW_WIDTH + self.rect.width
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0 or active==False:
            self.kill()
        bullet_crashed = pygame.sprite.spritecollide(self, bullets, True)
        for _ in bullet_crashed:
            self.kill()

# Define the skyobstacle class
class sky_Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = s_obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + self.rect.width
        self.rect.y =random.randrange(MAX_SKYOB_HEIGHT,MAX_SKYOB_BOTTOM,25)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0 or active==False:
            self.kill()
        bullet_crashed = pygame.sprite.spritecollide(self, bullets, True)
        for _ in bullet_crashed:
            self.kill()

# Define the ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, image, x,speed,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_HEIGHT+y
        self.x = x
        self.speed=speed
    def update(self):
        self.x -= self.speed
        if self.x < -self.rect.width:
            self.x += self.rect.width*2
        self.rect.x = self.x

# Create a button sprite
class Button(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = True
        
    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            
    def set_visibility(self, visible):
        self.visible = visible
    
    def is_visible(self):
        return self.visible
    
    def is_pressed(self, event):
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        else:
            return False

#boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self,code):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH-130
        self.rect.y = 200
        self.speed = 3
        self.score_threshold = 2000
        self.fireball_timer = 0
        self.movement_timer=0
        self.fireballs = pygame.sprite.Group()
        self.direction = 1
        if code:
            self.hp=2000
            self.movement_cooldown=500
            self.fireball_cooldown=500
        else:
            self.hp=500 
            self.movement_cooldown=800
            self.fireball_cooldown=800
        self.HP_STATE=self.hp
        self.fire_image = boss_fire_image
        self.fire_timer = 0
        self.fire_duration = 500

    def update(self):
        score=player.score
        current_time = pygame.time.get_ticks()

        # fireball shooting logic
        if score >= self.score_threshold and current_time - self.fireball_timer >= self.fireball_cooldown:
            self.image = self.fire_image
            self.fire_timer = current_time
            fireball = Fireball(player.rect.center)
            fireball.rect.midright = self.rect.midleft
            boss_fire_sound.play()
            fireballs.add(fireball)
            all_sprites.add(fireball)
            self.fireball_timer = current_time
        if current_time - self.fire_timer >= self.fire_duration:
            self.image = boss_image
        self.fireballs.update()
        for fireball in self.fireballs.copy():
            if fireball.rect.right < 0:
                fireball.kill()

        # collision detection with player bullets
        bullet_crashed = pygame.sprite.spritecollide(self, bullets, True)
        for _ in bullet_crashed:
            self.hp-=40

        # draw boss hp bar
        boss_hp_text = font2.render("HP: " + str(self.hp), True, (255, 100, 100))
        game_window.blit(boss_hp_text, (WINDOW_WIDTH-170, 7))
        draw_bar(game_window, WINDOW_WIDTH-170, 30, self.hp, self.HP_STATE)

        # movement
        if current_time - self.movement_timer >= self.movement_cooldown:
            # change direction randomly and reset timer
            self.direction = random.choice([-1, 1])
            self.movement_timer = current_time
            self.movement_cooldown = random.randrange(1000, 3000) # randomize cooldown time
        # update vertical position
        new_y = self.rect.y + self.direction * self.speed
        if new_y < 0:
            self.direction = 1
            self.rect.y = 0
        elif new_y > WINDOW_HEIGHT - self.rect.height:
            self.direction = -1
            self.rect.y = WINDOW_HEIGHT - self.rect.height
        else:
            self.rect.y = new_y

        if active==False:
            self.kill()
        if self.hp<=0:
            self.kill()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        super().__init__()
        self.image = fireball_image
        self.rect = self.image.get_rect()
        player_pos=(player.rect.centerx,player.rect.centery)
        dx = player_pos[0] - boss.rect.x
        dy = player_pos[1] - boss.rect.y
        dist = sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / dist
        self.dy = dy / dist

        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.right < 0 or active==False:
            self.kill()
        bullet_crashed = pygame.sprite.spritecollide(self, bullets, True)
        for _ in bullet_crashed:
            self.kill()
        

#class title effect
class BreathingImage:
    def __init__(self, image, center_pos):
        self.image =image
        self.rect = self.image.get_rect(center=center_pos)
        self.angle = 0
        self.size_range = (400, 420)
        self.size_speed = 0.5
        self.angle_range = (-1, 7)
        self.angle_speed = 0.1

    def update(self):
        size = int((self.size_range[1] - self.size_range[0]) * (abs(pygame.time.get_ticks() % 2000 - 1000) / 1000) + self.size_range[0])
        self.angle = (self.angle_range[1] - self.angle_range[0]) * (abs(pygame.time.get_ticks() % 2000 - 1000) / 1000) + self.angle_range[0]
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, size / max(self.image.get_size()))
        self.rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image

#sprite groups:player coins obstacles ground background title
player_group = pygame.sprite.GroupSingle(Player())
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
sparke_boss=pygame.sprite.Group()
bullets=pygame.sprite.Group()
bg=pygame.sprite.Group()
ground1 = Ground(ground_image, 0, 5,60)
ground2 = Ground(ground_image, ground1.rect.width, 5,60)
background1 = Ground(background_image, 0, 0.5,0)
background2 = Ground(background_image, background1.rect.width, 0.5,0)
title = BreathingImage(title_image, center_pos=(500, 100))
bg.add(background1)
bg.add(background2)
bg.add(ground1)
bg.add(ground2)
start_button = Button(start_button_image,315,300)
restart_button = Button(restart_button_image,250,250)
quit_button = Button(quit_button_image,200,370)
boss = Boss(0)
boss2 = Boss(1)
player = Player()
player_group.add(player)
all_sprites.add(player)


# Set up the game loop
clock = pygame.time.Clock()
game_over = False
active=False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN and active==False:
            if quit_button.is_pressed(event):
                game_over_sound.stop()
                button_sound.play()
                game_over = True
            elif start_button.is_pressed(event):
                pygame.mixer.music.play(-1)
                button_sound.play()
                Is_first=False
                start_button.set_visibility(False)
                active=True
            elif restart_button.is_pressed(event):
                #initialize
                game_over_sound.stop()
                button_sound.play()
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1) 
                OBSTACLE_MIN_INTERVAL = 5000 
                OBSTACLE_MAX_INTERVAL = 10000
                S_OBSTACLE_MIN_INTERVAL = 5000 
                S_OBSTACLE_MAX_INTERVAL = 10000 
                MAX_SKYOB_HEIGHT =80
                MAX_SKYOB_BOTTOM =130
                obstacle_timer = 0
                s_obstacle_timer = 0
                COIN_MIN_INTERVAL = 500 
                COIN_MAX_INTERVAL = 2000  
                coin_timer = 0
                sparke_boss.empty()
                bullets.empty()
                all_sprites.empty()
                coins.empty()
                obstacles.empty()
                fireballs.empty()
                player_group.empty()
                boss = Boss(0)
                boss2 = Boss(1)
                sparke_boss.add(boss)
                player = Player()
                player_group.add(player)
                all_sprites.add(player)
                obstacle = Obstacle(random.choice([1,2,3,0]))
                player.score = 0
                Boss_defeated1 = False
                Boss_defeated2 = False
                STATE1=False
                STATE2=False
                Is_boss=False
                game_over = False
                active=True
    if active:     
        # Generate coins obstacles
        if coin_timer <= 0:
            if not Is_boss:
                coin=Coin(random.choice([1,1,2,3,3]))
            else:
                coin=Coin(3)
            coins.add(coin)
            all_sprites.add(coin)
            coin_timer = random.randint(COIN_MIN_INTERVAL, COIN_MAX_INTERVAL)
        else:
            coin_timer-=60 

        if obstacle_timer <= 0:
            obstacle = Obstacle(random.choice([1,1,1,2,3,0]))
            obstacles.add(obstacle)
            all_sprites.add(obstacle)
            obstacle_timer = random.randint(OBSTACLE_MIN_INTERVAL, OBSTACLE_MAX_INTERVAL) 
        else:
            obstacle_timer-=60

        if front_view_timer <= 0:
            front_view=Front_view(random.choice([1,2,3,0]))
            all_sprites.add(front_view)
            front_view_timer = random.randint(FRONT_VIEW_MIN_INTERVAL, FRONT_VIEW_MAX_INTERVAL) 
        else:
            front_view_timer-=60 

        if s_obstacle_timer <= 0:
            sky_obstacle = sky_Obstacle()
            obstacles.add(sky_obstacle)
            all_sprites.add(sky_obstacle)
            s_obstacle_timer = random.randint(S_OBSTACLE_MIN_INTERVAL, S_OBSTACLE_MAX_INTERVAL)
        else:
            s_obstacle_timer-=60

        if pygame.sprite.spritecollide(player, fireballs, True):
            pygame.mixer.music.stop()
            crash_sound.play()
            game_over_sound.play()
            active = False

        if pygame.sprite.spritecollide(player, obstacles, False):
            pygame.mixer.music.stop()
            crash_sound.play()
            game_over_sound.play()
            active = False

        if pygame.sprite.spritecollide(coin, obstacles, False):
            coin.kill()

        if pygame.sprite.spritecollide(front_view, obstacles, False):
            front_view.kill()
        
        # game level
        # orginal
            # OBSTACLE_MIN_INTERVAL = 5000 
            # OBSTACLE_MAX_INTERVAL = 10000
            # S_OBSTACLE_MIN_INTERVAL = 5000 
            # S_OBSTACLE_MAX_INTERVAL = 10000 
            # MAX_SKYOB_HEIGHT =80
            # MAX_SKYOB_BOTTOM =130
        if Is_boss==True:
            OBSTACLE_MIN_INTERVAL = 999999
            OBSTACLE_MAX_INTERVAL = 999999
            S_OBSTACLE_MIN_INTERVAL = 999999
            S_OBSTACLE_MAX_INTERVAL = 999999
            COIN_MIN_INTERVAL = 500 
            COIN_MAX_INTERVAL = 900
            MAX_SKYOB_HEIGHT =0
            MAX_SKYOB_BOTTOM =1

        elif  6000<=player.score<12000:
            OBSTACLE_MIN_INTERVAL = 5000 
            OBSTACLE_MAX_INTERVAL = 7000
            S_OBSTACLE_MIN_INTERVAL = 5000 
            S_OBSTACLE_MAX_INTERVAL = 8500
            COIN_MIN_INTERVAL = 1000 
            COIN_MAX_INTERVAL = 2000
            MAX_SKYOB_HEIGHT =150
            MAX_SKYOB_BOTTOM =170
        elif  12000<=player.score<18000:
            OBSTACLE_MIN_INTERVAL = 4500 
            OBSTACLE_MAX_INTERVAL = 6500
            S_OBSTACLE_MIN_INTERVAL = 4500 
            S_OBSTACLE_MAX_INTERVAL = 6500 
            COIN_MIN_INTERVAL = 500 
            COIN_MAX_INTERVAL = 1000
            MAX_SKYOB_HEIGHT =150
            MAX_SKYOB_BOTTOM =230
        elif  player.score>=18000:
            OBSTACLE_MIN_INTERVAL = 2000 
            OBSTACLE_MAX_INTERVAL = 5000
            S_OBSTACLE_MIN_INTERVAL = 2500 
            S_OBSTACLE_MAX_INTERVAL = 4500 
            COIN_MIN_INTERVAL = 10
            COIN_MAX_INTERVAL = 100
            MAX_SKYOB_HEIGHT =200
            MAX_SKYOB_BOTTOM =270

        # Update and draw all
        all_sprites.update()
        bg.update()
        bg.draw(game_window)
        all_sprites.draw(game_window)

        #if boss and after boss
        if 2000<=player.score and Is_boss==False and Boss_defeated1==False and STATE1==False:
           STATE1=True
           sparke_boss.add(boss)
           Is_boss=True
        if player.score>=15000 and Is_boss==False and Boss_defeated1==True and Boss_defeated2==False and STATE2==False:
           STATE2=True
           sparke_boss.add(boss2)
           Is_boss=True
        if Is_boss:
            sparke_boss.update()
            sparke_boss.draw(game_window)

            if boss.hp<=0 and STATE2==False:
                crash_sound.play()
                player.score+=2000
                OBSTACLE_MIN_INTERVAL = 2500 
                OBSTACLE_MAX_INTERVAL = 8000
                S_OBSTACLE_MIN_INTERVAL = 5000 
                S_OBSTACLE_MAX_INTERVAL = 10000
                MAX_SKYOB_HEIGHT =100
                MAX_SKYOB_BOTTOM =200
                obstacle_timer = 0
                s_obstacle_timer = 0
                Boss_defeated1=True
                Is_boss=False
            elif boss2.hp<=0:
                crash_sound.play()
                player.score+=5000
                obstacle_timer = 0
                s_obstacle_timer = 0
                Boss_defeated2=True
                Is_boss=False

        # Draw the score 
        jump_text = font2.render("JUMP REMAIN: " + str(10-player.jumps), True, (218,165,32))
        score_text = font2.render("SCORE: " + str(player.score), True, (255,223,0))
        bullet_text = font2.render("AMMO: " + str(player.bullet), True, (212,175,55))
        draw_bar(game_window, 10, 70, 10-player.jumps, 10)
        draw_bar(game_window, 10, 130, player.bullet, 25)
        game_window.blit(score_text, (10, 10))
        game_window.blit(jump_text, (10, 40))
        game_window.blit(bullet_text, (10, 100))
        pygame.display.update()
        clock.tick(60)

    # Game over screen
    else:
        if Is_first:
            game_window.blit(menu_image,(0,0))
            start_button.draw(game_window)
            quit_button.set_visibility(False)
            restart_button.set_visibility(False)
            rotated_image = title.update()
            game_window.blit(rotated_image, title.rect)
            pygame.display.flip()
            pygame.display.update()
        else:
            game_window.blit(menu_image,(0,0))
            game_over_text = font.render("GAME OVER! Your score is " + str(player.score), True, (255, 255, 255))
            game_window.blit(game_over_text, (350, 250))
            quit_button.set_visibility(True)
            restart_button.set_visibility(True)
            restart_button.draw(game_window)
            quit_button.draw(game_window)
            rotated_image = title.update()
            game_window.blit(rotated_image, title.rect)
            pygame.display.flip()
            pygame.display.update()

pygame.display.update()
pygame.quit()
sys.exit()