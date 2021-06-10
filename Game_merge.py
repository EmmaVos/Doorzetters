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
# player_health = 100
main_menu = True
expl_menu = False
play_timer = True
draw_world = True


# Kleuren Health bar
DARK_GREEN = (45, 201, 55)
LIGHT_GREEN = (153, 193, 64)
YELLOW = (231, 180, 22)
ORANGE = (219, 123, 43)
RED = (204, 50, 50)

# Kleuren algemeen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Afbeeldingen laden
sun_img = pygame.image.load("zon.png")
bg_img = pygame.image.load("background.png")
dirt_img = pygame.image.load("modder.png")
grass_img = pygame.image.load("gras.png")
rutten_img = pygame.image.load("rutten.png")

# startscherm afbeeldingen laden
start_img_og = pygame.image.load("start.png")
exit_img_og = pygame.image.load("exit.png")
menu_img_og = pygame.image.load("menu.png")
start_game_img_og = pygame.image.load("start_game.png")
expl_img_og = pygame.image.load("expl.png")
back_img_og = pygame.image.load("terug.png")
start_screen_og = pygame.image.load("start_window.png")

# Afbeeldingen startscherm sizen
start_img = pygame.transform.scale(start_img_og, (240, 120))
exit_img = pygame.transform.scale(exit_img_og, (240, 120))
menu_img = pygame.transform.scale(menu_img_og, (120, 40))
start_game_img = pygame.transform.scale(start_game_img_og, (240, 120))
expl_img = pygame.transform.scale(expl_img_og, (800, 800))
back_img = pygame.transform.scale(back_img_og, (240, 120))
start_screen_img = pygame.transform.scale(start_screen_og, (800, 800))


# Countdown afbeeldingen laden
een_img_og = pygame.image.load("1.png")
twee_img_og = pygame.image.load("2.png")
drie_img_og = pygame.image.load("3.png")

een_img = pygame.transform.scale(een_img_og, (400, 400))
twee_img = pygame.transform.scale(twee_img_og, (400, 400))
drie_img = pygame.transform.scale(drie_img_og, (400, 400))

# Vijand inladen
corona_p_img = pygame.image.load("corona_paars.png")
corona_g_img = pygame.image.load("corona_groen.png")
kappie_img = pygame.image.load("kapje.png")
deur_img = pygame.image.load("poort.png")
mondkapje_img = pygame.image.load("kapje.png")
vaccin_img = pygame.image.load("spuit.png")

# # Muziek inladen
# pygame.mixer.init()
# pygame.mixer.music.load("background_music.mp3")
# pygame.mixer.music.play(-1)

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
        self.hit_time = 0
        self.is_hit = False

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
                    self.in_air = False

            # checken op botsingen met enemies
            # check for collision with enemies

        if (
            pygame.sprite.spritecollide(self, corona_paars_group, False)
            and self.first_kill == False
        ):
            self.health -= 10
            self.first_kill = True
            self.hit_time_enemy = pygame.time.get_ticks()

            # check for collision with enemie
        if (
            pygame.sprite.spritecollide(self, corona_groen_group, False)
            and self.first_kill == False
        ):
            self.health -= 20
            self.first_kill = True
            self.hit_time_enemy = pygame.time.get_ticks()

        if (
            pygame.sprite.spritecollide(self, corona_paars_no_move_group, False)
            and self.first_kill == False
        ):
            self.health -= 10
            self.first_kill = True
            self.hit_time_enemy = pygame.time.get_ticks()

        if (
            pygame.sprite.spritecollide(self, corona_groen_no_move_group, False)
            and self.first_kill == False
        ):
            self.health -= 20
            self.first_kill = True
            self.hit_time_enemy = pygame.time.get_ticks()

        ######## collision met spaar spullen #######

        if (
            pygame.sprite.spritecollide(self, mondkapje_group, False)
            and self.first_kill == False
        ):
            self.health += 20
            print("mondkapje", self.health)
            self.first_kill = True
            self.hit_time_enemy = pygame.time.get_ticks()

        if (
            pygame.sprite.spritecollide(self, vaccin_group, False)
            and self.first_save == False
        ):
            self.save += 1
            print("injectie", self.save)
            self.first_save = True
            self.hit_time_interactable = pygame.time.get_ticks()

        if (
            pygame.sprite.spritecollide(self, deur_group, False)
            and self.first_kill == False
        ):
            if player.save == 3:
                Deur.is_hit = True
                print(Deur.is_hit)
                self.hit_time = pygame.time.get_ticks() + 2000
            else:
                print("You have to earn more stuff")

        # Update speler coordinaten
        self.rect.x += dx
        self.rect.y += dy

        screen.blit(self.image, self.rect)
        return self.health
        return self.save


class Deur(pygame.sprite.Sprite):
    is_hit = False

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = (
            image  ##     ## uitzoeken hoe dit werkt met twee verschillende groepen
        )
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mondkapje(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = (
            image  ##     ## uitzoeken hoe dit werkt met twee verschillende groepen
        )
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Vaccin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = (
            image  ##     ## uitzoeken hoe dit werkt met twee verschillende groepen
        )
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Vijand(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = (
            image  ##     ## uitzoeken hoe dit werkt met twee verschillende groepen
        )
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.beweeg_richting = 1
        self.beweeg_teller = 0

    def update(self):
        self.rect.x += self.beweeg_richting
        self.beweeg_teller += 1
        if abs(self.beweeg_teller) > 50:
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
                    corona_paars = Vijand(
                        col_count * tile_size, row_count * tile_size, corona_p_img
                    )
                    corona_paars_group.add(corona_paars)
                if tile == 4:  # 4 had volgens mij nog geen inhoud
                    corona_groen = Vijand(
                        col_count * tile_size, row_count * tile_size, corona_g_img
                    )
                    corona_groen_group.add(corona_groen)
                if tile == 5:  # 3 had volgens mij nog geen inhoud
                    corona_paars_no_move = Vijand(
                        col_count * tile_size, row_count * tile_size, corona_p_img
                    )
                    corona_paars_no_move_group.add(corona_paars_no_move)
                if tile == 6:  # 4 had volgens mij nog geen inhoud
                    corona_groen_no_move = Vijand(
                        col_count * tile_size, row_count * tile_size, corona_g_img
                    )
                    corona_groen_no_move_group.add(corona_groen_no_move)
                if tile == 7:
                    deur = Deur(col_count * tile_size, row_count * tile_size, deur_img)
                    deur_group.add(deur)

                if tile == 8:
                    mondkapje = Mondkapje(
                        col_count * tile_size, row_count * tile_size, mondkapje_img
                    )
                    mondkapje_group.add(mondkapje)
                if tile == 9:
                    vaccin = Vaccin(
                        col_count * tile_size, row_count * tile_size, vaccin_img
                    )
                    vaccin_group.add(vaccin)

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
    if player.health >= 100:
        player.health = 100
    pygame.draw.rect(screen, get_color(player.health), (560, 20, player.health * 2, 40))
    if player.health <= 0:
        print("GAME OVER")


def draw_savings():
    pygame.draw.rect(screen, (BLACK), (240, 20, 120, 40), 2)
    if player.save == 1:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 40, 40))
    if player.save == 2:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 80, 40))
    if player.save == 3:
        pygame.draw.rect(screen, (DARK_GREEN), (240, 20, 120, 40))


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


def hit_cooldown():
    if player.is_hit == True:
        if player.hit_time < pygame.time.get_ticks():
            player.is_hit = False
            print("cooldown complete")


def beginning_timer():
    timer_array = [een_img, twee_img, drie_img]

    seconds = 2
    while seconds >= 0:
        screen.blit(timer_array[seconds], (200, 200))
        pygame.display.update()
        pygame.time.delay(1000)
        seconds -= 1


# data van de wereld > bepaald welke afbeelding if tile == waar wordt geplaast.
def saving_cooldown():
    if player.first_save == True:
        if player.hit_time_interactable + 4000 < pygame.time.get_ticks():
            player.first_save = False
            print("saving complete")


# data van de wereld > bepaald welke afbeelding if tile == waar wordt geplaast.
world_data = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 4, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 1],
        [1, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 9, 9, 7, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
        [1, 0, 0, 0, 9, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 1],
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
    ],
]


# Vijandjes
corona_groen_group = pygame.sprite.Group()
corona_paars_group = pygame.sprite.Group()
corona_groen_no_move_group = pygame.sprite.Group()
corona_paars_no_move_group = pygame.sprite.Group()
deur_group = pygame.sprite.Group()
mondkapje_group = pygame.sprite.Group()
vaccin_group = pygame.sprite.Group()


currentLevel = 0

# Objecten
player = Player(100, screen_height - 100)
world = World(world_data)

# Buttons
start_button = Button(100, 340, start_img)
exit_button = Button(450, 340, exit_img)
menu_button = Button(20, 20, menu_img)
start_game_button = Button(460, 630, start_game_img)
back_button = Button(100, 630, back_img)

world = World(world_data[currentLevel])

# Game mainloop
run = True
while run:
    print(Deur.is_hit, "mainloop")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg_img, (0, 0))  # Plaatsen achtergrond
    screen.blit(sun_img, (100, 100))  # Plaatsen zon

    if main_menu == True:
        screen.blit(start_screen_img, (0, 0))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
            expl_menu = True
    elif expl_menu == True:
        screen.blit(expl_img, (0, 0))
        if start_game_button.draw():
            expl_menu = False
            play_timer = True
        if back_button.draw():
            expl_menu = False
            main_menu = True
    else:  # Indent alles hieronder in de else statement

        world.draw()

        corona_groen_group.draw(screen)
        corona_groen_group.update()
        corona_paars_group.draw(screen)
        corona_paars_group.update()
        corona_groen_no_move_group.draw(screen)
        corona_paars_no_move_group.draw(screen)
        deur_group.draw(screen)
        mondkapje_group.draw(screen)
        vaccin_group.draw(screen)
        ######## proberen ########   testen of onderstaande regels wel nodig zijn
        deur_group.update()
        mondkapje_group.update()
        vaccin_group.update()

        if Deur.is_hit == True and Vaccin > 3:
            print("Joepie het werkt eindelijk")

            currentLevel += 1
            world = World(world_data[currentLevel])
            Deur.is_hit = False

        player.update()

        draw_savings()
        draw_health()  # Plaatsen health bar

        if menu_button.draw():
            main_menu = True

        if play_timer:
            beginning_timer()
            play_timer = False

    pygame.display.update()  # Update het scherm

pygame.quit()
