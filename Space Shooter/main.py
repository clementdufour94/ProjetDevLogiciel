from numpy import empty
import pygame
import os
import random
import pickle
from pygame import mixer



from pygame.constants import MOUSEBUTTONDOWN
pygame.font.init()
pygame.init()

mixer.music.load("assets/background.wav")
mixer.music.play(-1)

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeux de tir projet Dev")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
HEART = pygame.image.load(os.path.join("assets", "heart.png"))
BOLT = pygame.image.load(os.path.join("assets", "bolt.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED2_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red2.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
RED_LASER2 = pygame.image.load(os.path.join("assets", "pixel_laser_red2.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30
    

    def __init__(self, x, y, health=100, score=0, player_vel=5, player_name=""):
        self.x = x
        self.y = y
        self.health = health
        self.score = score
        self.player_name = player_name
        self.player_vel = player_vel
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0


    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()




class Player(Ship):
    
    def __init__(self, x, y, health=100, player_vel=5, score=0, player_name=""):
        super().__init__(x, y, health, player_vel, score, player_name)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.player_vel = player_vel
        self.score = score
        self.player_name = player_name
        

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        
                        objs.remove(obj)
                        self.score += 100
                        
                        
                        
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                
            
        


    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))




class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1




class Heart(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = HEART
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
class Bolt(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = BOLT
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel



    


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = choix.level
    
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    hearts = []
    heart_vel= 1
    bolts = []
    bolt_vel= 1
    
    wave_length = choix.wave_length
    enemy_vel = 1

    laser_vel = 5
    
    

    player = Player(30, 630)
    player2 = Player(630, 630)
    player2.ship_img = RED2_SPACE_SHIP
    player2.laser_img = RED_LASER2
    player.player_name = "Joueur 1"
    player2.player_name = "Joueur 2"


    clock = pygame.time.Clock()

    lost = False
    
    lost_count = 0

    def pause():
        loop= 1
        
        while loop:
    
            title_font = pygame.font.SysFont("comicsans", 50)
            jouer = title_font.render("Pause", 1, (255,255,255))
            option = title_font.render("Pour reprendre le jeux appuyer sur Entrée", 1, (255,255,255))
            

            
            WIN.blit(jouer, (320, 215))
            WIN.blit(option, (15, 315))
            
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_RETURN:
                        loop = 0
            pygame.display.update()
            clock.tick(60)
            

    

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Vies : {lives}", 1, (255,255,255))

        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"Score {player.player_name} : {player.score}", 1, (255,255,255))
        score_label2 = main_font.render(f"Score {player2.player_name} : {player2.score}", 1, (255,255,255))
        lost_label = lost_font.render(f"{player.player_name} à gagner!!", 1, (255,255,255))
        lost_label2 = lost_font.render(f"{player2.player_name} à gagner!!", 1, (255,255,255))
        lost_label3 = lost_font.render("Egalité !!", 1, (255,255,255))

        WIN.blit(score_label, (10, 10))
        WIN.blit(score_label2, (10, 60))
        WIN.blit(lives_label, (10, 110))
    
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        for heart in hearts:
            heart.draw(WIN)
        for bolt in bolts:
            bolt.draw(WIN)
        

        player.draw(WIN)
        player2.draw(WIN)
        
        best_score_temp=0
        
        
        
        

        if lost:
            if player.score < player2.score : # Player2
                
                WIN.blit(lost_label2, (WIDTH/2 - lost_label2.get_width()/2, 350))
                WIN.blit(score_label, (WIDTH/2 - lost_label.get_width()/2, 400))
                WIN.blit(score_label2, (WIDTH/2 - lost_label.get_width()/2, 450))
                best_score_temp = [player2.score]
                
                # Chargement du meilleur score 
                with open('savefile.dat', 'rb') as f:
                    best_score = pickle.load(f)
                #Si score temporaire sup à bestscore alors on sauvegarde bestscore
                
                if best_score_temp > best_score:
                    best_score = best_score_temp
                    with open('savefile.dat', 'wb') as f:
                        pickle.dump(best_score, f, protocol=2)
                
            if player.score > player2.score: # Player1
                
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
                WIN.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 400))
                WIN.blit(score_label2, (WIDTH/2 - score_label2.get_width()/2, 450))
                best_score_temp = [player.score]
                 # Chargement du meilleur score 
                with open('savefile.dat', 'rb') as f:
                    best_score = pickle.load(f)
                #Si score temporaire sup à bestscore alors on sauvegarde bestscore
            
                if best_score_temp > best_score:
                    best_score = best_score_temp
                    with open('savefile.dat', 'wb') as f:
                        pickle.dump(best_score, f, protocol=2)
               
            if player.score == player2.score: #

                WIN.blit(lost_label3, (WIDTH/2 - lost_label3.get_width()/2, 350))
                WIN.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 400))
                WIN.blit(score_label2, (WIDTH/2 - score_label2.get_width()/2, 450))
                best_score_temp = player2.score
                 # Chargement du meilleur score 
                with open('savefile.dat', 'rb') as f:
                    best_score = pickle.load(f)
                #Si score temporaire sup à bestscore alors on sauvegarde bestscore
                
                if best_score_temp > best_score:
                    best_score = best_score_temp
                    with open('savefile.dat', 'wb') as f:
                        pickle.dump(best_score, f, protocol=2)


        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0 or player2.health <= 0 :
            lost = True
            lost_count += 1

        

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        
        if len(enemies) == 0:
            level += 1
            player.player_vel = 5
            player2.player_vel = 5
            player.health += 3
            player2.health += 3
            wave_length += 5

            if level%5 == 0:
                lives +=2
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                heart = Heart(random.randrange(50, WIDTH-100), random.randrange(-10500, -100))
                hearts.append(heart)
                bolt = Bolt(random.randrange(50, WIDTH-100), random.randrange(-10500, -100))
                bolts.append(bolt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and player.x - player.player_vel > 0: # left
            player.x -= player.player_vel
        if keys[pygame.K_d] and player.x + player.player_vel + player.get_width() < WIDTH: # right
            player.x += player.player_vel
        if keys[pygame.K_z] and player.y - player.player_vel > 0: # up
            player.y -= player.player_vel
        if keys[pygame.K_s] and player.y + player.player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player.player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            bulletSound = mixer.Sound("assets/laser.wav")
            bulletSound.play()

        if keys[pygame.K_LEFT] and player2.x - player2.player_vel > 0: # left
            player2.x -= player2.player_vel
        if keys[pygame.K_RIGHT] and player2.x + player2.player_vel + player2.get_width() < WIDTH: # right
            player2.x += player2.player_vel
        if keys[pygame.K_UP] and player2.y - player2.player_vel > 0: # up
            player2.y -= player2.player_vel
        if keys[pygame.K_DOWN] and player2.y + player2.player_vel + player.get_height() + 15 < HEIGHT: # down
            player2.y += player2.player_vel
        if keys[pygame.K_KP1]:
            player2.shoot()
            bulletSound = mixer.Sound("assets/laser.wav")
            bulletSound.play()
        if keys[pygame.K_ESCAPE]:
            pause()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            enemy.move_lasers(laser_vel, player2)


            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                player.score -= 10
                if player.score <0:
                    player.score =0
                enemies.remove(enemy)
            elif collide(enemy, player2):
                    player2.health -= 10
                    player2.score -= 10
                    if player2.score <0:
                        player2.score =0
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        for heart in hearts[:]:
            heart.move(heart_vel)
            if collide(heart, player):

                
                player.health += 10
                hearts.remove(heart)
                
            elif collide(heart, player2):
                    
                    player2.health += 10
                    hearts.remove(heart)
            elif heart.y + heart.get_height() > HEIGHT:
                hearts.remove(heart)
        for bolt in bolts[:]:
            bolt.move(bolt_vel)

            if collide(bolt, player):
    
                
                player.player_vel += 2

                bolts.remove(bolt)
                
            elif collide(bolt, player2):
                    
                player2.player_vel += 2

                bolts.remove(bolt)

            elif bolt.y + bolt.get_height() > HEIGHT:
                bolts.remove(bolt)

        
                    
           
        player.move_lasers(-laser_vel, enemies)
        player2.move_lasers(-laser_vel, enemies)



def main_menu():
        title_font = pygame.font.SysFont("comicsans", 30)
        score_font = pygame.font.SysFont("comicsans", 50)
        run = True
        click = False

        with open('savefile.dat', 'rb') as f:
            best_score = pickle.load(f)

        
        while run:
            mx, my = pygame.mouse.get_pos()
            
            WIN.blit(BG, (0,0))
            
            jouer = title_font.render("Jouer", 1, (255,255,255))
            option = title_font.render("Règles", 1, (255,255,255))
            quitter  = title_font.render("Quitter", 1, (255,255,255))
            button_1 = pygame.Rect(225,100,300,50)
            button_2 = pygame.Rect(225,200,300,50)
            button_3 = pygame.Rect(225,300,300,50)

            texte_score = score_font.render("Meilleur Score :", 1, (255,255,255))
            score_score = score_font.render(f"{best_score}", 1, (255,255,255))
            
            
            pygame.draw.rect(WIN, (128, 128, 128), button_1)
            pygame.draw.rect(WIN, (128, 128, 128), button_2)
            pygame.draw.rect(WIN, (128, 128, 128), button_3)
            WIN.blit(jouer, (350, 115))
            WIN.blit(option, (350, 215))
            WIN.blit(quitter, (350, 315))
            WIN.blit(texte_score, (240, 515))
            WIN.blit(score_score, (350, 615))
            pygame.display.update()
            if button_1.collidepoint((mx,my)):
                if click:
                    choix()
                    
            if button_2.collidepoint((mx,my)):
                if click:
                    regles()
                
            if button_3.collidepoint((mx,my)):
                if click:
                    run = False
                    
            click= False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button ==1:
                        
                        click=True
            
        pygame.quit()
        main_menu()
def regles():
        run = True
        click = False
        
        while run:
            mx, my = pygame.mouse.get_pos()
            WIN.blit(BG, (0, 0))
            title_font = pygame.font.SysFont("comicsans", 25)
            regles = title_font.render(
                "C'est un jeu de tirs multijoueurs ou le but est de faire un meilleur score que l'autre ", 1, (255, 255, 255))
            regles1 = title_font.render("joueur. Pour cela vous devez tirer sur les vaisseaux ennemis sans mourir. Lorsqu’un", 1, (255, 255, 255))
            regles2 = title_font.render("joueur n’a plus de vie c’est la fin de la partie. Les ennemies sont réparties en vagues ", 1, (255, 255, 255))
            regles3 = title_font.render("qui a chaque niveau augmente. Pour vous aider vous pouvez récupérer des objets : ", 1, (255, 255, 255))
            regles4 = title_font.render("Les cœurs vont font augmenter la vie et les éclairs la vitesse de déplacement jusqu’au ", 1, (255, 255, 255))
            regles5 = title_font.render("prochain niveau. Les commandes pour le joueur 1 sont Z,Q,S,D pour se déplacer", 1, (255, 255, 255))
            regles6 = title_font.render("et espace pour tirer et pour le joueur 2 les flèches directionnelles du clavier ", 1, (255, 255, 255))
            regles7 = title_font.render("et Numpad01 pour tirer.", 1, (255, 255, 255))
            jouer = title_font.render("Retour", 1, (255, 255, 255))

            button_1 = pygame.Rect(225, 600, 300, 50)
            pygame.draw.rect(WIN, (128, 128, 128), button_1)
            WIN.blit(jouer, (340, 615))
            WIN.blit(regles, (25, 115))
            WIN.blit(regles1, (25, 165))
            WIN.blit(regles2, (25, 215))
            WIN.blit(regles3, (25, 265))
            WIN.blit(regles4, (25, 315))
            WIN.blit(regles5, (25, 365))
            WIN.blit(regles6, (25, 415))
            WIN.blit(regles7, (25, 465))

            pygame.display.update()

            if button_1.collidepoint((mx, my)):
                if click:
                    run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:

                        click = True
def choix():
        title_font = pygame.font.SysFont("comicsans", 30)
        run = True
        level = 0
        wave_length = 0
        click = False
        while run :
            mx, my = pygame.mouse.get_pos()
            
            WIN.blit(BG, (0,0))

            
            jouer = title_font.render("Normal", 1, (255,255,255))
            option = title_font.render("Difficile", 1, (255,255,255))
            quitter  = title_font.render("Retour", 1, (255,255,255))
            button_1 = pygame.Rect(225,100,300,50)
            button_2 = pygame.Rect(225,200,300,50)
            button_3 = pygame.Rect(225,300,300,50)  
            pygame.draw.rect(WIN, (128, 128, 128), button_1)
            pygame.draw.rect(WIN, (128, 128, 128), button_2)
            pygame.draw.rect(WIN, (128, 128, 128), button_3)
            WIN.blit(jouer, (350, 115))
            WIN.blit(option, (350, 215))
            WIN.blit(quitter, (350, 315))
            pygame.display.update()
            if button_1.collidepoint((mx,my)):
                if click:
                    choix.level = 0
                    choix.wave_length = 5
                    main()
                    
            if button_2.collidepoint((mx,my)):
                if click:
                    choix.level = 4
                    choix.wave_length = 10
                    main()
                    
                
            if button_3.collidepoint((mx,my)):
                if click:
                    run = False
                    
            click= False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button ==1:
                        
                        click=True
main_menu()
