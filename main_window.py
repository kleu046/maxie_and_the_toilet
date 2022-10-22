import random
import math

import pygame

from pygame.locals import (
    RLEACCEL,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

KEY_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (202, 217, 184)


class Maxie(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super(Maxie, self).__init__()

        self.x = x
        self.y = y
        self.r = r

        #self.surf = pygame.Surface((self.r, self.r))
        #self.surf.fill(color = KEY_COLOR)
        #self.surf.set_colorkey(KEY_COLOR, RLEACCEL)
        self.surf = pygame.image.load("maxie.png").convert() # maxie
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect(center = (self.x, self.y))

        self.angle = 0

        # for i in range(0, 50, 2):
        #     #pygame.draw.ellipse(self.surf, WHITE, pygame.Rect((0,self.r*(1/3)), (self.r, self.r* (1/3))), self.r)
        #     pygame.draw.circle(self.surf, WHITE, (self.r/2+i, self.r/2+i), self.r/2*0.9**i, 2)

    def update(self, x, y, v):
        self.x = x
        self.y = y
        self.angle = (self.angle + v * 0.1)%360 # new angle for surface
        self.rotated_surf = pygame.transform.rotate(self.surf.copy(), self.angle) # rotate a copy
        self.rect = self.rotated_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.rotated_surf, self.rect)

class Poop(pygame.sprite.Sprite):
    def __init__(self, x, y, r = 5, color = (255, 0, 0), line_width = 1):
        super(Poop, self).__init__()

        self.x = x
        self.y = y
        self.r = r
        self.color = color

        self.angle = random.randint(0,360)
        self.rot_v = random.random() / 10

        if color == (0, 0, 255):
            self.surf = pygame.image.load("banana.png").convert() # banance - blue poop
        elif color == (128, 128, 128):
            self.surf = pygame.image.load("toiletpaper.png").convert() # toilet paper - grey poop
        else:
            self.surf = pygame.image.load("poop.png").convert()  # poop - red poop

        self.surf.set_colorkey(BLACK, RLEACCEL)
        #self.surf = pygame.Surface((self.r, self.r))
        #self.surf.fill(color=KEY_COLOR)
        #self.surf.set_colorkey(KEY_COLOR, RLEACCEL)
        #self.rect = self.surf.get_rect(center = (self.r, self.r))

        #pygame.draw.line(self.surf,color,(0,0),(self.r,self.r), width = line_width)
        #pygame.draw.line(self.surf,color,(self.r,0),(0,self.r), width = line_width)
        #pygame.draw.line(self.surf,(color[0],color[1]+210,color[0]),(round(self.r/2,0),round(self.r/2,0)),(round(self.r/2,0),round(self.r/2,0)))

        self.rotated_surf = pygame.transform.rotate(self.surf.copy(), self.angle)  # rotate a copy
        self.rect = self.rotated_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.rotated_surf, self.rect)

    def move(self, xy, speed = 1):
        x_c, y_c = xy

        if abs(self.x - x_c) < speed * 2 and abs(self.y - y_c) < speed * 2:
            self.kill()
            return 1

        else:
            self.d = (y_c - self.y) / (x_c - self.x) # slope
            c = y_c - self.d * x_c # intercept

            dx = speed / math.sqrt(1+self.d**2)
            if self.x < x_c:
                self.x += dx
            else:
                self.x -= dx
            self.y = (self.x * self.d + c)
            return 0


    def update(self):
        self.angle += 2
        self.rotated_surf = pygame.transform.rotate(self.surf.copy(), self.angle * self.rot_v)  # rotate a copy
        self.rect = self.rotated_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.rotated_surf, self.rect)

pygame.init()
clock = pygame.time.Clock()
clock.tick(10)

mouse_enabled = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
poops = pygame.sprite.Group()
maxie = Maxie(400,300,40)

random_tick = None
running = True

score = 0
blue_hit = 1

mouse_x = 0
mouse_y = 0
mouse_v = 0

poop_speed = 0.1

black_hole_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

toilet_bowl = pygame.image.load("toiletbowl.png").convert()
toilet_bowl.set_colorkey(BLACK, RLEACCEL)
toilet_bowl_rotated = pygame.transform.rotate(toilet_bowl.copy(), random.randint(0,360))

spawn_positions  =[]
for i in range(1, SCREEN_WIDTH, 2):
    if i > 35:
        spawn_positions.append((i, -35))
    spawn_positions.append((i, SCREEN_HEIGHT + 35))
for j in range(1, SCREEN_HEIGHT, 2):
    if j > 35:
        spawn_positions.append((-35, j))
    spawn_positions.append((SCREEN_WIDTH + 35, j))

font = pygame.font.SysFont('CollegiateBorderFLF.ttf', size = 32)

num_toilet_paper = 0
num_toilet_paper_label_size = 25

def draw_toilet_paper(num):
    width = 26
    space = 10
    start_x = SCREEN_WIDTH/2 - width *2.5 - space * 2
    y = SCREEN_HEIGHT - 30
    r = width/2
    for i in range(0,5):
        x = start_x + (26 + 10)*i
        pygame.draw.line(screen,(128,128,128), (x-r,y-r),(x+r,y-r),2)
        pygame.draw.line(screen, (128,128,128), (x-r,y-r),(x-r, y+r),2)
        pygame.draw.line(screen, (128,128,128), (x+r,y-r), (x+r,y+r),2)
        pygame.draw.line(screen, (128,128,128), (x-r,y+r), (x+r,y+r),2)

    toilet_paper_icon = pygame.image.load("toiletpaper.png").convert()
    toilet_paper_icon.set_colorkey(BLACK, RLEACCEL)
    toilet_paper_icon = pygame.transform.scale(toilet_paper_icon, (width, width))
    if num > 0:
        for j in range(0,num):
            toilet_paper_icon_copy = toilet_paper_icon.copy()
            x = start_x + (26 + 10)*j
            screen.blit(toilet_paper_icon_copy, toilet_paper_icon_copy.get_rect(center=(x, y)))

def init():
    #screen.fill(BACKGROUND_COLOR)
    maxie = Maxie(mouse_x, mouse_y, 50)
    random_tick = None
    score = 0
    blue_hit = 1
    poop_speed = 0.1
    black_hole_pos = (random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)
    toilet_bowl_rotated = pygame.transform.rotate(toilet_bowl.copy(), random.randint(0, 360))

    return(maxie, random_tick, score, blue_hit, poop_speed, black_hole_pos, toilet_bowl_rotated)

def test_collision(maxie, poop):
    if (maxie.x - poop.x)**2 + (maxie.y - poop.y)**2 < (((maxie.r/2) + (poop.r)))**2:
        return True
    else:
        return False

while running:

    current_time = pygame.time.get_ticks()

    if random_tick is None:
        if 80 - blue_hit * 5 < 10:
            low = 10
        else:
            low = 80 - blue_hit * 5
        if 300 - blue_hit * 10 < 100:
            high = 100
        else:
            high = 300 - blue_hit * 10
        random_tick = current_time + random.randint(low,high)

    if random_tick < current_time:
        spawn_x, spawn_y = spawn_positions[random.randint(0, len(spawn_positions)-1)]
        dice = random.randint(1,50)
        if dice == 7:
            poops.add(Poop(spawn_x, spawn_y, color=(0,0,255),r=30))
        elif any([dice == 8, dice==16]):
            poops.add(Poop(spawn_x, spawn_y, color=(128, 128,128),r=35))
        else:
            poops.add(Poop(spawn_x, spawn_y, r=40))
        random_tick = None

    screen.fill(BACKGROUND_COLOR)
    screen.blit(toilet_bowl_rotated, toilet_bowl_rotated.get_rect(center=black_hole_pos))

    #pygame.mouse.set_visible(False) # set mouse as invisible

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            with open('high_score.txt', 'w') as f:
                f.write(str(hi_score))

        if event.type == MOUSEBUTTONDOWN:
            if num_toilet_paper > 0:
                num_toilet_paper -= 1
                score += len(poops) * blue_hit + 100 * blue_hit
                poops.empty()

        if event.type == MOUSEMOTION:
            mouse_off = False
            if not mouse_off:
                mouse_x, mouse_y = event.pos
                if 0 < mouse_x < SCREEN_WIDTH and 0 < mouse_y < SCREEN_HEIGHT:
                    mouse_dx, mouse_dy = event.rel
                    if abs(mouse_dx + mouse_dy) > 0:
                        sign = (mouse_dx + mouse_dy) / abs(mouse_dx + mouse_dy)
                    else:
                        sign = 1
                    mouse_v = (mouse_dx**2 + mouse_dy**2)**(1/2) * sign * 0.5
                else:
                    mouse_v = 0

    # mouse position is available globally
    # as long as there is a distance between mouse and maxie
    # the maxie will be drawn slowly toward the cursor
    new_maxie_x = maxie.x + (mouse_x - maxie.x) * 0.02
    new_maxie_y = maxie.y + (mouse_y - maxie.y) * 0.02

    # move movement boundaries
    if new_maxie_x <= maxie.r:
        new_maxie_x = maxie.r
    elif new_maxie_x >= SCREEN_WIDTH - maxie.r:
        new_maxie_x = SCREEN_WIDTH - maxie.r
    if new_maxie_y <= maxie.r + 30:
        new_maxie_y = maxie.r + 30
    elif new_maxie_y >= SCREEN_HEIGHT - maxie.r:
        new_maxie_y = SCREEN_HEIGHT - maxie.r

    maxie.update(new_maxie_x, new_maxie_y, mouse_v)

    screen.blit(maxie.rotated_surf, maxie.rect) # draw maxie first so that we can test poop over the white maxie

    for poop in poops:
        score += poop.move(black_hole_pos, poop_speed) * blue_hit # move poop toward centre of screen
        if poop.move(black_hole_pos, poop_speed) * blue_hit >=1:
            poop.move(black_hole_pos, poop_speed) * blue_hit
        pull = poop_speed * blue_hit * 0.1
        poop.move((maxie.x, maxie.y), pull) # move poop toward maxie
        # poop.move((mouse_x, mouse_y), 2)

    poops.update()

    hit_poop = pygame.sprite.spritecollideany(maxie, poops)

    # score
    with open('high_score.txt') as f:
        hi_score = int(f.readline())

    if score > hi_score:
        hi_score = score

    if hit_poop and test_collision(maxie, hit_poop):
        if hit_poop.color == (0, 0, 255):
            print("collided")
            score += len(poops) + (100 * blue_hit)
            blue_hit += 1
            poop_speed *= 1.1
            hit_poop.kill()
            black_hole_pos = (random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)

        if hit_poop.color == (128,128,128):
            print("got toilet paper")
            if num_toilet_paper < 5:
                num_toilet_paper += 1
            hit_poop.kill()

        elif screen.get_at((int(round(hit_poop.x,0)), int(round(hit_poop.y,0)))) != BACKGROUND_COLOR:
            with open('high_score.txt', 'w') as f:
                f.write(str(hi_score))
            poops.empty()
            num_toilet_paper = 0
            maxie, random_tick, score, blue_hit, poop_speed, black_hole_pos, toilet_bowl_rotated = init()

    for poop in poops:
        screen.blit(poop.rotated_surf, poop.rect)

    score_label = font.render("Score: " + str(score), False, (255,0,0))
    screen.blit(score_label, score_label.get_rect(topright = (SCREEN_WIDTH -10, 10)))

    hi_score_label = font.render("Hi Score: " + str(hi_score), False, (255, 0, 0))
    screen.blit(hi_score_label, hi_score_label.get_rect(topleft = (10, 10)))

    blue_hit_label = font.render("Banana Multi X " + str(blue_hit), False, (255, 255, 110))
    screen.blit(blue_hit_label, blue_hit_label.get_rect(center = (SCREEN_WIDTH/2, 10 + blue_hit_label.get_size()[1]/2)))

    draw_toilet_paper(num_toilet_paper)

    pygame.display.flip()
