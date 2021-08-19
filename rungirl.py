import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Running Girl") # set window title

BG_img = pygame.image.load(os.path.join("Asetgirl/Other", "desert.png"))
BG = pygame.transform.scale(BG_img, (1000, 500))

RUNNING = [pygame.image.load(os.path.join("Asetgirl/girl", "GirlRun1.png")),
           pygame.image.load(os.path.join("Asetgirl/girl", "GirlRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Asetgirl/girl", "GirlJump.png"))
DUCKING = [pygame.image.load(os.path.join("Asetgirl/girl", "GirlDuck1.png")),
           pygame.image.load(os.path.join("Asetgirl/girl", "GirlDuck2.png"))]

CORONA = [pygame.image.load(os.path.join("Asetgirl/corona", "virus(1).png")),
                pygame.image.load(os.path.join("Asetgirl/corona", "virus(2).png")),
                pygame.image.load(os.path.join("Asetgirl/corona", "virus(3).png"))]

BIRD = [pygame.image.load(os.path.join("Asetgirl/corona", "virus(4).png")),
        pygame.image.load(os.path.join("Asetgirl/corona", "virus(5).png"))]

music = pygame.mixer.music.load(os.path.join("Asetgirl/music", "moonlight.wav"))
pop_sound = pygame.mixer.Sound(os.path.join("Asetgirl/music", "explode.wav")) 
pygame.mixer.music.play(-1) 

class Girl:
    X_POS = 80
    Y_POS = 360
    Y_POS_DUCK = 370
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.girl_duck = False
        self.girl_run = True
        self.girl_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.girl_rect = self.image.get_rect()
        self.girl_rect.x = self.X_POS
        self.girl_rect.y = self.Y_POS

    def update(self, userInput):
        if self.girl_duck:
            self.duck()
        if self.girl_run:
            self.run()
        if self.girl_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.girl_jump:
            self.girl_duck = False
            self.girl_run = False
            self.girl_jump = True
        elif userInput[pygame.K_DOWN] and not self.girl_jump:
            self.girl_duck = True
            self.girl_run = False
            self.girl_jump = False
        elif not (self.girl_jump or userInput[pygame.K_DOWN]):
            self.girl_duck = False
            self.girl_run = True
            self.girl_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.girl_rect = self.image.get_rect()
        self.girl_rect.x = self.X_POS
        self.girl_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.girl_rect = self.image.get_rect()
        self.girl_rect.x = self.X_POS
        self.girl_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.girl_jump:
            self.girl_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.girl_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.girl_rect.x, self.girl_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Corona(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 375



class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 285
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Girl()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (800, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        
        
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Corona(CORONA))
            elif random.randint(0, 2) == 1:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.girl_rect.colliderect(obstacle.rect):
                pop_sound.play()
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        

        
        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
    exit()


menu(death_count=0)
