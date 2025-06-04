import pygame 
pygame.init()
import math 
import random 




#Functions 
def load_image(img, scale): 
    img = pygame.image.load(img)
    width = img.get_width() 
    height = img.get_height() 
    ratio = width / height 
    img = pygame.transform.scale(img, (width * scale, (width * scale/ratio)))
    return img 

def scale_image(img, scale): 
    width = img.get_width() 
    height = img.get_height() 
    ratio = width / height 
    img = pygame.transform.scale(img, (width * scale, (width * scale/ratio)))
    return img    


def draw(): 
    screen.fill(BLACK)
    gameboard.draw()

    pygame.draw.rect(screen, SILVER, (0, SCREEN_HEIGHT-100, SCREEN_WIDTH, 100))  
    if gameboard.turn == "enemy": 
        pos_x = 0
        for enemy in all_enemies: 
            screen.blit(enemy.animation["static"][0], (pos_x , SCREEN_HEIGHT - 130) )
            pos_x += 200
        message_text = BIG_FONT.render("Enemies are moving...", 1, WHITE)
        screen.blit(message_text, (200 , SCREEN_HEIGHT - 75))


    elif gameboard.turn =="player": 
        if gameboard.selected_l == None: 
            selected_unit_text = BIG_FONT.render(f"Please select your unit. [Left click] move / [Right click] attack", 1, WHITE)
        if gameboard.selected_l != None: 
            screen.blit(scale_image(gameboard.selected_l.animation["static"][0], 1), (10, SCREEN_HEIGHT-130))
            selected_unit_text = BIG_FONT.render(f"Unit: {gameboard.selected_l.name}    [Left click] select a place to move.", 1, WHITE)
        if gameboard.selected_r != None: 
            screen.blit(scale_image(gameboard.selected_r.animation["static"][0], 1), (10, SCREEN_HEIGHT-130))
            selected_unit_text = BIG_FONT.render(f"Unit: {gameboard.selected_r.name}    [Right click] select a place to attack.", 1, WHITE)
        screen.blit(selected_unit_text, (20 , SCREEN_HEIGHT - 75))

    pygame.display.update()

def get_grid_pos(pos): 
    x, y = pos 
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col


# setup screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Toys War") 
screen_2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
screen_shake = 0 



#Set game variables 
ROWS = 10
COLS= 10
SQUARE_SIZE = SCREEN_WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (165, 169, 180)
RED_ALPHA = (255, 0, 0, 100)
BLUE_ALPHA = (0, 0, 255, 100)
GREEN_ALPHA = (0, 255, 0, 100)
TRANSPARENT = (0, 0, 0, 0)
LIGHTGREEN = (144, 238, 144)
LIGHTRED = (255, 127, 127)
BIG_FONT = pygame.font.SysFont("comicsans", 25)
SMALL_FONT = pygame.font.SysFont("comicsans", 15)

#set frame rate 
clock = pygame.time.Clock() 
FPS = 60 

#load game images 
background_img = pygame.image.load("img/background.jpg")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT-100))
pointer_img = pygame.image.load("img/pointer.png")

#Load Gundam
gundam_animation = {} 
gundam_animation["static"] = [] 
gundam_animation["idle"] = [] 
gundam_animation["move"] = []
gundam_animation["attack"] = [] 
gd_img = pygame.image.load("img/gundam/static.png")
gundam_animation["static"].append(scale_image(gd_img, 0.4))
for i in range (20): 
    gd_img = pygame.image.load(f"img/gundam/idle/{i}.png")
    gundam_animation["idle"].append(scale_image(gd_img, 0.3)) 
for i in range (21): 
    gd_img = pygame.image.load(f"img/gundam/attack/{i}.png")
    gundam_animation["attack"].append(scale_image(gd_img, 0.35)) 
for i in range (21): 
    gd_img = pygame.image.load(f"img/gundam/move/{i}.png")
    gundam_animation["move"].append(scale_image(gd_img, 0.3)) 

#Load Deep Striker
deep_animation = {} 
deep_animation["static"] = [] 
deep_animation["idle"] = [] 
deep_animation["move"] = []
deep_animation["attack"] = [] 
deep_img = pygame.image.load("img/deep/static.png")
deep_animation["static"].append(scale_image(deep_img, 0.4))
for i in range (2): 
    deep_img = pygame.image.load(f"img/deep/idle/{i}.png")
    deep_animation["idle"].append(scale_image(deep_img, 0.8)) 
for i in range (18): 
    deep_img = pygame.image.load(f"img/deep/attack/{i}.png")
    deep_animation["attack"].append(scale_image(deep_img, 0.7)) 
for i in range (20): 
    deep_img = pygame.image.load(f"img/deep/move/{i}.png")
    deep_animation["move"].append(scale_image(deep_img, 0.8)) 


#Load Wing Gundam
wing_animation = {} 
wing_animation["static"] = [] 
wing_animation["idle"] = [] 
wing_animation["move"] = []
wing_animation["attack"] = [] 
wing_img = pygame.image.load("img/wing/static.png")
wing_animation["static"].append(scale_image(wing_img, 1))
for i in range (2): 
    wing_img = pygame.image.load(f"img/wing/idle/{i}.png")
    wing_animation["idle"].append(scale_image(wing_img, 0.3)) 
for i in range (20): 
    wing_img = pygame.image.load(f"img/wing/attack/{i}.png")
    wing_animation["attack"].append(scale_image(wing_img, 0.35)) 
for i in range (20): 
    wing_img = pygame.image.load(f"img/wing/move/{i}.png")
    wing_animation["move"].append(scale_image(wing_img, 0.4)) 

#bullet_img = load_image("img/bullet.png", 1) 
bullet_animation = [] 
for i in  range (13): 
    bullet_img = pygame.image.load(f"img/bullet/{i}.png")
    bullet_animation.append(scale_image(bullet_img, 0.2)) 
explosion_animation = [] 
for i in  range (15): 
    explosion_img = pygame.image.load(f"img/explosion/{i}.png")
    explosion_animation.append(scale_image(explosion_img, 0.3)) 


#Classes 
class Board:
    def __init__(self):
        self.board = [] 
        self.create_board()
        self.selected_l = None
        self.selected_r = None 
        self.avail_move = []
        self.avail_shoot = []
        self.enemy_avail_moves = [] 
        self.enemy_avail_shoots = [] 
        self.ai_moving = False 
        self.turn = "player"
        self.change_turn_counter = 0 

     
    def draw(self): 
        screen.blit(background_img, (0, 0))
        screen_2.fill(TRANSPARENT)
        for row in range(ROWS): 
            for col in range(COLS): 
                pygame.draw.rect(screen, WHITE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                unit = gameboard.board[row][col] 
                if unit != 0:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE 
                    pygame.draw.rect(screen_2, GREEN_ALPHA, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        
        if len(self.avail_move) != 0: 
            for pos in self.avail_move:
                row, col = pos 
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                pygame.draw.rect(screen_2, RED_ALPHA, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            mpos = pygame.mouse.get_pos()
            m_x, m_y = mpos  
            unit_mask = pygame.mask.from_surface(self.selected_l.image)
            unit_shadow = unit_mask.to_surface(setcolor = (0, 0, 0, 180), unsetcolor = (0, 0, 0, 0))
            screen_2.blit(unit_shadow, (m_x - self.selected_l.image.get_width() //2, m_y - self.selected_l.image.get_height()//2) )
        if len(self.avail_shoot) != 0: 
            for pos in self.avail_shoot:
                row, col = pos 
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                pygame.draw.rect(screen_2, BLUE_ALPHA, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            mpos = pygame.mouse.get_pos()
            m_x, m_y = mpos 
            screen_2.blit(pointer_img, (m_x - pointer_img.get_width() //2, m_y - pointer_img.get_height()//2) ) 
        if len(self.enemy_avail_moves) != 0: 
            for pos in self.enemy_avail_moves:
                row, col = pos 
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                pygame.draw.rect(screen_2, RED_ALPHA, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        if len(self.enemy_avail_shoots) != 0: 
            for pos in self.enemy_avail_shoots:
                row, col = pos 
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                pygame.draw.rect(screen_2, BLUE_ALPHA, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        all_flyings.draw(screen_2)

        #all_units.draw(screen_2)
        for row in range (ROWS):
            for col in range (COLS): 
                unit = gameboard.board[row][col] 
                if unit != 0:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE 
                    unit.draw_unit() 
        

        all_bullets.draw(screen_2)
        all_explosions.draw(screen_2)
        screen_shake_offset = (random.random() * screen_shake - screen_shake/2, random.random() * screen_shake - screen_shake/2)
        screen.blit(screen_2, (screen_shake_offset))


    def create_board(self): 
        for row in range(ROWS): 
            self.board.append([])
            for col in range (COLS):
                self.board[row].append(0) 
    
    def select_unit(self, row, col): 
        if self.selected_l:   #check if this is the second click
            self.place_unit(self.selected_l, row, col)
        else:   # else if this is the first click 
            unit = self.board[row][col]
            if unit != 0 and unit.type == "player": 
                self.selected_l = unit
                self.selected_r = None
                self.avail_shoot = []   
                self.avail_move = self.selected_l.calc_avail_move()
                self.board[row][col].frame = 0
                self.board[row][col].action = "move"
                #print(self.avail_move)
                
    def place_unit(self, unit, row, col): 
        if row < ROWS: 
            if (row, col) in self.selected_l.avail_move and self.board[row][col] == 0: 
                flying = Flying(unit, unit.row, unit.col, row, col)
                all_flyings.add(flying)
                self.board[unit.row][unit.col], self.board[row][col] = self.board[row][col], self.board[unit.row][unit.col] # this is copy only, not change the row, col , x , y data yet
                self.board[row][col].move(row, col)
                self.board[row][col].avail_move = [] 
                self.board[row][col].frame = 0
                self.board[row][col].action = "idle"
                self.avail_move = [] 
                self.before_shoot(self.selected_l.row, self.selected_l.col) 
                #print("placed")
                
                              
            else: 
                self.board[self.selected_l.row][self.selected_l.col].frame = 0
                self.board[self.selected_l.row][self.selected_l.col].action = "idle"
                self.selected_l = None 
                self.avail_move = [] 
                #print("can't move")  
        else: 
            self.board[self.selected_l.row][self.selected_l.col].frame = 0
            self.board[self.selected_l.row][self.selected_l.col].action = "idle"
            self.selected_l = None 
            self.avail_move = [] 
            #print("can't move")  


    def before_shoot(self, row, col): 
        if self.selected_r:  #check if this is the second click
            self.shoot(self.selected_r, row, col)
        else:   # else if this is the first click 
            unit = self.board[row][col]
            if unit != 0 and unit.type == "player": 
                self.selected_r = unit 
                self.selected_l = None
                self.avail_move = []  
                self.avail_shoot = self.selected_r.calc_avail_shoot()
                self.board[row][col].frame = 0
                self.board[row][col].action = "attack"
                print(self.selected_r)

    def shoot(self, unit, row, col): 
        if row < ROWS:         
            if (row, col) in self.selected_r.avail_shoot: 
                bullet = Bullet(unit.row, unit.col, row, col)
                all_bullets.add(bullet)
                self.board[self.selected_r.row][self.selected_r.col].frame = 0
                self.board[self.selected_r.row][self.selected_r.col].action = "idle"
                self.avail_shoot = [] 
                self.selected_r = None 
                print("shoot")
                self.turn = "enemy"
            else: 
                #self.board[self.selected_r.row][self.selected_r.col].frame = 0
                #self.board[self.selected_r.row][self.selected_r.col].action = "idle"            
                #self.selected_r = None 
                #self.avail_shoot = [] 
                print("can't shoot")
                
        else: 
            #self.board[self.selected_r.row][self.selected_r.col].frame = 0
            #self.board[self.selected_r.row][self.selected_r.col].action = "idle"          
            #self.selected_r = None 
            #self.avail_shoot = [] 
            print("can't shoot")
    
    
    def ai_before_move(self): 
        for enemy in all_enemies: 
            enemy_avail_move = enemy.calc_avail_move()
            self.enemy_avail_moves.extend(enemy_avail_move)
            self.board[enemy.row][enemy.col].frame = 0 
            self.board[enemy.row][enemy.col].action = "move" 
    
    def ai_move(self): 
        for enemy in all_enemies: 
            enemy_avail_move = enemy.calc_avail_move()
            print(enemy_avail_move)
            t_row, t_col = random.choice(enemy_avail_move)
            print(t_row, t_col)
            if t_row >= 0 and t_row < ROWS and t_col >=0 and t_col < COLS:
                if self.board[t_row][t_col] == 0:  
                    flying = Flying(enemy, enemy.row, enemy.col, t_row, t_col)
                    all_flyings.add(flying)
                    self.board[enemy.row][enemy.col], self.board[t_row][t_col] = self.board[t_row][t_col], self.board[enemy.row][enemy.col]
                    self.board[t_row][t_col].move(t_row, t_col)
        self.enemy_avail_moves = [] 

    def ai_before_shoot(self): 
        for enemy in all_enemies: 
            enemy_avail_shoot = enemy.calc_avail_shoot()
            self.enemy_avail_shoots.extend(enemy_avail_shoot)
            self.board[enemy.row][enemy.col].frame = 0 
            self.board[enemy.row][enemy.col].action = "attack"         

    def ai_shoot(self): 
        for enemy in all_enemies: 
            enemy_avail_shoot = enemy.calc_avail_shoot()
            if (player.row, player.col) in enemy_avail_shoot: 
                bullet = Bullet(enemy.row, enemy.col, player.row, player.col)
                all_bullets.add(bullet)
                self.board[enemy.row][enemy.col].frame = 0
                self.board[enemy.row][enemy.col].action = "idle"
            else: 
                print("pass")
                self.board[enemy.row][enemy.col].frame = 0
                self.board[enemy.row][enemy.col].action = "idle"     
        self.enemy_avail_shoots = []           

                  
class Unit(pygame.sprite.Sprite): 
    def __init__(self, type, row, col, animation, name, speed, range, health):
        pygame.sprite.Sprite.__init__(self)         
        self.type = type
        self.animation = animation 
        self.action = "idle"
        self.image = self.animation[self.action][0]
        self.rect = self.image.get_rect() 
        self.move(row, col) 
        self.name = name 
        self.speed = speed
        self.avail_move = []
        self.health = health 
        self.max_health = 100  
        self.range = range
        self.avail_shoot = [] 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()  

    def update(self):  
        now = pygame.time.get_ticks() 
        if now - self.last_update > 80: 
            self.last_update = now         
            self.frame += 1
            if len(self.animation[self.action]) == 1: 
                self.frame = 0 
            elif self.frame == len(self.animation[self.action]): 
                self.frame = 0              
            else: 
                if self.col + 1 <= COLS//2 :
                    self.image = pygame.transform.flip(self.animation[self.action][self.frame], True, False)
                    self.calc_pos()          
                elif self.col + 1 > COLS//2 : 
                    self.image = self.animation[self.action][self.frame]
                    self.calc_pos()
        
        if self.health <=0: 
            expl = Explosion(self.rect.centerx, self.rect.centery)
            all_explosions.add(expl)
            gameboard.board[self.row][self.col] = 0 
            self.kill() 
            print("kill unit")
            

    def calc_pos(self): 
        self.rect.x = self.col * SQUARE_SIZE - (self.image.get_width()-SQUARE_SIZE)//2
        self.rect.y = self.row * SQUARE_SIZE - (self.image.get_height()-SQUARE_SIZE)

    def draw_unit(self): 
        screen_2.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen_2, LIGHTRED, (self.rect.centerx-25, self.rect.y - 5, 50, 3))
        pygame.draw.rect(screen_2, LIGHTGREEN, (self.rect.centerx-25, self.rect.y - 5, 50 * self.health/self.max_health, 3))  

    def move(self, t_row, t_col): 
        self.row = t_row 
        self.col = t_col 
        self.calc_pos() 

    def calc_avail_move(self): 
        if self.speed == 1: 
            self.avail_move  = [(self.row -1, self.col), (self.row+1, self.col), (self.row, self.col-1), (self.row, self.col+1) ]
        elif self.speed == 2: 
            self.avail_move  = [(self.row -1, self.col), (self.row+1, self.col), (self.row, self.col-1), (self.row, self.col+1), 
                                (self.row -2, self.col), (self.row+2, self.col), (self.row, self.col-2), (self.row, self.col+2), 
                                (self.row -1, self.col-1), (self.row+1, self.col-1), (self.row-1, self.col+1), (self.row+1, self.col+1)
                                ]            
        else: 
            self.avail_move  = [(self.row -1, self.col), (self.row+1, self.col), (self.row, self.col-1), (self.row, self.col+1), 
                                (self.row -2, self.col), (self.row+2, self.col), (self.row, self.col-2), (self.row, self.col+2), 
                                (self.row -1, self.col-1), (self.row+1, self.col-1), (self.row-1, self.col+1), (self.row+1, self.col+1), 
                                (self.row -3, self.col), (self.row+3, self.col), (self.row, self.col-3), (self.row, self.col+3), 
                                (self.row -1, self.col-2), (self.row-2, self.col-1), 
                                (self.row -1, self.col+2), (self.row-2, self.col+1),
                                (self.row+2, self.col-1), (self.row+1, self.col-2),
                                (self.row+2, self.col+1), (self.row+1, self.col+2)
                                ]            
  
        return self.avail_move

    def calc_avail_shoot(self): 
        if self.range == 1: 
            self.avail_shoot  = [(self.row -1, self.col), (self.row+1, self.col), (self.row, self.col-1), (self.row, self.col+1) ]
        elif self.range == 2: 
            self.avail_shoot  = [(self.row -2, self.col), (self.row+2, self.col), (self.row, self.col-2), (self.row, self.col+2), 
                                (self.row -1, self.col-1), (self.row+1, self.col-1), (self.row-1, self.col+1), (self.row+1, self.col+1)
                                ]            
        else: 
            self.avail_shoot  = [(self.row -3, self.col), (self.row+3, self.col), (self.row, self.col-3), (self.row, self.col+3), 
                                (self.row -1, self.col-2), (self.row-2, self.col-1), 
                                (self.row -1, self.col+2), (self.row-2, self.col+1), 
                                (self.row+2, self.col-1), (self.row+1, self.col-2),
                                (self.row+2, self.col+1), (self.row+1, self.col+2)
                                ]            
  
        return self.avail_shoot
        

class Flying(pygame.sprite.Sprite):
    def __init__ (self, unit, row, col, t_row, t_col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row 
        self.col = col
        self.t_row = t_row
        self.t_col = t_col 
        self.animation = unit.animation["move"]
        self.o_image = self.animation[0]
        self.frame = 0 
        self.rect = self.o_image.get_rect() 
        self.speed = 10
        self.rect.x = int(self.col * SQUARE_SIZE + SQUARE_SIZE //2 - self.o_image.get_width()//2)
        self.rect.y = int(self.row * SQUARE_SIZE + SQUARE_SIZE //2 - self.o_image.get_height()//2)
        self.t_x = int(self.t_col * SQUARE_SIZE + SQUARE_SIZE //2 - self.o_image.get_width()//2) 
        self.t_y = int(self.t_row * SQUARE_SIZE + SQUARE_SIZE //2 - self.o_image.get_height()//2)
        self.angle = 0 


    def update(self): 

        x_diff = self.t_x - self.rect.x 
        y_diff = self.t_y - self.rect.y 
        angle_radians = math.atan2(y_diff, x_diff)
        move_x = math.cos(angle_radians) * self.speed
        move_y = math.sin(angle_radians) * self.speed
        self.rect.y += move_y 
        self.rect.x += move_x 

        if abs(self.t_y - self.rect.y) < self.speed:
            self.t_y = self.rect.y
        if abs(self.t_x - self.rect.x) < self.speed:
            self.t_x = self.rect.x             

        if self.t_y == self.rect.y and self.t_x == self.rect.x: 
            self.kill() 
            print("finish")

        self.frame += 1
        if self.frame == len(self.animation):
            self.frame = 0 
        else: 
            self.o_image = self.animation[self.frame]
            unit_mask = pygame.mask.from_surface(self.o_image)
            self.image = unit_mask.to_surface(setcolor = (0, 0, 0, 180), unsetcolor = (0, 0, 0, 0))


class Bullet(pygame.sprite.Sprite): 

    def __init__ (self, row, col, t_row, t_col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row 
        self.col = col
        self.t_row = t_row
        self.t_col = t_col 
        self.image = bullet_animation[0]
        self.frame = 0 
        self.rect = self.image.get_rect() 
        self.speed = 10
        self.rect.x = int(self.col * SQUARE_SIZE + SQUARE_SIZE //2 - self.image.get_width()//2)
        self.rect.y = int(self.row * SQUARE_SIZE + SQUARE_SIZE //2 - self.image.get_height()//2)
        self.t_x = int(self.t_col * SQUARE_SIZE + SQUARE_SIZE //2 - self.image.get_width()//2) 
        self.t_y = int(self.t_row * SQUARE_SIZE + SQUARE_SIZE //2 - self.image.get_height()//2)
        self.angle = 0 

    def update(self): 

        x_diff = self.t_x - self.rect.x 
        y_diff = self.t_y - self.rect.y 
        angle_radians = math.atan2(y_diff, x_diff)
        move_x = math.cos(angle_radians) * self.speed
        move_y = math.sin(angle_radians) * self.speed
        self.rect.y += move_y 
        self.rect.x += move_x 

        if abs(self.t_y - self.rect.y) < self.speed:
            self.t_y = self.rect.y
        if abs(self.t_x - self.rect.x) < self.speed:
            self.t_x = self.rect.x             

        if self.t_y == self.rect.y and self.t_x == self.rect.x: 
            if gameboard.board[self.t_row][self.t_col] != 0: 
                gameboard.board[self.t_row][self.t_col].health -= 20
                expl = Explosion(self.rect.centerx, self.rect.centery)
                all_explosions.add(expl)
            self.kill() 
            print("kill")

        self.frame += 1
        if self.frame == len(bullet_animation):
            self.frame = 0 
        else: 
            self.image = bullet_animation[self.frame]
        

class Explosion(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_animation[0]
        self.rect = self.image.get_rect() 
        self.rect.centerx = x
        self.rect.centery = y
        self.frame = 0 
    
    def update(self):
        self.frame += 1
        if self.frame == len(explosion_animation):
            self.kill() 
            return True 
        else: 
            self.image = explosion_animation[self.frame]        



#Sprite Group 
all_flyings = pygame.sprite.Group() 
all_units = pygame.sprite.Group() 
all_enemies = pygame.sprite.Group() 
all_bullets = pygame.sprite.Group() 
all_explosions = pygame.sprite.Group()


    
#setup game, player and enemies (sortie loop?) 
gameboard = Board() 

player = Unit("player", 5, 2, gundam_animation, "Gundam RX-78-2", 5, 3, 80)
all_units.add(player)
gameboard.board[player.row][player.col] = player

enemy_1 = Unit("enemy", 5, 5, deep_animation, "Deep Striker", 1, 3, 80)
all_units.add(enemy_1)
all_enemies.add(enemy_1)
gameboard.board[enemy_1.row][enemy_1.col] = enemy_1

enemy_2 = Unit("enemy", 7, 6, wing_animation, "Wing", 5, 2, 80)
all_units.add(enemy_2)
all_enemies.add(enemy_2)
gameboard.board[enemy_2.row][enemy_2.col] = enemy_2



#game loop 
run = True 
while run:

    clock.tick(FPS) 
    all_units.update()
    all_bullets.update()
    all_explosions.update()
    all_flyings.update()

    if len(all_explosions) != 0 and screen_shake == 0: 
        screen_shake = 50 
    screen_shake = max (0, screen_shake - 1)
    
    draw()

    if gameboard.turn == "enemy": 
        gameboard.change_turn_counter += 1 
        if gameboard.change_turn_counter == 25: 
            gameboard.ai_before_move()
        if gameboard.change_turn_counter == 50: 
            gameboard.ai_move()
        if gameboard.change_turn_counter == 75: 
            gameboard.ai_before_shoot()        
        if gameboard.change_turn_counter == 100: 
            gameboard.change_turn_counter = 0 
            gameboard.ai_shoot()            
            gameboard.turn = "player" 


    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False 
            
        if event.type == pygame.MOUSEBUTTONDOWN and gameboard.turn == "player": 
            if event.button == 1 and gameboard.selected_r == None: 
                mpos = pygame.mouse.get_pos() 
                row, col = get_grid_pos(mpos)
                print(row, col)
                if row < ROWS: 
                    gameboard.select_unit(row, col) 

            if event.button == 3:                 
                pos = pygame.mouse.get_pos() 
                row, col = get_grid_pos(pos)
                print(row, col)
                if row < ROWS: 
                    gameboard.before_shoot(row, col)

pygame.quit() 

#Copyright © 2025 by futuristickids (Instagram), Futuristic Kids(Facebook), ay.parentingworkshop@yahoo.com, andrewyip-workshop, Andrew Yip
#All rights reserved
#Copyright © 2025 by futuristickids (Instagram), Futuristic Kids(Facebook), ay.parentingworkshop@yahoo.com, Andrew Yip
#All rights reserved
