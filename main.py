import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600                                     #Sets the width and height of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)                                     #Sets the colour of the screen    
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

heart_image = pygame.image.load("heart.png")        #Loads the image of the heart
heart_image = pygame.transform.scale(heart_image, (30, 30))

class Snake:         #Creates the snake
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10 
        self.velocity = 20
        self.direction = "RIGHT"
        self.lives = 3
        self.length = 0
        self.explored = []
        self.invincible = False
        self.flash = 0

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.direction != "RIGHT":
            self.direction = "LEFT"
        if keys[pygame.K_RIGHT] and self.direction != "LEFT":
            self.direction = "RIGHT"
        if keys[pygame.K_UP] and self.direction != "DOWN":
            self.direction = "UP"
        if keys[pygame.K_DOWN] and self.direction != "UP":
            self.direction = "DOWN"


        if self.direction == "LEFT":
            self.x -= self.velocity
        if self.direction == "RIGHT":
            self.x += self.velocity
        if self.direction == "UP":
            self.y -= self.velocity
        if self.direction == "DOWN":
            self.y += self.velocity


        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))

        if self.x == 0:
            self.x = WIDTH
        elif self.x == WIDTH - self.size:
            self.x = 0
        elif self.y == 0:
            self.y = HEIGHT
        elif self.y == HEIGHT - self.size:
            self.y = 0

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size)) 
        count = 0
        self.flash = not self.flash    #Makes the snake flash when invincible
        for x,y in self.explored:    #Draws the snake's body
            if self.length == count:
                break

            if self.invincible:
                if self.flash:
                    colour = RED
                else:
                    colour = GREEN
            else:
                colour = YELLOW
            pygame.draw.rect(screen, colour, (x, y, self.size, self.size))
            count += 1

    def check(self):
        if not self.invincible:
            if (self.x, self.y) in self.explored:
                return True
            
class hunters:          #Creates the hunters
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 10
        self.moveStatus = False
        self.speed = 20

    def move(self):
        if self.moveStatus:
            self.x += random.uniform(-self.speed, self.speed)  
            self.y += random.uniform(-self.speed, self.speed)  
            self.x = max(0, min(self.x, WIDTH - self.size))
            self.y = max(0, min(self.y, HEIGHT - self.size))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

    def check(self, x, y, snake):           #Checks if the snake has collided with the hunter
        if not snake.invincible:
            for x, y in snake.explored:
                if abs(self.x - x) <= self.size and abs(self.y - y) <= self.size:
                    snake.lives -= 1
                    self.moveStatus = False    #Hunter's legs are paralysed from snake venom
                    snake.invincible = True

                    return True
        return False 

class food:         #Creates the food
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 10
        self.drawStatus = True
    def draw(self):
        if self.drawStatus:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)        
    def check(self, x, y):
        if abs(self.x - x) <= self.size and abs(self.y - y) <= self.size:
            self.drawStatus = False
            return True
        return False
    

class Game:
    def display_message(self, *message):            #Displays the message on the screen
        i = 0
        j = 0
        for msg in message:
            font = pygame.font.Font(None, 74)
            text = font.render(msg, True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + j))
            screen.blit(text, text_rect)
            j += 50
        pygame.display.update()

    def score(self, length, snake, flag2, speed):           #Displays the score and the velocity of the snake
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(length * 20) +"   Velocity:" + str(speed), True, WHITE)
        screen.blit(text, (10, 10))
        if length % 5 == 0 and flag2 and snake.velocity < 35:
            snake.velocity += 1

    def draw_hearts(self, lives):
        for i in range(lives):  
            screen.blit(heart_image, (WIDTH - (i + 1) * 40, 10))

    def run(self):        #Runs the game
        flag = 0
        innviceTime = 0
        snake = Snake(400, 300) 
        clock = pygame.time.Clock()  
        objects = []
        ogHunter = hunters()
        ogHunter.moveStatus = True
        hunterz = [ogHunter]

        for i in range(10):
            object = food()
            objects.append(object)
        running = True

        while running:          #Main loop
            screen.fill(BLACK) 
            flag2 = 0

            for object in objects:
                object.draw() 
                if object.check(snake.x, snake.y):
                    snake.length += 1
                    flag2 = 1
                    flag = 1
                    object.x = random.randint(0, WIDTH)
                    object.y = random.randint(0, HEIGHT)
                    object.drawStatus = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if snake.length > 0:
                snake.explored.append((snake.x, snake.y))
            if len(snake.explored) > snake.length:
                snake.explored.pop(0)

            snake.move() 
            snake.draw()  
            self.draw_hearts(snake.lives)
            self.score(snake.length, snake, flag2, snake.velocity)

            if snake.length > 4:                            #Adds hunters based on snake length
                if snake.length % 6 == 0 and flag == 1:
                    hunter = hunters()
                    hunter.moveStatus = True
                    hunterz.append(hunter)
                    flag = 0
                for hunter in hunterz:
                    hunter.draw()
                    hunter.move()
                    hunter.check(snake.x, snake.y, snake)
                             
            if snake.lives < 0 or snake.check():        #Ends the game if the snake has no lives or has collided with itself
                waiting_for_restart = True
                while waiting_for_restart:
                    self.display_message("Game Over", "Press R to restart")
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_restart = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:  
                                snake = Snake(20, 20)
                                hunterz = [ogHunter]
                                waiting_for_restart = False
                            else:
                                break
            if snake.invincible:      #Controls how long the snake is invincible for
                innviceTime += 1
                if innviceTime == 50:
                    snake.invincible = False
                    innviceTime = 0

            pygame.display.update()  
            clock.tick(10)  

        pygame.quit()


game = Game()
game.run()