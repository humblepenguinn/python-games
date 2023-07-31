import pygame 
import neat
import time
import os
import os.path
import random
import sys
import pickle

# --> Some crap we need
pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
BERD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","berd1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","berd2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","berd2.png")))
            ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.Font("04B_19__.TTF",50)
MENU_FONT  = pygame.font.Font("04B_19__.TTF",30)
win = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
player_option = None

# --> Button class
class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = MENU_FONT.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

# --> Berd class
class Berd:
    IMGS = BERD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    # --> Berd physics
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count+1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0 :
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    # --> Berd animation
    def draw(self , win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]

        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]

        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img , self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x , self.y)).center)
        win.blit(rotated_image , new_rect.topleft)
    
    # --> Berd mask
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# --> Pipe class
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG , False , True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    # --> Pipe spawn
    def set_height(self):
        self.height = random.randrange(50 , 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    # --> Pipe move
    def move(self):
        self.x -= self.VEL
    
    # --> Pipe blit on screen
    def draw(self , win):
        win.blit(self.PIPE_TOP, (self.x , self.top))
        win.blit(self.PIPE_BOTTOM, (self.x , self.bottom))

    # --> Collision system
    def collide(self , berd):
        berd_mask = berd.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - berd.x, self.top - round(berd.y))
        bottom_offset = (self.x - berd.x , self.bottom - round(berd.y))

        b_point = berd_mask.overlap(bottom_mask , bottom_offset) # --> return None if it dosent collide
        t_point = berd_mask.overlap(top_mask , top_offset)
        
        if t_point or b_point:
            return True

        return False

# --> Base class
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y =  y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    # --> Base movement
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0 :
            self.x2 = self.x1 + self.WIDTH
    
    # --> Base blit
    def draw(self , win):
        win.blit(self.IMG , (self.x1 , self.y))
        win.blit(self.IMG , (self.x2 , self.y))

# --> Blit everything on screen
def draw_window_model(win , berds , pipes , base , score , gen, mode, font):
    _continue = True
    win.blit(BG_IMG , (0,0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render(str(score) , 1 , (255 , 255 , 255)) 
    win.blit(text,(WIN_WIDTH - 230 - text.get_width() , 10 ))
    
    if mode == "Training":
        text = STAT_FONT.render("Gen: "+ str(gen) , 1 , (255 , 255 , 255)) 
        win.blit(text,(10 , 10 ))

    if mode == "AI":
        if score < 3:
            win.blit(font, (WIN_WIDTH//2 - 150, WIN_HEIGHT//2 - 250))
        elif 3 < score < 8:
            font = MENU_FONT.render("HAHAH YOU SUCK MY AI IS BETTER THAN U!", 1 , (255 , 255 , 255))
            win.blit(font, (WIN_WIDTH//2 - 350, WIN_HEIGHT//2 - 250))

        elif 15 < score < 20:
            font = MENU_FONT.render("FEEL LIKE A LOSER??", 1 , (255 , 255 , 255))
            win.blit(font, (WIN_WIDTH//2 - 150, WIN_HEIGHT//2 - 250))
        
        

        

    base.draw(win)

    for berd in berds:
        berd.draw(win)

    pygame.display.update()


def draw_window(win , berd , pipes , base , score , dead):
    win.blit(BG_IMG , (0,0))
    
    if dead == False:
        text = STAT_FONT.render(str(score) , 1 , (255 , 255 , 255)) 
        win.blit(text,(WIN_WIDTH - 230 - text.get_width() , 10 ))
    else:
        text = STAT_FONT.render("Game Over" , 1 , (255 , 255 , 255)) 
        win.blit(text,(WIN_WIDTH - 120 - text.get_width() , 10 ))

    for pipe in pipes:
        pipe.draw(win)
        
    base.draw(win)
    berd.draw(win)

    pygame.display.update()

# --> The AI function
def fitness(genomes , config):
    mode = None
    global  GEN
    GEN += 1
    nets = []
    ge = []
    berds = []
    font = None
    


    for _ ,g in genomes: # --> Beacuse its a tuple
        net = neat.nn.FeedForwardNetwork.create(g , config)
        nets.append(net)
        berds.append(Berd(230 , 350))
        g.fitness = 0
        ge.append(g)
    
    if len(berds) > 1:
        mode = "Training"
    
    else:
        mode = "AI"
    
    

    base = Base(730)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and mode == "Training":
                if event.key == pygame.K_s:
                    run = False

        pipe_ind = 0
        if len(berds) > 0:
            if len(pipes) > 1 and berds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, berd in enumerate(berds):
            berd.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((berd.y , abs(berd.y - pipes[pipe_ind].height) , abs(berd.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                berd.jump()
                
        rem = []
        add_pipe = False
        for pipe in pipes:
            for x ,berd in enumerate(berds):
                if pipe.collide(berd):
                    ge[x].fitness -= 1
                    berds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < berd.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5

            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
        
        for x,berd in enumerate(berds):
            if berd.y + berd.img.get_height() >= 730 or berd.y < 0:
                berds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if mode == "AI":
            font = MENU_FONT.render("Give it up for Bobby", 1 , (255 , 255 , 255))
            
        
        base.move()
        draw_window_model(win , berds , pipes , base , score , GEN, mode, font)

# --> Main game function
def main():
    dead = False
    berd = Berd(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        berd.move()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if dead == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        berd.jump()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    berd.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(berd):
                    dead = True

            if not pipe.passed and pipe.x < berd.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
            
        if berd.y + berd.img.get_height() >= 730 or berd.y < 0:
            dead = True
        
        if dead:
            text =  STAT_FONT.render("Game Over", 1, (255, 0, 0))
            win.blit(text , (145, 350))
            pygame.display.update()
            time.sleep(1)
            run = False
            
        base.move()
        draw_window(win , berd , pipes , base , score , dead)

  

# --> To load the model
def replay_genome(config_path, genome_path="model.pkl"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    genomes = [(1, genome)]

    fitness(genomes, config)

    

# --> Config neat
def run(config_path):
    # --> Load config file
    config =  neat.config.Config(neat.DefaultGenome , neat.DefaultReproduction,
                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                      config_path)

    # --> To see output on screen
    popultaion = neat.Population(config)
    popultaion.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    popultaion.add_reporter(stats)

    winner = popultaion.run(fitness,5)

    with open("model.pkl" , "wb") as f:
        pickle.dump(winner , f)

clock = pygame.time.Clock()
berd = Berd(230,350)
base = Base(730)
while True:
    clock.tick(60)
    win.blit(BG_IMG , (0,0))
    
    title =  STAT_FONT.render("Flappy Bird", 1, (255, 255, 255))
    win.blit(title , (WIN_WIDTH // + 4, WIN_HEIGHT // 2 - 250))
    
    play_btn = Button((255, 0, 0), 145, 450, 230, 60, "Play")
    train_btn = Button((255, 0, 0), 145, 550, 230, 60, "Train")
    ai_btn = Button((255, 0, 0), 145, 650, 230, 60, "AI")
    x, y = pygame.mouse.get_pos()

    play = play_btn.isOver((x, y))
    train = train_btn.isOver((x, y))
    ai = ai_btn.isOver((x, y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and play:
            player_option = "player"
            main()
                
        if event.type == pygame.MOUSEBUTTONDOWN and train:
            player_option = "train"
            local_dir = os.path.dirname(__file__)
            config_path = os.path.join(local_dir ,"config-feedforward.txt")
            run(config_path)

        if event.type == pygame.MOUSEBUTTONDOWN and ai:
            player_option = "AI"
            if os.path.exists('model.pkl'):
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir ,"config-feedforward.txt")
                replay_genome(config_path)
            else:
                print("No Model To Use! Please Train A Model By Using The Train Argument!")
                    
    base.move()    
    play_btn.draw(win, outline = (255,255,255))
    train_btn.draw(win, outline = (255,255,255))
    ai_btn.draw(win, outline = (255,255,255))
    berd.draw(win)
    base.draw(win)

    pygame.display.update()










