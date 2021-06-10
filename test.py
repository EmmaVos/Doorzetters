import pygame
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()
fps = 60

# Afmetingen scherm
screen_width = 800
screen_height = 800

# Scherm aanmaken
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CORONA SPEL DE DOORZETTERS")

# Globale variabelen
tile_size = 40
#player_health = 100
main_menu = True

# Kleuren Health bar
DARK_GREEN = (45, 201, 55)
LIGHT_GREEN = (153, 193, 64)
YELLOW = (231, 180, 22)
ORANGE = (219, 123, 43)
RED = (204, 50, 50)

# Kleuren algemeen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Afbeeldingen laden (eigen pad toevoegen niet nodig)
<<<<<<< Updated upstream
sun_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/zon.png"
)
bg_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/background.png"
)
dirt_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/modder.png"
)
grass_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/gras.png"
)
rutten_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/rutten.png"
)
# corona_img = pygame.image.load("corona.png")

start_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/start.png"
)
exit_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/exit.png"
)
menu_img = pygame.image.load(
    "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/menu.png"
)
=======
sun_img = pygame.image.load("zon.png")
bg_img = pygame.image.load("background.png")
dirt_img = pygame.image.load("modder.png")
grass_img = pygame.image.load("gras.png")
rutten_img = pygame.image.load("rutten.png")

start_img = pygame.image.load("start.png")
exit_img = pygame.image.load("exit.png")
menu_img = pygame.image.load("menu.png")
>>>>>>> Stashed changes

#Vijand inladen
corona_p_img = pygame.image.load("corona_paars.png")
corona_g_img = pygame.image.load("corona_groen.png")

<<<<<<< Updated upstream
# Muziek inladen
# pygame.mixer.init()
# pygame.mixer.music.load("/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/background_music.mp3")
# pygame.mixer.music.play(-1)
# spring = pygame.mixer.Sound(
#   "/Users/wout/Desktop/MINOR/Projectkraken/Doorzetters/spring.mp3"
# )
=======
# # Muziek inladen
# pygame.mixer.init()
# pygame.mixer.music.load("background_music.mp3")
# pygame.mixer.music.play(-1)
>>>>>>> Stashed changes

# Player parent class
class Player:
    def __init__(self, x, y):
        img = rutten_img
        self.image = pygame.transform.scale(img, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.health = 100
        self.save = 0
        self.first_kill = False
        self.hit_time = 0



    def update(self):
        dx = 0
        dy = 0

        # Bewegen
        key = pygame.key.get_pressed()
        # Beweging naar links
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True
            # pygame.mixer.music.stop()
            # pygame.mixer.Sound.play(spring)
            # pygame.mixer.music.play()

        if key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 5

        if key[pygame.K_RIGHT]:
            dx += 5

        # Hoogte springen bepalen
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # checken op botsingen met platformen
        self.in_air = True
        for tile in world.tile_list:
            # checken op botsing op x-as
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # checken voor botsing op de y-as
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                # checken of speler springt
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # checken of de speler valt
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

            # checken op botsingen met enemies
            #check for collision with enemies
        
        if pygame.sprite.spritecollide(self,corona_paars_group, False) and self.first_kill == False:
            self.health -=10
            self.first_kill = True
            self.hit_time=pygame.time.get_ticks()
         

            #check for collision with enemie
        if pygame.sprite.spritecollide(self,corona_groen_group, False) and self.first_kill == False:
            self.health -=20
            print("groen" , self.health)
            self.first_kill = True
            self.hit_time=pygame.time.get_ticks()

        if pygame.sprite.spritecollide(self,corona_paars_no_move_group, False) and self.first_kill == False:
            self.health -=10
            print("groen" , self.health)
            self.first_kill = True
            self.hit_time=pygame.time.get_ticks()
        
        if pygame.sprite.spritecollide(self,corona_groen_no_move_group, False) and self.first_kill == False:
            self.health -=20
            print("groen" , self.health)
            self.first_kill = True
            self.hit_time=pygame.time.get_ticks()

        # Update speler coordinaten
        self.rect.x += dx
        self.rect.y += dy
<<<<<<< Updated upstream

        # ------- onderstaand is niet nodig. Dit check is al in de collision op y-as
        # if self.rect.bottom > screen_height:
        #     self.rect.bottom = screen_height
        #     dy = 0
=======
        
        

>>>>>>> Stashed changes
        screen.blit(self.image, self.rect)
        return self.health
        


class Vijand(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image ##     ## uitzoeken hoe dit werkt met twee verschillende groepen
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        self.beweeg_richting=1
        self.beweeg_teller=0

    def update(self):
        self.rect.x += self.beweeg_richting
        self.beweeg_teller += 1
        if abs (self.beweeg_teller) > 50:
            self.beweeg_richting *= -1
            self.beweeg_teller *= -1


# Wereld class, zorgt voor tegels aanmaken
class World:
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Modder blokjes
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # Gras blokjes
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  # 3 had volgens mij nog geen inhoud
                    corona_paars = Vijand(col_count*tile_size, row_count*tile_size, corona_p_img )
                    corona_paars_group.add(corona_paars)
                if tile == 4:  # 4 had volgens mij nog geen inhoud
                    corona_groen = Vijand(col_count*tile_size, row_count*tile_size, corona_g_img)
                    corona_groen_group.add(corona_groen)
                if tile == 5:  # 3 had volgens mij nog geen inhoud
                    corona_paars_no_move = Vijand(col_count*tile_size, row_count*tile_size, corona_p_img )
                    corona_paars_no_move_group.add(corona_paars)
                if tile == 6:  # 4 had volgens mij nog geen inhoud
                    corona_groen_no_move = Vijand(col_count*tile_size, row_count*tile_size, corona_g_img)
                    corona_groen_no_move_group.add(corona_groen)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (WHITE), tile[1], 2)

def get_color(health):
    color = BLACK
    if health == 100:
        color = DARK_GREEN
    elif health >= 80:
        color = LIGHT_GREEN
    elif health >= 60:
        color = YELLOW
    elif health >= 40:
        color = ORANGE
    elif health >= 0:
        color = RED
    return color

# Health bar tekenen (loopt af met stappen van 20)
def draw_health():
    pygame.draw.rect(screen, (BLACK), (560, 20, 200, 40), 2)
    pygame.draw.rect(screen, get_color(player.health), (560, 20, player.health * 2, 40))
    if player.health <= 0:
        print("GAME OVER")

<<<<<<< Updated upstream
=======
def draw_savings():
    pygame.draw.rect(screen, (BLACK), (240, 20, 120, 40), 2)
    if player.save == 1:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 40, 40), 2)
    if player.save == 2:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 80, 40), 2)
    if player.save == 3:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 120, 40), 2)


>>>>>>> Stashed changes

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0]:
            self.clicked = False

        # teken button
        screen.blit(self.image, self.rect)

        return action


<<<<<<< Updated upstream
=======
def hit_cooldown():
    if player.first_kill == True:
        if player.hit_time + 500 < pygame.time.get_ticks():
            player.first_kill = False
            print("cooldown complete")

>>>>>>> Stashed changes
# data van de wereld > bepaald welke afbeelding if tile == waar wordt geplaast.
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
    [1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 4, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]



#Vijandjes
corona_groen_group= pygame.sprite.Group()
corona_paars_group= pygame.sprite.Group()
corona_groen_no_move_group =pygame.sprite.Group()
corona_paars_no_move_group =pygame.sprite.Group()



# Objecten
player = Player(100, screen_height - 130)
world = World(world_data)

# Buttons
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
menu_button = Button(50, 20, menu_img)



# Game mainloop
run = True
while run:
<<<<<<< Updated upstream
    clock.tick
=======
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    


>>>>>>> Stashed changes
    screen.blit(bg_img, (0, 0))  # Plaatsen achtergrond
    screen.blit(sun_img, (100, 100))  # Plaatsen zon

    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:  # Indent alles hieronder in de else statement

        world.draw() 
        corona_groen_group.draw(screen)
        corona_groen_group.update()
        corona_paars_group.draw(screen)
        corona_paars_group.update()
        corona_groen_no_move_group.draw(screen)
        corona_paars_no_move_group.draw(screen)



        hit_cooldown()
        player.update()

        
        draw_health()  # Plaatsen health bar
        draw_savings()


        if menu_button.draw():
            main_menu = True

    pygame.display.update()  # Update het scherm

pygame.quit()
