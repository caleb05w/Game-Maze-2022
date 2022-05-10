#Maze Game

import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Maze Game"

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    def __init__(self, x, y):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/runner.png.webp")
        # Scale
        self.image = pygame.transform.scale(self.image, (38, 38))
        # self.image.set_colorkey((WHITE))    # set transparency

        # RECT the hitbox
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    # Movement
    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 1"""

    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [
            [0, 0, 20, 250, WHITE],
            [0, 350, 20, 250, WHITE],
            [780, 0, 20, 250, WHITE],
            [780, 350, 20, 250, WHITE],
            [20, 0, 760, 20, WHITE],
            [20, 580, 760, 20, WHITE],
            [390, 50, 20, 500, BLUE]
         ]

        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# class Room2(Room):
#     """This creates all the walls in room 2"""
#
#     def __init__(self):
#         super().__init__()
#
#         walls = [[0, 0, 20, 250, RED],
#                  [0, 350, 20, 250, RED],
#                  [780, 0, 20, 250, RED],
#                  [780, 350, 20, 250, RED],
#                  [20, 0, 760, 20, RED],
#                  [20, 580, 760, 20, RED],
#                  [190, 50, 20, 500, GREEN],
#                  [590, 50, 20, 500, GREEN]
#                  ]
#
#         for item in walls:
#             wall = Wall(item[0], item[1], item[2], item[3], item[4])
#             self.wall_list.add(wall)

#
# class Room3(Room):
#     """This creates all the walls in room 3"""
#
#     def __init__(self):
#         super().__init__()
#
#         walls = [[0, 0, 20, 250, PURPLE],
#                  [0, 350, 20, 250, PURPLE],
#                  [780, 0, 20, 250, PURPLE],
#                  [780, 350, 20, 250, PURPLE],
#                  [20, 0, 760, 20, PURPLE],
#                  [20, 580, 760, 20, PURPLE]
#                  ]
#
#         for item in walls:
#             wall = Wall(item[0], item[1], item[2], item[3], item[4])
#             self.wall_list.add(wall)
#
#         for x in range(100, 800, 100):
#             for y in range(50, 451, 300):
#                 wall = Wall(x, y, 20, 200, RED)
#                 self.wall_list.add(wall)
#
#         for x in range(150, 700, 100):
#             wall = Wall(x, 200, 20, 200, WHITE)
#             self.wall_list.add(wall)

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites_group = pygame.sprite.Group()

    # player.level = current_level

    # Create sprites to fill the groups
    player = Player(50, 50)
    all_sprites_group.add(player)

    # Create Rooms in Room List
    rooms = [Room1()]

    current_room_no = 0
    current_room = rooms[current_room_no]

    # ----- MAIN LOOP
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        # Update the player.
        player.move(current_room.wall_list)


        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC

        # ----- RENDER
        screen.fill(BLACK)
        current_room.wall_list.draw(screen)
        all_sprites_group.draw(screen)


        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()