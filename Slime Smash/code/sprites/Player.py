from sprites.Sprite import *

class Player(Sprite):
    def __init__(self, group, camera):
        super().__init__(group, camera)

        self.images = {
            "normal0_right" : pygame.image.load("assets/character/player/ninja0_right.png").convert_alpha(),
            "normal1_right" : pygame.image.load("assets/character/player/ninja1_right.png").convert_alpha(),
            "normal0_left" : pygame.image.load("assets/character/player/ninja0_left.png").convert_alpha(),
            "normal1_left" : pygame.image.load("assets/character/player/ninja1_left.png").convert_alpha(),
            "death0_right" : pygame.image.load("assets/character/player/ninja_death0_right.png").convert_alpha(),
            "death1_right" : pygame.image.load("assets/character/player/ninja_death1_right.png").convert_alpha(),
            "death2_right" : pygame.image.load("assets/character/player/ninja_death2_right.png").convert_alpha(),
            "death3_right" : pygame.image.load("assets/character/player/ninja_death3_right.png").convert_alpha(),
            "death0_left" : pygame.image.load("assets/character/player/ninja_death0_left.png").convert_alpha(),
            "death1_left" : pygame.image.load("assets/character/player/ninja_death1_left.png").convert_alpha(),
            "death2_left" : pygame.image.load("assets/character/player/ninja_death2_left.png").convert_alpha(),
            "death3_left" : pygame.image.load("assets/character/player/ninja_death3_left.png").convert_alpha(),
        }

        self.statu = "normal"
        self.animationFrame = 0
        self.direction = "right"
        self.animationTick = 2

        self.player = Image2(self.getImage())
        self.player.scaleImage(SCALAR)

        self.image = self.player.image
        self.rect = self.player.rect

        self.hitbox = self.rect.copy().inflate(0, 0)
        self.position = pygame.math.Vector2(SCREEN_WIDTH / 2, GROUND_Y - self.hitbox.height / 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.axis = pygame.math.Vector2(0, 0)
        self.falling = 0
        self.jumping = 1

        self.jumpPower = 700
        self.jumpHeight = 13
        self.friction = 0.8
        self.moveSpeed = 80

        self.playerJumpSound = pygame.mixer.Sound("audio/effect/playerJump.wav")

        self.setPositionWithCamera()
    
    def collisionX(self):
        if self.position.x + self.hitbox.width / 2 > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.hitbox.width / 2
            self.velocity.x = 0
        if self.position.x - self.hitbox.width / 2 < 0:
            self.position.x = self.hitbox.width / 2
            self.velocity.x = 0
    
    def control(self):
        keys = pygame.key.get_pressed()
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.axis.x = right - left
        self.axis.y = up - down
    
    def move(self):
        self.control()
        self.velocity.x = self.velocity.x * self.friction + self.axis.x * self.moveSpeed
        if self.axis.y == 1:
            if self.falling < 2 or self.jumping > 0:
                if self.falling == 0:
                    self.playerJumpSound.play()
                self.jumping += 1
                if self.jumping < self.jumpHeight:
                    self.velocity.y = -self.jumpPower
        else:
            self.jumping = 0
    
    def getImage(self):
        return self.images[f"{self.statu}{int(self.animationFrame) % self.animationTick}_{self.direction}"]
    
    def animate(self, dt):
        if not self.isAlive:
            self.animationTick = 4
            self.statu = "death"
            self.animationFrame += dt * 8
        else:
            self.animationTick = 2
            if self.axis.x != 0:
                if self.axis.x > 0:
                    self.direction = "right"
                else:
                    self.direction = "left"
                if self.falling < 2:
                    self.animationFrame += dt * 8
            else:
                if self.falling < 2:
                    self.animationFrame += dt * 4
                else:
                    self.animationFrame = 0

        self.player.setImage(self.getImage())
        self.image = self.player.image

    def update(self, dt):
        self.integrate(dt)
        if self.isAlive:
            self.collisionX()
            self.collisionY()
            self.move()
        self.setPositionWithCamera()
        self.animate(dt)