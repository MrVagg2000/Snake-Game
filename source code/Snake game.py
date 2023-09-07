import pygame
from pygame.locals import *
import time
import random
from tkinter import *
from ttkthemes import ThemedTk
SIZE = 40

def menu():
    global window
    window = ThemedTk(theme= "blue")
    window.configure(themebg= "blue")

    window.title("Snake Game")
    window.geometry("500x700")

    label1= Label(window,text = "Welcome to the snake game",font=("arial", 30),bg="#4AC9FF")
    label1.pack()

    buton = Button(window,text= "play", font= ("arial",50),bg="#4AC9FF",command=game.run)
    buton.pack()
    img = PhotoImage(file="snake2.png")
    label2=Label(window,bg="#6699cc",width=1000,height=1000)
    label2.config(image=img)
    label2.pack()

    window.mainloop()

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.x = 100
        self.y = 100
        self.direction = "down"

        self.length= length
        self.x = [40]*length
        self.y = [40]*length

    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)



    def move_left(self):
        self.direction = "left"


    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"






    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0]   -=  SIZE
        if self.direction == "right":
            self.x[0]   +=  SIZE
        if self.direction == "up":
            self.y[0]   -=  SIZE
        if self.direction == "down":
            self.y[0]   +=  SIZE
        self.draw()

    def draw(self):
        self.parent_screen.fill((0, 153, 0))

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = 200
        self.y = 200

    def draw(self):

        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 25)* SIZE
        self.y = random.randint(1, 20)*SIZE


class Game:
    def __init__(self):
        pygame.init()


    def is_collision(self,x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 +SIZE:
                return True

        return False

    def eat_apple(self):
        eat=pygame.mixer.Sound("apple_sound.mp3")
        #pygame.mixer.music.set_volume(0.05)
        pygame.mixer.Sound.play(eat)
        #pygame.mixer.music.stop()

    def bg_music(self):
        pygame.mixer.music.load("BG_MUSICK.mp3")
        #pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1,0)

    def hit_boundaries(self):
        hit=pygame.mixer.Sound("metal_pipe.mp3")
        #pygame.mixer.music.set_volume(0.1)
        pygame.mixer.Sound.play(hit)



    def score(self):
        font = pygame.font.SysFont("arial", 30)
        line3 = font.render(f"SCORE: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line3, (800, 10))

    def show_game_over(self):
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over!Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press enter.To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def boundaries(self):
        if self.snake.x[0]<0 or self.snake.x[0] >1000 or self.snake.y[0]<0 or self.snake.y[0]>1000 :
            self.hit_boundaries()
            raise "Boundaries Hit"




    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.boundaries()
        self.score()

        pygame.display.flip()
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y ) ==True :
                self.snake.increase_length()
                self.eat_apple()
                self.apple.move()
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]) == True :
                raise "Colission Ocured"


    def run(self):
        window.destroy()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1)
        # pygame.mixer.Sound.set_volume(0.1)
        self.bg_music()

        self.surface = pygame.display.set_mode((1000, 1000))
        self.snake = Snake(self.surface, 1)  # poso megalo thelw na einai
        self.snake.draw()
        self.apple = Apple(self.surface)  # to appla me a mikro legetai adikimeno,object to appla me A legetai class h ergosatsio.
        self.apple.draw()

        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_a:
                        self.snake.move_left()

                    if event.key == K_d:
                        self.snake.move_right()

                    if event.key == K_w:
                        self.snake.move_up()

                    if event.key == K_s:
                        self.snake.move_down()

                    if event.key == K_RETURN:
                        pause = False
                        self.bg_music()


                elif event.type == QUIT:
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e :
                pause = True
                self.show_game_over()
                self.reset()



            time.sleep(.1)


if __name__ == "__main__":
    game = Game()
    menu()
