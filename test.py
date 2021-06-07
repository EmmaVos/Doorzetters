import pygame
from pygame.locals import *


pygame.init()

# Afmetingen scherm
screen_width = 800
screen_height = 800

# Scherm aanmaken
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CORONA SPEL DE DOORZETTERS")

# Globale variabelen
tile_size = 40
player_health = 100

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
sun_img = pygame.image.load("zon.png")
bg_img = pygame.image.load("background.png")
dirt_img = pygame.image.load("modder.png")
grass_img = pygame.image.load("gras.png")
rutten_img = pygame.image.load("rutten.png")
corona_img = pygame.image.load("corona.png")

# Muziek inladen
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)


# Grid tekenen van de wereld
# ----- deze kan er gewoon uit blijven toch?-----
# def draw_grid():
#     for line in range(0, 20):
#         pygame.draw.line(
#             screen,
#             (255, 255, 255),
#             (0, line * tile_size),
#             (screen_width, line * tile_size),
#         )
#         pygame.draw.line(
#             screen,
#             (255, 255, 255),
#             (line * tile_size, 0),
#             (line * tile_size, screen_height),
#         )

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

    def update(self):
        dx = 0
        dy = 0

        # Bewegen
        key = pygame.key.get_pressed()
        # Beweging naar links
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True

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
            if tile[1].colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                dx = 0
            # checken voor botsing op de y-as
            if tile[1].colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                # checken of speler springt
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # checken of de speler valt
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air= False

        # Update speler coordinaten
        self.rect.x += dx
        self.rect.y += dy
        
        # ------- onderstaand is niet nodig. Dit check is al in de collision op y-as
        # if self.rect.bottom > screen_height:
        #     self.rect.bottom = screen_height
        #     dy = 0
        screen.blit(self.image, self.rect)


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
                # -------- corona kunnen we misschien beter los plaatsen ipv. in het grid-----
                # if tile == 3: #corona
                #     img = pygame.transform.scale(corona_img, (tile_size, tile_size))
                #     img_rect = img.get_rect()
                #     img_rect.x = col_count * tile_size
                #     img_rect.y = row_count * tile_size
                #     tile = (img, img_rect)
                #     self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (WHITE), tile[1], 2)


# Health bar tekenen (loopt af met stappen van 20)
def draw_health():
    pygame.draw.rect(screen, (BLACK), (560, 20, 200, 40), 2)

    if player_health == 100:
        pygame.draw.rect(screen, (DARK_GREEN), (560, 20, 200, 40))
    elif player_health == 80:
        pygame.draw.rect(screen, (LIGHT_GREEN), (560, 20, 160, 40))
    elif player_health == 60:
        pygame.draw.rect(screen, (YELLOW), (560, 20, 120, 40))
    elif player_health == 40:
        pygame.draw.rect(screen, (ORANGE), (560, 20, 80, 40))
    elif player_health == 20:
        pygame.draw.rect(screen, (RED), (560, 20, 40, 40))
    elif player_health == 0:
        print("GAME OVER")


# data van de wereld > bepaald welke afbeelding if tile == waar wordt geplaast.
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

world_data2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Objecten
player = Player(100, screen_height - 130)
world = World(world_data)

# Game mainloop
run = True
while run:

    screen.blit(bg_img, (0, 0))  # Plaatsen achtergrond
    screen.blit(sun_img, (100, 100))  # Plaatsen zon

    world.draw()  # Plaatsen wereld tegels
    player.update()  # Plaatsen speler

    # draw_grid() #Plaatsen grid --> hoeft niet toch?

    draw_health()  # Plaatsen health bar

    # Zorgt voor het sluiten van de game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()  # Update het scherm

pygame.quit()
