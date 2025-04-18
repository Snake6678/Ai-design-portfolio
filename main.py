import pygame
import math

# ——— Constants ——————————————————————————————————————————————————————————————————
SCREEN_SIZE = WIDTH, HEIGHT = 800, 600
BG_COLOR     = (30, 30, 30)
PLAYER_COLOR = (50, 200, 50)
GUARD_COLOR  = (200, 50, 50)
FPS          = 60

# Vision cone parameters
VISION_ANGLE = math.radians(60)    # 60° cone
VISION_DIST  = 200                 # pixels

# Patrol waypoints
POINT_A = (100, 300)
POINT_B = (700, 300)

# ——— Helper functions —————————————————————————————————————————————————————————————
def vec_from_to(a, b):
    return (b[0]-a[0], b[1]-a[1])

def length(vec):
    return math.hypot(vec[0], vec[1])

def normalize(vec):
    l = length(vec)
    return (vec[0]/l, vec[1]/l) if l else (0,0)

def angle_between(v1, v2):
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    return math.acos(dot / (length(v1)*length(v2) + 1e-6))

# ——— Guard (Enemy) Class —————————————————————————————————————————————————————————————
class Guard:
    def __init__(self):
        self.pos       = list(POINT_A)
        self.speed     = 2.0
        self.waypoint  = POINT_B
        self.state     = 'patrol'  # other state: 'alert'

    def update(self, player_pos):
        if self.state == 'patrol':
            self.patrol()
            if self.can_see(player_pos):
                self.state = 'alert'
        elif self.state == 'alert':
            self.chase(player_pos)

    def patrol(self):
        # Move toward current waypoint
        dir = vec_from_to(self.pos, self.waypoint)
        nd  = normalize(dir)
        self.pos[0] += nd[0]*self.speed
        self.pos[1] += nd[1]*self.speed
        # Switch waypoint if reached
        if length(dir) < 5:
            self.waypoint = POINT_A if self.waypoint==POINT_B else POINT_B

    def chase(self, target):
        dir = vec_from_to(self.pos, target)
        nd  = normalize(dir)
        self.pos[0] += nd[0]*self.speed * 1.2
        self.pos[1] += nd[1]*self.speed * 1.2

    def can_see(self, target):
        # Distance check
        dir    = vec_from_to(self.pos, target)
        dist   = length(dir)
        if dist > VISION_DIST:
            return False
        # Angle check against facing vector (toward waypoint)
        facing = normalize(vec_from_to(self.pos, self.waypoint))
        to_target = normalize(dir)
        return angle_between(facing, to_target) < (VISION_ANGLE/2)

    def draw(self, screen):
        # draw guard
        pygame.draw.rect(screen, GUARD_COLOR, (*self.pos, 20, 20))
        # draw vision cone (for debug)
        facing = normalize(vec_from_to(self.pos, self.waypoint))
        base_angle = math.atan2(facing[1], facing[0])
        for sign in (-1,1):
            end = (
                self.pos[0] + math.cos(base_angle + sign*(VISION_ANGLE/2))*VISION_DIST,
                self.pos[1] + math.sin(base_angle + sign*(VISION_ANGLE/2))*VISION_DIST
            )
            pygame.draw.line(screen, (100,100,100), self.pos, end, 1)

# ——— Main Loop ————————————————————————————————————————————————————————————————————
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock  = pygame.time.Clock()

    player = [400, 500]
    guard  = Guard()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Move player with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player[0] -= 4
        if keys[pygame.K_RIGHT]:
            player[0] += 4
        if keys[pygame.K_UP]:
            player[1] -= 4
        if keys[pygame.K_DOWN]:
            player[1] += 4

        # Update guard AI
        guard.update(player)

        # Draw
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, (*player, 20, 20))
        guard.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
