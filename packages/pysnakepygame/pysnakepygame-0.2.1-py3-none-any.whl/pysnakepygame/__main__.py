import pygame as pyg
import random
import itertools as it
WINDOW_SIZE = 500
from copy import deepcopy

class Snake():
    SIZE = 10
    SPEED = 5

    class BodyPart():
        def __init__(self, rect, velocity):
            self.rect = rect
            self.velocity = velocity 

    def __init__(self):
        self.body = []
        self.head = None
        self.apple = pyg.Rect(0, 0, Snake.SIZE, Snake.SIZE)
        self.reset()

    def extend(self):
        tail = self.body[-1]
        self.body.append(Snake.BodyPart(pyg.Rect(tail.rect.left - int(tail.velocity.x)*Snake.SIZE, \
            tail.rect.top - int(tail.velocity.y)*Snake.SIZE,\
             Snake.SIZE, Snake.SIZE), tail.velocity))
        pyg.display.set_caption("Snake | {}".format(len(self.body)))


    def get_rects(self):
        rects = []
        for part in self.body:
            rects.append(part.rect)

        return rects
    def move(self):
        #print(self.get_rects())
        for index, part in reversed(list(enumerate(self.body))):
            part.rect.left += Snake.SIZE*int(part.velocity.x)
            part.rect.top  += Snake.SIZE*int(part.velocity.y)
            if index != 0:
                part.velocity = self.body[index - 1].velocity
        #print(self.get_rects())

    def check_collisions(self):
        head = self.head.rect
        if head.left <= 0 or head.top <= 0 or head.left + Snake.SIZE >= WINDOW_SIZE or head.top + Snake.SIZE >= WINDOW_SIZE:
            return True
        for index, a in enumerate(self.body):
            for b in self.body[index + 1:len(self.body) - 1]:
                if a.rect.colliderect(b.rect):
                    return True
        return False

    def check_keys(self):
        if pyg.key.get_pressed()[pyg.K_UP] and (self.head.velocity != pyg.math.Vector2(0, 1) or len(self.body) == 1):
            self.head.velocity = pyg.math.Vector2(0, -1)
        elif pyg.key.get_pressed()[pyg.K_DOWN] and (self.head.velocity != pyg.math.Vector2(0, -1) or len(self.body) == 1):
            self.head.velocity = pyg.math.Vector2(0, 1)
        elif pyg.key.get_pressed()[pyg.K_LEFT] and (self.head.velocity != pyg.math.Vector2(1, 0) or len(self.body) == 1):
            self.head.velocity = pyg.math.Vector2(-1, 0)
        elif pyg.key.get_pressed()[pyg.K_RIGHT] and (self.head.velocity != pyg.math.Vector2(-1, 0) or len(self.body) == 1):
            self.head.velocity = pyg.math.Vector2(1, 0)

    def draw(self):
        screen = pyg.display.get_surface()
        rect_list = []
        for part in self.body:
            pyg.draw.rect(screen, (0, 255, 50), part.rect)
            rect_list.append(part.rect)
        pyg.draw.rect(screen, (255, 0, 0), self.apple)
        rect_list.append(self.apple)

        return rect_list

    def update(self):
        self.check_keys()
        if self.check_collisions():
            self.reset()
        else:
            self.move()
        if self.head.rect.colliderect(self.apple):
            self.extend()
            self.move_apple()

    def reset(self):
        self.body = [Snake.BodyPart(pyg.Rect(Snake.SIZE*random.randint(0, WINDOW_SIZE/Snake.SIZE - 1), Snake.SIZE*random.randint(0, WINDOW_SIZE/Snake.SIZE - 1), Snake.SIZE, Snake.SIZE), \
             pyg.math.Vector2(0, 0))] 
        self.head = self.body[0]
        self.move_apple()
        pyg.display.set_caption("Snake | 1")

    def move_apple(self):
        empty = [(x, y) for x, y in \
            it.product(\
                range(Snake.SIZE, WINDOW_SIZE-Snake.SIZE, Snake.SIZE), \
                range(Snake.SIZE, WINDOW_SIZE-Snake.SIZE, Snake.SIZE))]
        for part in self.body:
            try:
                empty.remove((part.rect.left, part.rect.top))
            except ValueError:
                pass
        self.apple.left, self.apple.top = random.choice(empty)

def main():
    pyg.init()
    screen = pyg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pyg.display.set_caption("Snake | 1")

    snecc = Snake()

    game_clock = pyg.time.Clock()

    last_rects = []
    pyg.display.flip()

    running = True
    while running:
        game_clock.tick(20)

        for event in pyg.event.get():
            if event.type == pyg.QUIT or pyg.key.get_pressed()[pyg.K_ESCAPE]:
                running = False
                break

        screen.fill((0,0,0))

        snecc.update()
        
        rects = snecc.draw()
        pyg.display.update(rects)
        pyg.display.update(last_rects)
        last_rects = deepcopy(rects)
    pyg.quit()

if __name__ == "__main__":
    main()