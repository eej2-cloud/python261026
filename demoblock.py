import math
import random

import pygame


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

PLAY_AREA = pygame.Rect(40, 100, 880, 500)
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_GAP = 8
BRICK_HEIGHT = 25
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 14
BALL_RADIUS = 9

BACKGROUND = (12, 17, 34)
PLAY_AREA_COLOR = (19, 27, 49)
WHITE = (238, 243, 255)
MUTED = (150, 164, 194)
BRICK_COLORS = [
    (255, 91, 110),
    (255, 151, 77),
    (255, 207, 87),
    (76, 207, 160),
    (89, 160, 255),
]


class BreakoutGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("블럭깨기")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 42)
        self.font = pygame.font.Font(None, 27)
        self.small_font = pygame.font.Font(None, 20)
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.state = "ready"
        self.paddle = pygame.Rect(
            SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
            PLAY_AREA.bottom - 34,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )
        self.create_bricks()
        self.attach_ball()

    def create_bricks(self):
        brick_width = (
            PLAY_AREA.width - (BRICK_COLUMNS - 1) * BRICK_GAP
        ) // BRICK_COLUMNS
        self.bricks = []
        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):
                x = PLAY_AREA.left + column * (brick_width + BRICK_GAP)
                y = PLAY_AREA.top + 18 + row * (BRICK_HEIGHT + BRICK_GAP)
                self.bricks.append(
                    (pygame.Rect(x, y, brick_width, BRICK_HEIGHT), BRICK_COLORS[row])
                )

    def attach_ball(self):
        self.ball_x = float(self.paddle.centerx)
        self.ball_y = float(self.paddle.top - BALL_RADIUS - 2)
        self.ball_vx = 0.0
        self.ball_vy = 0.0

    def launch_ball(self):
        speed = 340 + (self.level - 1) * 25
        angle = random.uniform(-0.65, 0.65)
        self.ball_vx = speed * math.sin(angle)
        self.ball_vy = -speed * math.cos(angle)
        self.state = "playing"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_SPACE:
                if self.state == "ready":
                    self.launch_ball()
                elif self.state == "playing":
                    self.state = "paused"
                elif self.state == "paused":
                    self.state = "playing"
        return True

    def move_paddle(self, dt):
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.paddle.x += round(direction * 540 * dt)
        self.paddle.clamp_ip(PLAY_AREA)

        if self.state == "ready":
            self.attach_ball()

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = "game_over"
        else:
            self.attach_ball()
            self.state = "ready"

    def advance_level(self):
        self.level += 1
        self.create_bricks()
        self.attach_ball()
        self.state = "ready"

    def hit_brick(self, previous_x, previous_y):
        ball_rect = pygame.Rect(
            round(self.ball_x - BALL_RADIUS),
            round(self.ball_y - BALL_RADIUS),
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )
        for index, (brick, color) in enumerate(self.bricks):
            if not ball_rect.colliderect(brick):
                continue

            self.bricks.pop(index)
            self.score += 10 + (BRICK_ROWS - 1 - index // BRICK_COLUMNS) * 2
            if previous_y + BALL_RADIUS <= brick.top or previous_y - BALL_RADIUS >= brick.bottom:
                self.ball_vy *= -1
            elif previous_x + BALL_RADIUS <= brick.left or previous_x - BALL_RADIUS >= brick.right:
                self.ball_vx *= -1
            else:
                self.ball_vy *= -1

            if not self.bricks:
                self.advance_level()
            return

    def update_ball(self, dt):
        previous_x = self.ball_x
        previous_y = self.ball_y
        self.ball_x += self.ball_vx * dt
        self.ball_y += self.ball_vy * dt

        if self.ball_x - BALL_RADIUS <= PLAY_AREA.left:
            self.ball_x = PLAY_AREA.left + BALL_RADIUS
            self.ball_vx = abs(self.ball_vx)
        elif self.ball_x + BALL_RADIUS >= PLAY_AREA.right:
            self.ball_x = PLAY_AREA.right - BALL_RADIUS
            self.ball_vx = -abs(self.ball_vx)

        if self.ball_y - BALL_RADIUS <= PLAY_AREA.top:
            self.ball_y = PLAY_AREA.top + BALL_RADIUS
            self.ball_vy = abs(self.ball_vy)

        ball_rect = pygame.Rect(
            round(self.ball_x - BALL_RADIUS),
            round(self.ball_y - BALL_RADIUS),
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )
        if self.ball_vy > 0 and ball_rect.colliderect(self.paddle):
            offset = (self.ball_x - self.paddle.centerx) / (self.paddle.width / 2)
            self.ball_vx = offset * 390
            self.ball_vy = -max(230, math.sqrt(max(0, 390**2 - self.ball_vx**2)))
            self.ball_y = self.paddle.top - BALL_RADIUS

        self.hit_brick(previous_x, previous_y)
        if self.ball_y - BALL_RADIUS > PLAY_AREA.bottom:
            self.lose_life()

    def update(self, dt):
        self.move_paddle(dt)
        if self.state == "playing":
            self.update_ball(dt)

    def draw_text(self, text, font, color, center):
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_text("BLOCK BREAKER", self.title_font, WHITE, (SCREEN_WIDTH // 2, 39))
        self.draw_text(f"점수  {self.score}", self.font, WHITE, (150, 75))
        self.draw_text(f"레벨  {self.level}", self.font, WHITE, (SCREEN_WIDTH // 2, 75))
        self.draw_text(f"목숨  {'♥ ' * self.lives}", self.font, (255, 111, 130), (810, 75))

        pygame.draw.rect(self.screen, PLAY_AREA_COLOR, PLAY_AREA, border_radius=14)
        pygame.draw.rect(self.screen, (48, 62, 94), PLAY_AREA, width=2, border_radius=14)

        for brick, color in self.bricks:
            pygame.draw.rect(self.screen, color, brick, border_radius=6)
            shine = pygame.Rect(brick.left + 5, brick.top + 4, brick.width - 10, 3)
            pygame.draw.rect(self.screen, (255, 255, 255, 90), shine, border_radius=2)

        pygame.draw.rect(self.screen, (113, 184, 255), self.paddle, border_radius=7)
        pygame.draw.circle(
            self.screen, WHITE, (round(self.ball_x), round(self.ball_y)), BALL_RADIUS
        )

        if self.state == "ready":
            message = "SPACE를 눌러 시작"
        elif self.state == "paused":
            message = "일시 정지  ·  SPACE로 계속"
        elif self.state == "game_over":
            message = "게임 오버  ·  R을 눌러 다시 시작"
        else:
            message = ""

        if message:
            self.draw_text(message, self.font, WHITE, (SCREEN_WIDTH // 2, 390))

        self.draw_text(
            "이동: ← → 또는 A / D     시작·일시정지: SPACE     재시작: R     종료: ESC",
            self.small_font,
            MUTED,
            (SCREEN_WIDTH // 2, 620),
        )
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000, 0.03)
            for event in pygame.event.get():
                running = self.handle_event(event) and running
            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    BreakoutGame().run()
