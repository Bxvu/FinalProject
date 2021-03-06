# sprite classes for game
# i used some ideas from CodePylet https://www.youtube.com/watch?v=osDofIdja6s&t=1038s
# i also borrowed pretty much all of this from kids can code - thanks!
# on acceleration https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/v/average-velocity-for-constant-acceleration 
# on vectors: https://www.youtube.com/watch?v=ml4NSzCQobk 


import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *

vec = pg.math.Vector2
class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
class Player(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group - thanks pygame!
        self._layer = PLAYER_LAYER
        # add player to game groups when instantiated
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.isDead = False
        self.deathJump = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.direction = "left"
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print("adding vecs " + str(self.vel + self.acc))
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(690, 406, 120, 201),
                                self.game.spritesheet.get_image(614, 1063, 120, 191)
                                ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                self.game.spritesheet.get_image(692, 1458, 120, 207)
                                ]
        '''setup left frames by flipping and appending them into an empty list'''
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.death_frame = self.game.spritesheet.get_image(382, 946, 150, 174)
        self.death_frame.set_colorkey(BLACK)
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if self.isDead:
            if self.deathJump == False:
                self.vel.y = 0
                self.vel.y = -15
                self.deathJump = True
        else:
            if keys[pg.K_a]:
                self.acc.x =  -PLAYER_ACC
                self.direction = "left"
            elif keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.direction = "right"
            else:
                self.direction = "up"
        # set player friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # jump to other side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    # cuts the jump short when the space bar is released
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        print("jump is working")
        # check pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # adjust based on checked pixel
        self.rect.y -= 2
        # only allow jumping if player is on platform
        if hits and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        #only does other animations if player is not dead
        if self.isDead:
            self.image = self.death_frame
            self.rect = self.image.get_rect()
            # self.rect.bottom = bottom
        else:
            if self.vel.x != 0:
                self.walking = True
            else:
                self.walking = False
            if self.walking:
                if now - self.last_update > 200:
                    self.last_update = now
                    '''
                    assigns current frame based on the next frame and the remaining frames in the list.
                    If current frame is 'two' in a list with three elements, then:
                    2 + 1 = 3; 3 modulus 3 is zero, setting the animation back to its first frame.
                    If current frame is zero, then:
                    0 + 1 = 1; 1 modulus 3 is 1; 2 modulus 3 is 2; 3 modulus 3 is o

                    '''
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    bottom = self.rect.bottom
                    if self.vel.x > 0:
                        self.image = self.walk_frames_r[self.current_frame]
                    else:
                        self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            # checks state
            if not self.jumping and not self.walking:
                # gets current delta time and checks against 200 miliseconds
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    # reset bottom for each frame of animation
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        # collide will find this property if it is called self.mask
        self.mask = pg.mask.from_surface(self.image)
#carrots that go up and kill enemies
class Carrot(Sprite):
    def __init__(self, game, playerPosX, playerPosY, carrotAmount, direction):
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.carrots
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((78,70))
        self.image = self.game.spritesheet.get_image(820, 1733, 78, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = playerPosX
        self.rect.centery = playerPosY + 5
        self.image = pg.transform.rotate(self.image,randint(0,360))
        self.carrotAmount = carrotAmount
        #direction where the carrots move
        if direction == "right":
            if self.carrotAmount == 1:
                self.carrotMoveY = randint(0,0) 
                self.carrotMoveX = 10     
            elif self.carrotAmount > 1:
                self.carrotMoveY = randint(-3,3)
                self.carrotMoveX = randint(8,12)        
            elif self.carrotAmount > 5:
                self.carrotMoveY = randint(-12,12)
                self.carrotMoveX = randint(6,14) 
            elif self.carrotAmount > 7:
                self.carrotMoveY = randint(-30,30)
                self.carrotMoveX = randint(4,16) 
        elif direction == "left":
            if self.carrotAmount == 1:
                self.carrotMoveY = randint(0,0) 
                self.carrotMoveX = -10     
            elif self.carrotAmount > 1:
                self.carrotMoveY = randint(-3,3)
                self.carrotMoveX = -(randint(8,12))        
            elif self.carrotAmount > 5:
                self.carrotMoveY = randint(-12,12)
                self.carrotMoveX = -(randint(6,14))
            elif self.carrotAmount > 7:
                self.carrotMoveY = randint(-30,30)
                self.carrotMoveX = -(randint(4,16)) 
        else:
            if self.carrotAmount == 1:
                self.carrotMoveX = randint(0,0) 
                self.carrotMoveY = 10     
            elif self.carrotAmount > 1:
                self.carrotMoveX = randint(-3,3)
                self.carrotMoveY = randint(8,12)        
            elif self.carrotAmount > 5:
                self.carrotMoveX = randint(-12,12)
                self.carrotMoveY = randint(6,14) 
            elif self.carrotAmount > 7:
                self.carrotMoveX = randint(-30,30)
                self.carrotMoveY = randint(4,16) 
    def update(self):
        self.rect.y += -self.carrotMoveY
        self.rect.x += self.carrotMoveX
        self.image = pg.transform.rotate(self.image,0)
        #kills carrots of they go off screen
        if self.rect.top < -40 or self.rect.bottom > HEIGHT + 40:
            self.kill()
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
# shield which protects player from enemies and their attacks
class Shield(Sprite):
    def __init__(self, game, player):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.shield
        Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = self.game.spritesheet.get_image(0, 1662, 211, 215)
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.player.rect.centerx
        self.rect.bottom = self.player.rect.top
        self.rect.x = self.player.rect.x - 55
        self.rect.y = self.player.rect.y - 35
        self.last_update = 0
        self.spawn_Animation = True
        self.sizeX = 20
        self.sizeY = 20
        self.health = 1
    def update(self):
        # only does spawn animation at the beginning
        if self.spawn_Animation == True:
            now = pg.time.get_ticks()
            if now - self.last_update > 25:
                self.last_update = now  
                self.image = self.game.spritesheet.get_image(0, 1662, 211, 215)
                self.image = pg.transform.scale(self.image, (self.sizeX, self.sizeY))
                self.rect = self.image.get_rect()
                self.rect.centerx = self.player.rect.centerx
                self.rect.bottom = self.player.rect.top
                self.sizeX += 10
                self.sizeY += 10
                self.image.set_colorkey(BLACK)
                self.rect.bottom = self.player.rect.top
                self.rect.x = self.player.rect.x - 40
                self.rect.y = self.player.rect.y - 15
                if self.sizeX >= 140:
                    self.sizeX = 140
                    self.sizeY = 140
                    self.spawn_Animation = False
        if self.spawn_Animation == False:
            if self.health > 0:
                self.rect.bottom = self.player.rect.top
                self.rect.x = self.player.rect.x - 35
                self.rect.y = self.player.rect.y - 15
                now = pg.time.get_ticks()
                if now - self.last_update > 100:
                    self.last_update = now     
                    self.image = pg.transform.rotate(self.image, 90)
            else:
                self.kill()
# background decorations
class Cloud(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = CLOUD_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.clouds
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange (50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), 
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.speed = randrange(1,3)
    def update(self):
        if self.rect.top > HEIGHT * 2: 
            self.kill
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width
class Platform(Sprite):
    def __init__(self, game, zone, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        imagesGrass = [self.game.spritesheet.get_image(0, 288, 380, 94), 
                  self.game.spritesheet.get_image(213, 1662, 201, 100),                 
                  ]
        imagesSnow = [self.game.spritesheet.get_image(0, 768, 380, 94),
                  self.game.spritesheet.get_image(213, 1764, 201, 100),
                  ]
        imagesSand = [self.game.spritesheet.get_image(0, 672, 380, 94),
                  self.game.spritesheet.get_image(208, 1879, 201, 100),
                  ]
        imagesStone = [self.game.spritesheet.get_image(0, 96, 380, 94),
                  self.game.spritesheet.get_image(382, 408, 200, 100),
                  ]
        imagesWood = [self.game.spritesheet.get_image(0, 960, 380, 94),
                  self.game.spritesheet.get_image(218, 1558, 200, 100)
                  ]
        if zone == "grass":
            self.image = random.choice(imagesGrass)
        elif zone == "wood":
            self.image = random.choice(imagesWood)
        elif zone == "sand":
            self.image = random.choice(imagesSand)
        elif zone == "snow":
            self.image = random.choice(imagesSnow)
        elif zone == "stone":
            self.image = random.choice(imagesStone)
        self.image.set_colorkey(BLACK)
        '''leftovers from random rectangles before images'''
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #chance to spawn powerups and decorations
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
        if random.randrange(100) < 75:
            Deco(self.game, self, zone)
            if random.randrange(100) < 75:
                Deco(self.game, self, zone)
#power ups
class Pow(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost', 'carrotsUpgrade', 'shield'])
        if len(self.game.shield) > 0:
            self.type = random.choice(['boost', 'carrotsUpgrade'])
        self.powerIcons = [self.game.spritesheet.get_image(820, 1805, 71, 70),
                    self.game.spritesheet.get_image(812, 554, 54, 49),
                    self.game.spritesheet.get_image(826, 134, 71, 70)
                    ]
        # sets images depending on type
        if self.type == 'boost':
            self.image = self.powerIcons[0]
        elif self.type == 'carrotsUpgrade':
            self.image = self.powerIcons[1]
        elif self.type == 'shield':
            self.image = self.powerIcons[2]
        else:
            self.image = self.powerIcons[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()
#decoration class for visuals 
class Deco(Sprite):
    def __init__(self, game, plat, zone):
        # allows layering in LayeredUpdates sprite group
        self._layer = CLOUD_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        imagesGrass = [self.game.spritesheet.get_image(868, 1877, 58, 57),
                    self.game.spritesheet.get_image(784, 1931, 82, 70),
                    self.game.spritesheet.get_image(623, 2005, 38, 41)
                                ]
        imagesWood = [self.game.spritesheet.get_image(534, 1063, 58, 57),
                    self.game.spritesheet.get_image(801, 752, 82, 70),
                    ]
        imagesSand = [self.game.spritesheet.get_image(707, 134, 117, 160),
                    self.game.spritesheet.get_image(534, 1063, 58, 57),
                    self.game.spritesheet.get_image(801, 752, 82, 70),
                    self.game.spritesheet.get_image(623, 2005, 38, 41)
                    ]
        imagesSnow = [self.game.spritesheet.get_image(623, 2005, 38, 41),
                    self.game.spritesheet.get_image(814, 1574, 81, 85),
                    self.game.spritesheet.get_image(812, 453, 81, 99)
                    ]
        imagesStone = [self.game.spritesheet.get_image(814, 1574, 81, 85),
                    self.game.spritesheet.get_image(812, 453, 81, 99),
                    self.game.spritesheet.get_image(623, 2005, 38, 41)
                    ]
        if zone == "grass":
            self.image = random.choice(imagesGrass)
        elif zone == "wood":
            self.image = random.choice(imagesWood)
        elif zone == "sand":
            self.image = random.choice(imagesSand)
        elif zone == "snow":
            self.image = random.choice(imagesSnow)
        elif zone == "stone":
            self.image = random.choice(imagesStone)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx - randint(-(self.plat.rect.width)/2,self.plat.rect.width/2)
        self.rect.bottom = self.plat.rect.top
    def update(self):
        self.rect.bottom = self.plat.rect.top
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()
# tried to add a background sprite that changes with score, ended up being too laggy
# class Background(Sprite):
#     def __init__(self, game, zone):
#         # allows layering in LayeredUpdates sprite group
#         self._layer = BACKGROUND_LAYER
#         # add Platforms to game groups when instantiated
#         self.groups = game.all_sprites
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = self.game.background_images
#         # if zone == "grass":
#         #     self.image = random.choice(imagesGrass)
#         # elif zone == "wood":
#         #     self.image = random.choice(imagesWood)
#         # elif zone == "sand":
#         #     self.image = random.choice(imagesSand)
#         # elif zone == "snow":
#         #     self.image = random.choice(imagesSnow)
#         # elif zone == "stone":
#         #     self.image = random.choice(imagesStone)
#         self.image.set_colorkey(BLACK)
#         '''leftovers from random rectangles before images'''
#         # self.image = pg.Surface((w,h))
#         # self.image.fill(WHITE)
#         self.rect = self.image.get_rect()
#         self.rect.x = 0
#         self.rect.y = 0
#     # def update(self):
#     #     self.image = self.game.background_images
#     #     self.image.set_colorkey(BLACK)
#     #     self.rect = self.image.get_rect()
#     #     self.rect.x = 0
#     #     self.rect.y = 0
#     #     self.kill()
#mob that moves horizontally
class Mob(Sprite):
    def __init__(self, game, score):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.last_update = 0
        self.image = self.images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT//1.1)
        self.vy = 0
        self.dy = 0.5
        self.current_frame = 0
        self.attackTimer = 0
        # mob attack speed increases with the score, to a maximum
        self.attackTimerCooldown = 2000 - score/20
        if self.attackTimerCooldown < 500:
            self.attackTimerCooldown = 500
        self.flyRange = 5 + score/2500
        if self.flyRange > 10:
            self.flyRange = 10
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > self.flyRange or  self.vy < -self.flyRange:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.animate()
        else:
            self.image = self.images[4]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        # timer for when mob will attack
        now = pg.time.get_ticks()
        if now - self.attackTimer > self.attackTimerCooldown:
            self.attackTimer = now
            MobAttack(self.game, self)
    def load_images(self):
        self.images = [self.game.spritesheet.get_image(382, 635, 174, 126),
                    self.game.spritesheet.get_image(0, 1879, 206, 107),
                    self.game.spritesheet.get_image(0, 1559, 216, 101),
                    self.game.spritesheet.get_image(0, 1456, 216, 101),
                    self.game.spritesheet.get_image(382, 510, 182, 123)
                                ]
        '''setup left frames by flipping and appending them into an empty list'''
        for frame in self.images:
            frame.set_colorkey(BLACK)
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now     
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
#attack for horizontal mob
class MobAttack(Sprite):
    def __init__(self, game, mob):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobAttacks
        Sprite.__init__(self, self.groups)
        self.game = game
        self.mob = mob
        self.image = self.game.spritesheet.get_image(894, 206, 51, 87)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.mob.rect.centerx
        self.rect.bottom = self.mob.rect.bottom + 5
    def update(self):
        # kills sprite if it goes off screen
        if self.rect.top > HEIGHT + 40:
            self.kill()
        else:
            self.rect.y += 10
#mob that moves vertically
class VerticalMob(Sprite):
    def __init__(self, game, playerX, score):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(692, 1667, 120, 132)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, HEIGHT + 100])
        self.rect_top = self.rect.top
        self.vy = randrange(1, 4)
        if self.rect.centery > HEIGHT:
            self.vy *= -1
        self.rect.x = randrange(WIDTH//1.1)
        self.vx = 0
        self.dx = 0.5
        if self.rect.x < playerX + 175 and self.rect.x > playerX - 175:
            self.kill()
        self.attackTimer = 0
        # mob attack speed that increases as the score increases, to a maximum
        self.attackTimerCooldown = 2000 - score/10
        if self.attackTimerCooldown < 500:
            self.attackTimerCooldown = 500
        self.flyRange = 3 + score/2500
        if self.flyRange > 10:
            self.flyRange = 10
    def update(self):
        self.rect.y += self.vy
        self.vx += self.dx
        self.rect_top = self.rect.top
        if self.vx > self.flyRange or  self.vx < -self.flyRange:
            self.dx *= -1
        center = self.rect.center
        if self.dx < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.x += self.vx
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        # spawns the attack
        now = pg.time.get_ticks()
        if now - self.attackTimer > self.attackTimerCooldown:
            self.attackTimer = now
            VerticalMobAttack(self.game, self)         
# attack for Vertical mob
class VerticalMobAttack(Sprite):
    def __init__(self, game, mob):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobAttacks
        Sprite.__init__(self, self.groups)
        self.game = game
        self.mob = mob
        self.image = self.game.spritesheet.get_image(894, 206, 51, 87)
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.rotate(self.image, 90)
        if randint(0,1) == 1:
            self.direction = "left"
            self.image =  pg.transform.flip(self.image, True, False )
        else:
            self.direction = "right" 
        self.rect = self.image.get_rect()
        self.rect.centerx = self.mob.rect.centerx
        self.rect.bottom = self.mob.rect.bottom + 5
    def update(self):
        # kills sprite if off screen
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        else:
            if self.direction == "right":
                self.rect.x += 10
            else:
                self.rect.x -= 10