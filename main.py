# this file was created by Benthan Vu
# Sources: goo.gl/2KMivS, copied from Teacher Chris Cozort, pygame documentation

'''
**********Gameplay ideas:
shoot carrots up at enemy
shoot carrots left and right
platforms that change as you get a higher score
enemy that goes down instead of left and right
enemies shoot left right and down
enemies move faster and in larger areas as score gets higher
new power ups
carrot upgrades as you pick up more
shield powerup that blocks one enemy attack
background changes

**********Bugs
when you get launched by powerup or head jump player sometimes snaps to platform abruptly 
happens when hitting jump during power up boost
random "ghost" enemy that is not affected by anything and can't kill player with its attacks

**********Gameplay fixes
getting killed while being boosted

**********Features
upgrades for shooting carrots at enemies
enemies shoot stuff
picking up carrots lets you shoot more at once
if you have more than 3 carrots, you lose the carrots instead of dying
shield powerup
platforms and decorations on them change with higher scores

'''
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # init game window
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Jumpy Boi")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        ''' with is a contextual option that handles both opening and closing of files to avoid
        issues with forgetting to close
        '''
        try:
            # changed to r to avoid overwriting error
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET)) 
        #load cloud images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # self.background_images = pg.image.load(path.join(img_dir, 'grass.png'))
        # load sounds
        # great place for creating sounds: https://www.bfxr.net/
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))
        self.head_jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump39.wav'))
        # self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump39.wav'))
        # self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Woosh.wav'))
        # self.shoot_shound = pg.mixer.Sound()
    def new(self):
        # add score, the zone so platforms change, and cooldown for carrots
        self.score = 0
        self.zone = "grass"
        self.zoneRotation = 0
        self.changeInScore = 3000
        self.deathAnimation = False
        self.playerShootCooldown = 0
        self.playerShootCarrotAmount = 1
        self.timeSincePlayerShot = 0
        # add all sprites to the pg group
        # below no longer needed - using LayeredUpdate group
        # self.all_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        # create clouds group
        self.clouds = pg.sprite.Group()
        # add powerups
        self.powerups = pg.sprite.Group()
        self.carrots = pg.sprite.Group()
        self.shield = pg.sprite.Group()
        # mob attacks
        self.mobAttacks = pg.sprite.Group()
        # timers that doesn't let the sprite spawn until the timer is passed
        self.mob_timer = 0
        self.plat_timer = 0
        # add a player 1 to the group
        self.player = Player(self)
        # add mobs
        self.mobs = pg.sprite.Group()
        #invincibility when boosted so that you wont boost into an enemy and die
        self.boosted = False
        # no longer needed after passing self.groups in Sprites library file
        # self.all_sprites.add(self.player)        
        # instantiate new platform 
        for plat in PLATFORM_LIST:
            # spawn platforms in list from settings
            Platform(self, self.zone, *plat)
        # spawn clouds
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        # load music
        pg.mixer.music.load(path.join(self.snd_dir, 'YBSS.mp3'))
        # Background(self, self.zone)
        # call the run method
        self.run()
    def run(self):
        # game loop
        # play music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
    def update(self):
        self.all_sprites.update()
        #sees if the player has enough points to go to the next zone       
        if self.changeInScore < self.score:
            self.changeInScore = self.score + 3000
            print(self.changeInScore)
            self.zoneRotation += 1
            if self.zoneRotation == 0:
                self.zone = "grass"
                # Background(self, self.zone)
            elif self.zoneRotation == 1:
                self.zone = "wood"
                # Background(self, self.zone)
            elif self.zoneRotation == 2:
                self.zone = "sand"
            elif self.zoneRotation == 3:
                self.zone = "stone"
            elif self.zoneRotation == 4:
                self.zone = "snow"
            if self.zoneRotation >= 5:
                self.zoneRotation = 0
                self.zone = "grass"

        # spawns a mob when timer is passed
        now = pg.time.get_ticks()
        if now - self.mob_timer > 2000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            #random choice between spawning mobs
            if randint(0,1) == 0:
                Mob(self, self.score)
            else:
                VerticalMob(self, self.player.pos.x, self.score)
        ##### check for mob collisions ######
        # now using collision mask to determine collisions
        # can use rectangle collisions here first if we encounter performance issues
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            # can use mask collide here if mob count gets too high and creates performance issues
            if self.player.pos.y - 35 < mob_hits[0].rect_top and self.deathAnimation == False and self.boosted == False:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.head_jump_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.boosted = True
            else:
                #only kills player if they are not boosted
                if self.boosted == False:
                    print("player is " + str(self.player.pos.y))
                    print("mob is " + str(mob_hits[0].rect_top))
                    self.deathAnimation = True
                    self.player.isDead = True
                    # self.death_sound.play()
                    # self.playing = False
        mobAttack_hits = pg.sprite.spritecollide(self.player, self.mobAttacks, False, pg.sprite.collide_mask)
        if mobAttack_hits:
        #         #only kills player if they are not boosted
                if self.boosted == False:
                    self.deathAnimation = True
                    self.player.isDead = True
                    # self.death_sound.play()      

        # check to see if player can jump - if falling
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits and self.deathAnimation == False:
                self.boosted = False
                # set var to be current hit in list to find which to 'pop' to when two or more collide with player
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                # fall if center is off platform
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                        self.boosted = False
                
        # if player reaches top 1/4 of screen...
        if self.player.rect.top <= HEIGHT / 4:
            # spawn a cloud
            if randrange(100) < 13:
                Cloud(self)
            # set player location based on velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / randrange(2,10)), 2)
            # creates slight scroll based on player y velocity
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for mobAttack in self.mobAttacks:
                mobAttack.rect.y += max(abs(self.player.vel.y), 2)
            for carrots in self.carrots:
                carrots.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
        # if player hits a power up
        if self.boosted == False:
            pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
            for pow in pow_hits:
                    if pow.type == 'boost':
                        self.boosted = True
                        self.boost_sound.play()
                        self.player.vel.y = -BOOST_POWER
                        self.player.jumping = False
                    if pow.type == 'shield':
                        if len(self.shield) < 1:
                            Shield(self, self.player)
                    if pow.type == 'carrotsUpgrade':
                        if self.playerShootCarrotAmount < 10:
                            self.playerShootCarrotAmount += 1  
                            self.playerShootCooldown += 75   
                        else:
                            self.playerShootCarrotAmount = 10
                            self.score += 15 
                
        #kills enemies if they touch carrots or shield
        if pg.sprite.groupcollide(self.mobs,self.carrots,True,True):
            self.score += 100
        if pg.sprite.groupcollide(self.mobAttacks,self.carrots,True,True):
            self.score += 10
        if pg.sprite.groupcollide(self.shield,self.mobAttacks, True, True):
            self.score += 10
        
        #only kills the player if they have less than 3 carrots
        if self.player.pos.y > HEIGHT + 300:
            if self.playerShootCarrotAmount >= 3:
                self.playerShootCarrotAmount -= 3
                self.playerShootCooldown -= 225
                self.deathAnimation = False
                self.player.isDead = False
                self.player.vel.y = 0
                self.boosted = True
                self.player.vel.y = -BOOST_POWER
            else:
                self.playing = False

        # generate new random platforms
        platformAmount = 20 - self.score/3000
        if platformAmount < 5:
            platformAmount = 5
        while len(self.platforms) < platformAmount:
            width = random.randrange(50, WIDTH-50)
            Platform(self, self.zone, random.randrange(0,WIDTH-width), 
                                random.randrange(-75, -30)) 
# checks if player presses certain keys
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w and self.boosted == False:
                        """ # cuts the jump short if the space bar is released """
                        self.player.jump_cut()
                if event.type == pg.KEYDOWN:
                    now = pg.time.get_ticks()     
                    if event.key == pg.K_SPACE and self.deathAnimation == False:
                        if now - self.timeSincePlayerShot > self.playerShootCooldown:
                            # self.shoot_sound.play()
                            self.timeSincePlayerShot = now
                            for i in range(self.playerShootCarrotAmount):
                                Carrot(self, self.player.rect.centerx, self.player.rect.centery, self.playerShootCarrotAmount, self.player.direction)
                        # self.head_jump_sound.play()
    def draw(self):
        # changes sky depending on zone
        if self.zone == "grass":
            self.screen.fill(SKY_BLUE)
        elif self.zone == "wood":
            self.screen.fill(SKY_BLUE)
        elif self.zone == "sand":
            self.screen.fill(SKY_BLUE)
        elif self.zone == "stone":
            self.screen.fill(GRAY)
        elif self.zone == "snow":
            self.screen.fill(GRAY)
        else:
            self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, BLACK, WIDTH / 2, 15)
        self.draw_text("Carrots: " + str(self.playerShootCarrotAmount), 22, BLACK, WIDTH / 2, 40)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    def show_start_screen(self):
        """ # game splash screen """
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to shoot", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        """ # game splash screen """
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to shoot", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)


        pg.display.flip()
        self.wait_for_key()
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")