from sprites.Sprite import *
import random

class Slime(Sprite):
    def __init__(self, group, camera):
        super().__init__(group, camera)
    
        self.images = {
                "0_normal_right" : pygame.image.load("assets/character/enemy/slime1_normal_right.png").convert_alpha(),
                "0_normal_left" : pygame.image.load("assets/character/enemy/slime1_normal_left.png").convert_alpha(),
                "1_normal_right" : pygame.image.load("assets/character/enemy/slime2_normal_right.png").convert_alpha(),
                "1_normal_left" : pygame.image.load("assets/character/enemy/slime2_normal_left.png").convert_alpha(),
                "0_squish_right" : pygame.image.load("assets/character/enemy/slime1_squish_right.png").convert_alpha(),
                "0_squish_left" : pygame.image.load("assets/character/enemy/slime1_squish_left.png").convert_alpha(),
                "1_squish_right" : pygame.image.load("assets/character/enemy/slime2_squish_right.png").convert_alpha(),
                "1_squish_left" : pygame.image.load("assets/character/enemy/slime2_squish_left.png").convert_alpha(),
            }
        
        self.axis = pygame.math.Vector2(random.choice([-1, 1]), 0)
        self.type = random.randint(0, 1)
        self.statu = "normal"
        if self.axis.x == 1:
            self.direction = "right"
        else:
            self.direction = "left"
        self.squishedFrame = 0

        self.slime = Image2(self.getImage())
        self.slime.scaleImage(SCALAR)
        self.image  = self.slime.image
        self.rect = self.slime.rect
        self.hitbox = self.rect.copy().inflate(0, 0)

        if self.axis.x == 1:
            self.position = pygame.math.Vector2(-self.hitbox.width, GROUND_Y - self.hitbox.height / 2)
            self.velocity = pygame.math.Vector2(random.randint(200, 300), 0)
        else:
            self.position = pygame.math.Vector2(SCREEN_WIDTH + self.hitbox.width, GROUND_Y - self.hitbox.height / 2)
            self.velocity = pygame.math.Vector2(random.randint(-300, -200), 0)
        
        self.setPositionWithCamera()
        
        self.falling = 0
        self.jumpPower = random.randint(500, 1000)
    
    def getImage(self):
        return self.images[f"{self.type}_{self.statu}_{self.direction}"]

    def move(self):
        if not self.isAlive:
            if self.squishedFrame > 20:
                self.kill()
            self.squishedFrame += 1
            return
        
        if self.falling < 2:
            self.velocity.y = -self.jumpPower
    
    def animate(self):
        if not self.isAlive:
            self.statu = "squish"

        self.slime.setImage(self.getImage())
        self.image = self.slime.image

    def update(self, dt):
        if self.isAlive:
            self.integrate(dt)
        self.collisionY()
        self.move()
        self.animate()
        self.setPositionWithCamera()