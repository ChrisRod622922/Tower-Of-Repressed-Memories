# pylint: disable=import-error

''' TODO: - TITLE SCREEN, FOLLOWED BY SHORT EXPOSITION
          - Add menu option to toggle fullscreen mode
          - ALL SPRITES/TILES ARE TEMPORARY: Replace sprites, fonts and sounds eventually
          - Separate class modules into their own files
          - Game class needs more code moved to dedicated functions!!
'''

''' TODO:
          1. Nonkillable enemies (e.g. Lava) need to move in proportion to Timer
                    --- IN PROGRESS ---
          2. Add teleportation and follow ability for Stalkers
          3. Add screen effects and artifacts
          4. Add text updates on status effects (such as "Speed decreased due to lack of focus!")
          5. Restart current level on death, instead of restarting game
          6. TEST all functionality in test level.
             Create Level 1 layout / loop music logic
          7. Add background images and v. parallax
             If possible, a fuzzy dreamlike animated BG would be awesome
          8. Add fall damage
          9. Continue with other levels
         10. To-do list above
         11. Display actual hearts for Hearts (instead of numbers)
         12. Save points?
         13. Add animated sprites (improved sprites) if time allows
         14. (Opt.) Edit music and then try controlling tempo with Timer count
'''

''' TODO: LEVELS (planning):
          NOTE: map out in Photoshop or other editor where you can use a grid
          1. Escape from rising lava
          2. Shrinking level (spikes closing in on sides of screen)
          3. Blocks randomly fall OR there are ice blocks; instakill enemy is simply this

    NOTE:
        -- Anxiety and paranoia max value = 100
             
'''

# Imports
import pygame
import json
import os
import sys
import random
import time

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS + '/'
else:
    application_path = os.path.dirname(__file__) + '/'


# Initialize Pygame sound
pygame.mixer.pre_init()
pygame.init()

# Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Tower of Repressed Memories"
FPS = 30

#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)


# Helper functions for loading assets
def load_font(font_face, font_size):
    return pygame.font.Font(application_path + font_face, font_size)

def load_image(path):
    return pygame.image.load(application_path + path).convert_alpha()

def flip_image(img):
    return pygame.transform.flip(img, 1, 0)

def load_sound(path):
    return pygame.mixer.Sound(application_path + path)

# Helper functions for playing music
def play_music():
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()


# Colors
TRANSPARENT = (0, 0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (0, 255, 255)
BLUE = (0, 64, 255)
PURPLE = (128, 0, 255)
GREEN = (64, 255, 0)
ORANGE = (255, 128, 0)
GRAY = (91, 91, 91)
BABY_BLUE = (185, 209, 247)
SKY_BLUE = (0, 200, 225)
BRIGHT_GREEN = (0, 200, 0)
STORMY_BLUE =  (114, 144, 169)

# Fonts
font_xs = load_font("assets/fonts/TheConfessionRegular-YBpv.ttf", 16)
font_sm = load_font("assets/fonts/TheConfessionRegular-YBpv.ttf", 32)
font_md = load_font("assets/fonts/TheConfessionRegular-YBpv.ttf", 48)
font_lg = load_font("assets/fonts/TheConfessionRegular-YBpv.ttf", 64)
font_xl = load_font("assets/fonts/ToThePointRegular-n9y4.ttf", 80)

# Sounds
gem_snd = load_sound('assets/sounds/gem.ogg')
complete_snd = load_sound('assets/sounds/complete.ogg')
win_snd = load_sound('assets/sounds/win.ogg')
lose_snd = load_sound('assets/sounds/lose.ogg')

# Images
idle = load_image('assets/images/character/platformChar_idle.png')
walk = [load_image('assets/images/character/platformChar_walk1.png'),
        load_image('assets/images/character/platformChar_walk2.png')]
jump = load_image('assets/images/character/platformChar_jump.png')
hurt = load_image('assets/images/character/platformChar_hurt.png')


# TODO: replace images with custom or more fitting images
player_images = { "idle_rt": idle,
                "walk_rt": walk,
                "jump_rt": jump,
                "hurt_rt": hurt,
                "idle_lt": flip_image(idle),
                "walk_lt" : [flip_image(img) for img in walk],
                "jump_lt": flip_image(jump),
                "hurt_lt": flip_image(hurt) }
             
tile_images = { "Grass": load_image('assets/images/tiles/platformPack_tile001.png'),
                "Platform": load_image('assets/images/tiles/platformPack_tile041.png'),
                "Red_Platform": load_image('assets/images/tiles/platformPack_tile020.png'),
                "Sand": load_image('assets/images/tiles/platformPack_tile002.png'),
                "Dirt": load_image('assets/images/tiles/platformPack_tile004.png'),
                "Lava_Surface": load_image('assets/images/tiles/platformPack_tile006.png'),
                "Lava": load_image('assets/images/tiles/platformPack_tile018.png'),
                "Lamp": load_image('assets/images/tiles/lamp.png'),
                "Door": load_image('assets/images/tiles/platformPack_tile048.png') }
        
slime_enemy_images = [ load_image('assets/images/enemy/platformPack_tile024a.png'),
                       load_image('assets/images/enemy/platformPack_tile024b.png') ]

terror_enemy_images = [ load_image('assets/images/enemy/platformPack_tile011a.png'),
                          load_image('assets/images/enemy/platformPack_tile011b.png') ]

stalker_enemy_images = [ load_image('assets/images/enemy/platformPack_tile044.png'),
                          load_image('assets/images/enemy/platformPack_tile044.png') ]

nonkillable_enemy_images = [ load_image('assets/images/enemy/Lava.png') ]

item_images = { "Gem": load_image('assets/images/item/platformPack_item008.png'),
                "Stress_Ball": load_image('assets/images/item/platformPack_item010.png'),
                "Calming_Gem": load_image('assets/images/item/platformPack_item007.png'),
                "Magic_Strawberry": load_image('assets/images/item/platformPack_item006.png') }

# Levels
levels = ["assets/levels/level_1.json"]
# More levels here...
    

''' Sprites '''
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


''' Player '''
class Player(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()

        # Init variables
        self.images = images
        self.image = images["idle_rt"]
        self.rect = self.image.get_rect()

        self.speed = 10
        self.jump_power = 26
        self.vx = 0
        self.vy = 0

        self.inverse = False

        self.hearts = 5
        self.anxiety = 0 #max=100
        self.paranoia = 0 #max=100
        self.focus = 100
        self.adrenaline = 0

        self.adrenaline_timer = 0
        self.hurt_timer = 0
        self.speed_timer = 0
    
        self.reached_goal = False

        self.score = 0
        self.high_score = 0

        self.facing_right = True
        self.steps = 0
        self.step_rate = 4
        self.walk_index = 0
        
    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    # Animation speed
    def step(self):
        self.steps = (self.steps + 1) % self.step_rate

        if self.steps == 0:
            self.walk_index = (self.walk_index + 1) % len(self.images['walk_rt'])
        
    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False
        self.step()
    
    def move_right(self):
        self.vx = self.speed
        self.facing_right = True
        self.step()

    ''' Debugging function '''
    def move_up(self):
        self.vy = -self.speed
        self.step()

    ''' Debugging function '''
    def move_down(self):
        self.vy = self.speed
        self.step()
        
    def stop(self):
        self.vx = 0

    # Prevent clipping through tile if directly above Player
    def can_jump(self, tiles):
        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        self.rect.y -= 2

        return len(hit_list) > 0
        
    def jump(self, tiles):
        if self.can_jump(tiles):
            self.vy = -self.jump_power

    def apply_gravity(self, level):
        self.vy += level.gravity

        if self.vy > level.terminal_velocity:
            self.vy = level.terminal_velocity

    def adrenaline_cooldown(self):
        if self.adrenaline_timer > 0:
            self.adrenaline_timer -= 1
        else:
            self.speed += self.adrenaline
            self.adrenaline_timer = (FPS * 5)
            self.adrenaline = 0
            
    # Movement and tile collision detection
    def move_and_check_tiles(self, level):
        if self.inverse == False:
            
            self.rect.x += self.vx
            hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

            for hit in hit_list:
                if self.vx > 0:
                    self.rect.right = hit.rect.left
                elif self.vx < 0:
                    self.rect.left = hit.rect.right
                self.vx = 0
                    
            self.rect.y += self.vy
            hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

            for hit in hit_list:
                if self.vy > 0:
                    self.rect.bottom = hit.rect.top
                elif self.vy < 0:
                    self.rect.top = hit.rect.bottom
                self.vy = 0
                
        # Reverse movement
        elif self.inverse == True:
            
            self.rect.x -= self.vx
            hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

            for hit in hit_list:
                if self.vx > 0:
                    self.rect.right = hit.rect.left
                elif self.vx < 0:
                    self.rect.left = hit.rect.right
                self.vx = 0
                    
            self.rect.y += self.vy
            hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

            for hit in hit_list:
                if self.vy > 0:
                    self.rect.bottom = hit.rect.top
                elif self.vy < 0:
                    self.rect.top = hit.rect.bottom
                self.vy = 0

    def process_items(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.items, True)

        for hit in hit_list:
            # Assign item's values to Player variables, such as anxiety and paranoia
            print("Before hit anxiety: " + str(self.anxiety) + ". Paranoia: " + str(self.paranoia))
            hit.apply(self)
            print("After hit anxiety: " + str(self.anxiety) + ". Paranoia: " + str(self.paranoia))

    # Enemy collision detection
    def process_enemies(self, level):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        else:
            hit_list = pygame.sprite.spritecollide(self, level.enemies, False)
            for hit in hit_list:
                # Use same logic as items for individual collision. Ensures correct num of hearts is deduced
                hit.apply(self)
                self.hurt_timer = FPS

    # Process collisions with nonkillable enemy hitboxes
    def process_hitboxes(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.hitboxes, False)
        for hit in hit_list:
            hit.apply(self)
            self.adrenaline_cooldown()
    
    # Screen edges collision detection
    def check_world_edges(self, level):
        ''' Horizontal detection '''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width

        ''' Vertical detection '''
        if self.rect.top > level.height:
            self.hearts = 0

    # Checks conditions for core variables that may affect player speed or produce screen artifacts
    def check_variables(self):
        ''' Conditions for anxiety, paranoia, focus thresholds '''
        # If anxiety is past a threshold, inverse player controls and invoke vignette screen effect
        if self.anxiety > 25 and self.anxiety < 75:
            self.inverse = False
            Game.create_vignette(self)
        elif self.anxiety == 75:
            self.inverse = True

        # If paranoia is past a threshold, randomly spawn fake items and screen artifacts
        if self.paranoia == 25:
            Game.create_screen_artifacts(self)

        # If focus below a certain threshold, slow Player speed
        if self.speed_timer > 0:
            self.speed_timer -= 1
        else:
            # Speed timer used to accurately decrement player speed as described below
            if self.focus == 50:
                self.speed -= 2
                self.speed_timer = FPS
                print("Speed: " + str(self.speed))
            elif self.focus == 25:
                self.speed -= 3
                self.speed_timer = FPS
                print("Speed: " + str(self.speed))

    def check_goal(self, level):
        self.reached_goal = level.goal.contains(self.rect)

    # Animation
    def set_image(self):
        if self.facing_right:
            idle = self.images['idle_rt']
            walk = self.images['walk_rt']
            jump = self.images['jump_rt']
            hurt = self.images['hurt_rt']
        else:
            idle = self.images['idle_lt']
            walk = self.images['walk_lt']
            jump = self.images['jump_lt']
            hurt = self.images['hurt_lt']

        if self.hurt_timer > 0:
            self.image = hurt
        elif self.vy != 0:
            self.image = jump
        elif self.vx == 0:
            self.image = idle
        else:
            self.image = walk[self.walk_index]
            
    def update(self, level):
        self.apply_gravity(level)
        self.move_and_check_tiles(level)
        self.check_world_edges(level)
        self.process_items(level)
        self.process_enemies(level)
        self.process_hitboxes(level)
        self.check_variables()
        self.check_goal(level)
        self.set_image()


''' Enemies '''
class MindSlimeEnemy(pygame.sprite.Sprite):
    '''
    Mind Slime enemies move only in one direction, turning around whenever
    they hit a block or the edge of the world. They can walk off platforms.
    '''
    
    def __init__(self, x, y, images):
        super().__init__()

        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vx = -4
        self.vy = 0

        self.steps = 0
        self.step_rate = 6
        self.walk_index = 0

        self.score_value = -10
        self.heart_value = -2
        self.anxiety_value = 5
        self.paranoia_value = 0
        self.adrenaline_value = 0

    # Apply negative effects to Player upon collision (such as -Hearts)
    def apply(self, player):
        player.score += self.score_value
        player.hearts += self.heart_value
        player.anxiety += self.anxiety_value
        player.paranoia += self.paranoia_value
        player.adrenaline += self.adrenaline_value
        
    def reverse(self):
        self.vx = -1 * self.vx
        
    def apply_gravity(self, level):
        self.vy += level.gravity

        if self.vy > level.terminal_velocity:
            self.vy = level.terminal_velocity

    def move_and_check_tiles(self, level):
        # Horizontal tile check
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

        for hit in hit_list:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
            self.should_reverse = True

        # Vertical tile check, e.g., if enemy falls off platform
        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

        for hit in hit_list:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0
            
    def check_world_edges(self, level):
        # Horizontal
        if self.rect.left < 0:
            self.rect.left = 0
            self.should_reverse = True
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.should_reverse = True

        # Vertical
        if self.rect.top > level.height:
            self.kill()
        
    # Animation speed
    def step(self):
        self.steps = (self.steps + 1) % self.step_rate

        if self.steps == 0:
            self.walk_index = (self.walk_index + 1) % len(self.images)

    def set_image(self):
        self.image = self.images[self.walk_index]
        
    def update(self, level):
        self.should_reverse = False
        
        self.apply_gravity(level)
        self.move_and_check_tiles(level)
        self.check_world_edges(level)
        
        if self.should_reverse:
            self.reverse()
            
        self.step()
        self.set_image()

            
class TerrorEnemy(MindSlimeEnemy):
    '''
    Terror enemies behave the same as Mind Slimes, except
    that they will turn around on platform edges.
    '''
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.score_value = -10
        self.heart_value = -1
        self.anxiety_value = 5
        self.paranoia_value = 0
        self.adrenaline_value = 0

    ''' Override this function '''
    def move_and_check_tiles(self, level):
        #reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

        for hit in hit_list:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
            self.should_reverse = True

        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)
        
        on_platform = False

        for hit in hit_list:
            if self.vy >= 0:
                self.rect.bottom = hit.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= hit.rect.right:
                    on_platform = True
                elif self.vx < 0 and self.rect.left >= hit.rect.left:
                    on_platform = True

            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
                self.vy = 0

        if not on_platform:
            self.should_reverse = True


class StalkerEnemy(TerrorEnemy):
    '''
    Stalkers can jump, are faster, and can follow the Player.
    '''
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vx = -6
        self.vy = 0
        self.jump_power = 20

        self.steps = 0
        self.step_rate = 6
        self.walk_index = 0

        self.score_value = -10
        self.heart_value = -2
        self.anxiety_value = 5
        self.paranoia_value = 5
        self.adrenaline_value = 0

    # Prevent clipping
    def can_jump(self, tiles):
        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        self.rect.y -= 2

        return len(hit_list) > 0
        
    # TODO: jump at random (function needs to be called somewhere at random)
    def jump(self, tiles):
        if self.can_jump(tiles):
            self.vy = -self.jump_power

    # TODO: find way to get player coordinates
    def follow_player(self, player):
        pass

    ''' Override update function '''
    # TODO: update jump and follow functions
    def update(self, level):
        self.should_reverse = False
        
        self.apply_gravity(level)
        self.move_and_check_tiles(level)
        self.check_world_edges(level)
        
        if self.should_reverse:
            self.reverse()
            
        self.step()
        self.set_image()


class RisingLava(pygame.sprite.Sprite):
    '''
    Non-killable enemy. Moves up as the Timer depletes.
    '''
    def __init__(self, x, y, images):
        super().__init__()

        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # TODO: speed should be proportional to time left on Timers
        self.vy = 1

        self.steps = 0
        self.step_rate = 1
        self.walk_index = 0

        self.score_value = 0
        self.heart_value = -999
        self.anxiety_value = 0
        self.paranoia_value = 0
        self.adrenaline_value = 0

    # Apply negative effects to Player upon collision (such as -Hearts)
    def apply(self, player):
        player.score += self.score_value
        player.hearts += self.heart_value
        player.anxiety += self.anxiety_value
        player.paranoia += self.paranoia_value
        player.adrenaline += self.adrenaline_value
    
    def move(self, level):
        self.rect.y -= self.vy

    def set_image(self):
        self.image = self.images[0]

    def update(self, level):
        self.move(level)
        self.set_image()
        

class LavaHitbox(pygame.sprite.Sprite):
    '''
    This class simply provides a rect that the Player can collide with that 
    is slightly raised or close to the RisingLava enemy type so that adrenaline may increase.
    '''
    
    def __init__(self, x, y):
        super().__init__()

        self.rect = pygame.Rect(x, (y-100), 1280, 1)

        self.vy = 1

        self.steps = 0
        self.step_rate = 1
        self.walk_index = 0

        self.score_value = 0
        self.heart_value = 0
        self.anxiety_value = 0
        self.paranoia_value = 0
        self.adrenaline_value = 5

    def apply(self, player):
        player.score += self.score_value
        player.hearts += self.heart_value
        player.anxiety += self.anxiety_value
        player.paranoia += self.paranoia_value
        player.adrenaline += self.adrenaline_value
    
    def move(self, level):
        self.rect.y -= self.vy

    def update(self, level):
        self.move(level)


''' Items '''
class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Values to add to the Player class
        self.score_value = 100
        self.heart_value = 0
        self.anxiety_value = 0
        self.paranoia_value = 0

    def apply(self, player):
        gem_snd.play()
        player.score += self.score_value
        player.hearts += self.heart_value
        player.anxiety += self.anxiety_value
        player.paranoia += self.paranoia_value
        
    def update(self, level):
        ''' No animation yet, so nothing needs to be updated '''
        pass


class StressBall(Gem):
    ''' Only values need to be overridden '''
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Values to add to the Player class
        self.score_value = 25
        self.heart_value = 0
        self.anxiety_value = -10
        self.paranoia_value = 0


class CalmingGem(Gem):
    ''' Only values need to be overridden '''
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Values to add to the Player class
        self.score_value = 25
        self.heart_value = 0
        self.anxiety_value = 0
        self.paranoia_value = -10


class MagicStrawberry(Gem):
    ''' Only values need to be overridden '''
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Values to add to the Player class
        self.score_value = 50
        self.heart_value = 1
        self.anxiety_value = -5
        self.paranoia_value = -5


''' Level '''
class Level():
    def __init__(self, file_path):
        with open(application_path + file_path, 'r') as f:
            data = f.read()

        # Load data from JSON file
        self.map_data = json.loads(data)

        # Default timer, 5 min
        self.timer = 300

        self.load_layout()
        self.load_music()
        self.load_background()
        self.load_physics()
        self.load_timer()
        self.load_tiles()
        self.load_items()
        self.load_enemies()
        self.load_hitboxes()
        self.load_goal()
        
        self.generate_layers()
        self.prerender_inactive_layers()

    # Define level layout based on definition in JSON file
    def load_layout(self):
        self.scale =  self.map_data['layout']['scale']
        self.width =  self.map_data['layout']['size'][0] * self.scale
        self.height = self.map_data['layout']['size'][1] * self.scale
        self.start_x = self.map_data['layout']['start'][0] * self.scale
        self.start_y = self.map_data['layout']['start'][1] * self.scale

    def load_music(self):
        pygame.mixer.music.load(application_path + self.map_data['music'])
        
    def load_physics(self):
        self.gravity = self.map_data['physics']['gravity']
        self.terminal_velocity = self.map_data['physics']['terminal_velocity']

    def load_timer(self):
        self.timer = self.map_data['timer']['time']
        return self.timer

    # Load backgrounds as defined in file if it exists in file path
    def load_background(self):
        self.bg_color = self.map_data['background']['color']
        path1 = self.map_data['background']['image1']
        path2 = self.map_data['background']['image2']

        # If images defined in file does not exist, don't use a BG image
        if os.path.isfile(application_path + path1):
            self.bg_image1 = pygame.image.load(application_path + path1).convert_alpha()
        else:
            self.bg_image1 = None

        if os.path.isfile(application_path + path2):
            self.bg_image2 = pygame.image.load(application_path + path2).convert_alpha()
        else:
            self.bg_image2 = None

        self.parallax_speed1 = self.map_data['background']['parallax_speed1']
        self.parallax_speed2 = self.map_data['background']['parallax_speed2']
        
    def load_tiles(self):
        self.midground_tiles = pygame.sprite.Group()
        self.main_tiles = pygame.sprite.Group()
        self.foreground_tiles = pygame.sprite.Group()

        for group_name in self.map_data['tiles']:
            tile_group = self.map_data['tiles'][group_name]
            
            # Scale tiles based on size defined in level file
            for element in tile_group:
                x = element[0] * self.scale
                y = element[1] * self.scale
                kind = element[2]

                t = Tile(x, y, tile_images[kind])

                if group_name == 'midground':
                    self.midground_tiles.add(t)
                elif group_name == 'main':
                    self.main_tiles.add(t)
                elif group_name == 'foreground':
                    self.foreground_tiles.add(t)
            
    def load_items(self):
        self.items = pygame.sprite.Group()
        
        # Find item element in level JSON file and create items as defined there
        for element in self.map_data['items']:
            x = element[0] * self.scale
            y = element[1] * self.scale
            kind = element[2]
            
            if kind == "Gem":
                s = Gem(x, y, item_images[kind])
            elif kind == "Stress_Ball":
                s = StressBall(x, y, item_images[kind])
            elif kind == "Calming_Gem":
                s = CalmingGem(x, y, item_images[kind])
            elif kind == "Magic_Strawberry":
                s = MagicStrawberry(x, y, item_images[kind])
                
            self.items.add(s)

    def load_enemies(self):
        self.enemies = pygame.sprite.Group()
        
        for element in self.map_data['enemies']:
            x = element[0] * self.scale
            y = element[1] * self.scale
            kind = element[2]
            
            if kind == "MindSlime":
                s = MindSlimeEnemy(x, y, slime_enemy_images)
            elif kind == "Terror":
                s = TerrorEnemy(x, y, terror_enemy_images)
            elif kind == "Stalker":
                s = StalkerEnemy(x, y, stalker_enemy_images)
            elif kind == "Rising_Lava":
                s = RisingLava(x, y, nonkillable_enemy_images)
                
            self.enemies.add(s)

    def load_hitboxes(self):
        self.hitboxes = pygame.sprite.Group()

        for element in self.map_data['hitboxes']:
            x = element[0] * self.scale
            y = element[1] * self.scale
            kind = element[2]

            if kind == "Lava_Hitbox":
                s = LavaHitbox(x, y)

            self.hitboxes.add(s)

    def load_goal(self):
        g = self.map_data['layout']['goal']

        if isinstance(g, int):
            x = g * self.scale
            y = 0
            w = self.width - x
            h = self.height
        elif isinstance(g, list):
            x = g[0] * self.scale
            y = g[1] * self.scale
            w = g[2] * self.scale
            h = g[3] * self.scale

        self.goal = pygame.Rect([x, y, w, h])

    # Define PyGame surfaces for rendering based on the data read from the file
    def generate_layers(self):
        self.world = pygame.Surface([self.width, self.height])
        self.background1 = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.background2 = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.foreground = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

    def tile_image(self, img, surf):
        surface_width = surf.get_width()
        surface_height = surf.get_height()
        img_width = img.get_width()
        img_height = img.get_height()
        
        for x in range(0, surface_width, img_width):
            y = surface_height - img_height
            surf.blit(img, [x, y])
                
    # Prerender elements off screen (parallax only)
    def prerender_inactive_layers(self):
        self.background1.fill(self.bg_color)
        
        if self.bg_image1 != None:
            self.tile_image(self.bg_image1, self.background1)
            
        if self.bg_image2 != None:
            self.tile_image(self.bg_image2, self.background2)
                    
        self.midground_tiles.draw(self.inactive)
        self.main_tiles.draw(self.inactive)        
        self.foreground_tiles.draw(self.foreground)


''' Game class '''
class Game():

    ''' Game Stages '''
    START = 0
    PLAYING = 1
    CLEARED = 2
    WIN = 3
    LOSE = 4
    PAUSE = 5
    DEBUG = 6

    def __init__(self, levels):
        # Initial variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.levels = levels
        self.level_change_delay = 90
        self.cleared_timer = self.level_change_delay

        # Default time variables
        self.timer = 300
        self.initial_time = self.timer
        self.timer_count_time = 0
        self.max_value_a_p = 100
    
    def setup(self):
        # Create player
        self.player = Player(player_images)
        self.mc = pygame.sprite.GroupSingle()
        self.mc.add(self.player)

        # Set stage and start loading first level
        self.stage = Game.START
        self.current_level = 1
        self.load_level()

        # Retrieve High Score if it exists
        if not os.path.exists(application_path + 'assets/high_score/high_score.txt'):
            with open(application_path + '/assets/high_score/high_score.txt', 'w') as f:
                f.write(str(self.player.high_score))
            f.close()
        high_score_file = open(application_path + '/assets/high_score/high_score.txt', 'r')
        self.player.high_score = int(high_score_file.readline())
        high_score_file.close()

    def load_level(self):
        # Track current level and update variables based on level data
        level_index = self.current_level - 1
        level_data = self.levels[level_index] 
        self.level = Level(level_data)

        self.timer = self.level.load_timer()
        self.initial_time = self.timer
        # Calculate the rate of increase for anxiety and paranoia
        self.rate = self.max_value_a_p / (self.initial_time / 2)

        # Move Player to starting coordinates as defined in level file
        self.player.move_to(self.level.start_x, self.level.start_y)
        self.player.reached_goal = False

        # Group active sprites for drawing
        self.active_sprites = pygame.sprite.Group()
        self.active_sprites.add(self.player, self.level.items, self.level.enemies)

        # Define hitbox for level's nonkillable object
        self.hitbox = self.level.hitboxes

    def start_level(self):
        play_music()
        self.stage = Game.PLAYING
            
    def advance(self):
        # Advance to next level if not at the end of level list
        if self.current_level < len(self.levels):
            complete_snd.play()
            self.current_level += 1
            self.load_level()
            self.start_level()
        else:
            self.stage = Game.WIN
            win_snd.play()

    ''' Calculation for moving tiles based on Player position '''
    def calculate_offset(self):
        x = 0
        y = -1 * self.player.rect.centery + SCREEN_HEIGHT / 2

        ''' Vertical offset '''
        if self.player.rect.centery < SCREEN_HEIGHT / 2:
            y = 0
        elif self.player.rect.centery > self.level.height - SCREEN_HEIGHT / 2:
            y = -1 * self.level.height + SCREEN_HEIGHT

        return round(x), round(y)

    ''' Screens '''
    def show_title_screen(self):
        text = font_xl.render(TITLE, 1, WHITE, pygame.SRCALPHA)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = 320
        screen.blit(text, rect)
        
        text = font_md.render("Press SPACE to start!", 1, WHITE, pygame.SRCALPHA)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = 380
        screen.blit(text, rect)
        
    def show_cleared_screen(self):
        text = font_lg.render("Level cleared!", 1, TURQUOISE, pygame.SRCALPHA)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = 360
        screen.blit(text, rect)

    def show_win_screen(self):
        text = font_lg.render("You win!", 1, TURQUOISE, pygame.SRCALPHA)
        text2 = font_md.render("Press SPACE to play again or ESC to exit!", 1, WHITE, pygame.SRCALPHA)
        rect = text.get_rect()
        rect2 = text2.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = 330
        rect2.centerx = SCREEN_WIDTH // 2
        rect2.centery = 380
        screen.blit(text, rect)
        screen.blit(text2, rect2)

    def show_lose_screen(self):
        text = font_lg.render("YOU ARE DEAD.", 1, RED, pygame.SRCALPHA)
        text2 = font_md.render("Press SPACE to play again or ESC to exit.", 1, WHITE, pygame.SRCALPHA)
        rect = text.get_rect()
        rect2 = text2.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = 330
        rect2.centerx = SCREEN_WIDTH // 2
        rect2.centery = 380
        screen.blit(text, rect)
        screen.blit(text2, rect2)

    def show_pause(self):
        t1 = font_lg.render("PAUSED", True, WHITE, pygame.SRCALPHA)
        t2 = font_md.render("(Press SPACE to resume.)", True, YELLOW, pygame.SRCALPHA)
        w1 = t1.get_width()
        w2 = t2.get_width()
        screen.blit(t1, [SCREEN_WIDTH/2 - w1/2, 330])
        screen.blit(t2, [SCREEN_WIDTH/2 - w2/2, 380])

    ''' HUD information '''
    def show_stats(self):
        # Define number of pixels to evenly space the elements on the screen
        spacing = SCREEN_WIDTH / 7

        level_str = "Level: " + str(self.current_level)
        
        text1 = font_sm.render(level_str, 1, YELLOW, pygame.SRCALPHA)
        rect1 = text1.get_rect()
        rect1.left = 24
        rect1.top = 24
        screen.blit(text1, rect1)
    
        score_str = "Score: " + str(self.player.score)
        
        text2 = font_sm.render(score_str, 1, YELLOW, pygame.SRCALPHA)
        rect2 = text2.get_rect()
        rect2.left = 24
        rect2.top = rect1.bottom + 10
        screen.blit(text2, rect2)

        timer_str = "Time: " + str(self.timer)
        
        text3 = font_sm.render(timer_str, 1, YELLOW, pygame.SRCALPHA)
        rect3 = text3.get_rect()
        rect3.right = SCREEN_WIDTH - 24
        rect3.top = 24
        screen.blit(text3, rect3)

        anxiety_str = "Anxiety: " + str(self.player.anxiety)

        text4 = font_sm.render(anxiety_str, 1, YELLOW, pygame.SRCALPHA)
        rect4 = text4.get_rect()
        rect4.left = (spacing * 3) - (rect4.width / 2)
        rect4.top = 24
        screen.blit(text4, rect4)

        paranoia_str = "Paranoia: " + str(self.player.paranoia)

        text5 = font_sm.render(paranoia_str, 1, YELLOW, pygame.SRCALPHA)
        rect5 = text5.get_rect()
        rect5.left = (spacing * 4) - (rect5.width / 2)
        rect5.top = 24
        screen.blit(text5, rect5)

        focus_str = "Focus: " + str(self.player.focus)

        text6 = font_sm.render(focus_str, 1, YELLOW, pygame.SRCALPHA)
        rect6 = text6.get_rect()
        rect6.left = (spacing * 5) - (rect6.width / 2)
        rect6.top = 24
        screen.blit(text6, rect6)

        hearts_str = "Hearts: " + str(self.player.hearts)

        text7 = font_sm.render(hearts_str, 1, YELLOW, pygame.SRCALPHA)
        rect7 = text7.get_rect()
        rect7.left = (spacing * 2) - (rect7.width / 2)
        rect7.top = 24
        screen.blit(text7, rect7)

        high_score_str = "High Score: " + str(self.player.high_score)

        text8 = font_sm.render(high_score_str, 1, YELLOW, pygame.SRCALPHA)
        rect8 = text8.get_rect()
        rect8.right = SCREEN_WIDTH - 24
        rect8.top = rect3.bottom + 10
        screen.blit(text8, rect8)

    ''' Create different intensity vignette screen effect depending on anxiety level '''
    def create_vignette(player):
        # Can even add floating text with updates like, "Panic induced!" when Player controls are inversed
        pass

    ''' Create distractions and distortions on screen when paranoia high '''
    def create_screen_artifacts(player):
        # Change amount depending on how high paranoia is
        pass

    ''' Update player score with leftover time on timer '''
    def update_final_score(self):
        while self.timer > 0:
            self.timer -= 1
            self.player.score += 1
            self.show_stats()

    ''' Update high score function '''
    def update_highscore(self):
        if self.player.score >= self.player.high_score:
            self.player.high_score = self.player.score

        with open(application_path + '/assets/high_score/high_score.txt', 'w') as f:
            f.write(str(self.player.high_score))


    ''' Input processing '''
    def process_input(self):     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if self.stage == Game.START:
                    if event.key == pygame.K_SPACE:
                        self.start_level()
                        
                elif self.stage == Game.PLAYING:
                    if event.key == pygame.K_UP:
                        self.player.jump(self.level.main_tiles)
                    elif event.key == pygame.K_r:
                        self.setup()
                    elif event.key == pygame.K_p:
                        self.stage = Game.PAUSE
                        pause_music()
                    elif event.key == pygame.K_d:
                        ''' Debug Mode '''
                        self.stage = Game.DEBUG

                elif self.stage == Game.PAUSE:
                    if event.key == pygame.K_SPACE:
                        self.stage = Game.PLAYING
                        unpause_music()

                elif self.stage == Game.WIN or self.stage == Game.LOSE:
                    if event.key == pygame.K_SPACE:
                        self.setup()

        pressed = pygame.key.get_pressed()
        
        if self.stage == Game.PLAYING or self.stage == Game.DEBUG:
            if pressed[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()
            elif pressed[pygame.K_UP] and self.stage == Game.DEBUG:
                self.player.move_up()
            elif pressed[pygame.K_DOWN] and self.stage == Game.DEBUG:
                self.player.move_down()
            else:
                self.player.stop()
     
    ''' Update Game functions, sprites, and variables '''
    def update(self):
        if self.stage == Game.PLAYING or self.stage == Game.DEBUG:
            self.active_sprites.update(self.level)
            self.hitbox.update(self.level)

            # Update timer
            self.timer_count_time += 1
            if self.timer > 0 and self.timer_count_time == FPS:
                self.timer -= 1
                self.timer_count_time = 0

            # Calculate timer-based increase
            timer_increase = self.rate * (self.initial_time - self.timer)

            # Update anxiety and paranoia based on elapsed time
            self.player.anxiety = (int)(min(self.max_value_a_p, timer_increase))
            self.player.paranoia = (int)(min(self.max_value_a_p, timer_increase))

            ''' TODO: WHY TF am I stuck???
                NOTE: Give up for now. '''

            # Update focus
            if self.player.focus > 0 and self.player.focus < 101:
                self.player.focus = (int)(100 - ((self.player.anxiety / 2) + (self.player.paranoia / 2)))

            # If any variables are negative, change to 0 before updating display
            # TODO: can move to own function
            if self.player.score < 0:
                self.player.score = 0
            if self.player.hearts < 0:
                self.player.hearts = 0
            if self.player.anxiety < 0:
                self.player.anxiety = 0
            if self.player.paranoia < 0:
                self.player.paranoia = 0
            if self.player.focus < 0:
                self.player.focus = 0
            if self.player.focus > 100:
                self.player.focus = 100

            # Refresh HUD in case any variables were indeed below 0
            self.show_stats()

            # End conditions
            if self.player.reached_goal:
                stop_music()
                self.stage = Game.CLEARED
            elif self.player.hearts <= 0 or self.timer <= 0:
                self.stage = Game.LOSE
                lose_snd.play()
                stop_music()

        # Delay timer for level advancement
        elif self.stage == Game.CLEARED:
            self.cleared_timer -= 1

            if self.cleared_timer == 0:
                self.advance()
            
    ''' Draw tiles, sprites, screens '''
    def render(self):
        self.level.active.fill([0, 0, 0, 0])
        self.active_sprites.draw(self.level.active)

        offset_x, offset_y = self.calculate_offset()
        bg1_offset_x = -1 * offset_x * self.level.parallax_speed1
        bg1_offset_y = -1 * offset_y * self.level.parallax_speed1
        bg2_offset_x = -1 * offset_x * self.level.parallax_speed2
        bg2_offset_y = -1 * offset_y * self.level.parallax_speed2
        
        self.level.world.blit(self.level.background1, [bg1_offset_x, bg1_offset_y])
        self.level.world.blit(self.level.background2, [bg2_offset_x, bg2_offset_y])
        self.level.world.blit(self.level.inactive, [0, 0])
        self.level.world.blit(self.level.active, [0, 0])
        self.level.world.blit(self.level.foreground, [0, 0])                  

        screen.blit(self.level.world, [offset_x, offset_y])

        self.show_stats()
        
        if self.stage == Game.START:
            self.show_title_screen()
        elif self.stage == Game.CLEARED:
            self.update_final_score()
            self.update_highscore()
            self.show_cleared_screen()
        elif self.stage == Game.WIN:
            self.show_win_screen()
        elif self.stage == Game.LOSE:
            self.update_highscore()
            self.show_lose_screen()
        elif self.stage == Game.PAUSE:
            self.show_pause()

        pygame.display.flip()
    

    def run(self):        
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

            
# Main
if __name__ == "__main__":
    g = Game(levels)
    g.setup()
    g.run()
    
    pygame.quit()
    sys.exit()