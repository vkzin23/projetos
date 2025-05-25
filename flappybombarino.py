import pygame
import random
import sys
from pygame import image






pygame.init()


WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("bombardino crocodillo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = (139, 69, 19)  # marrom


#Variáveis do jogo
GRAVITY = 0.5
CROC_JUMP = -8
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

FONT = pygame.font.SysFont("Arial", 60)

def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(SCREEN, color, (x, y, w, h))
    btn_font = pygame.font.Font("assets/FlappybirdyRegular-KaBW.ttf", 60)
    txt = btn_font.render(text, True, text_color)
    SCREEN.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))


# imagem do BOMBARDINO CROCODILLO
CROC_IMG = pygame.image.load("assets/croc.png").convert_alpha()
CROC_IMG = pygame.transform.scale(CROC_IMG, (40, 40))  # Ajuste de tamanho do background

# decarando a imagem de fundo
BG_IMG = pygame.image.load("assets/bg.png").convert()
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

# efeito sonoro de pontuação
POINT_SOUND = pygame.mixer.Sound("assets/Everything/sfx_point.wav")
POINT_SOUND.set_volume(0.2) 


class Croc:
    waiting = True
    while waiting:
        SCREEN.blit(BG_IMG, (0, 0))
        draw_button("Iniciar", WIDTH//2 - 75, HEIGHT//2 - 30, 150, 60, (0, 128, 0), BLACK)
        title_font = pygame.font.Font("assets/FlappybirdyRegular-KaBW.ttf", 60)
        title = title_font.render("BORBARDINO COCRODILLO", True, BLACK, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3 - 100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH//2 - 75 < mx < WIDTH//2 + 75 and HEIGHT//2 - 30 < my < HEIGHT//2 + 30:
                    waiting = False
    
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.radius = 20
        self.vel = 0

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def jump(self):
        self.vel = CROC_JUMP

    def draw(self):
        SCREEN.blit(CROC_IMG, (int(self.x - 20), int(self.y - 20)))  # Centraliza a imagem

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Top pipe
        pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

def show_game_over_screen(score):
    waiting = True
    while waiting:
        SCREEN.blit(BG_IMG, (0, 0))
        #Game Over
        game_over_font = pygame.font.Font("assets/FlappybirdyRegular-KaBW.ttf", 60)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        SCREEN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))

        # pontuação final
        score_font = pygame.font.SysFont("Arial", 30)
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))

        # Botão de Restart
        draw_button("Restart", WIDTH//2 - 75, HEIGHT//2 + 50, 150, 60, (0, 128, 0), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH//2 - 75 < mx < WIDTH//2 + 75 and HEIGHT//2 + 50 < my < HEIGHT//2 + 110:
                    waiting = False  # Sai do loop e reinicia o jogo
                    main()  # Reinicia o jogo

def main():
    clock = pygame.time.Clock()
    croc = Croc()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    running = True

    while running:
        clock.tick(60)
        # Desenhe o fundo
        SCREEN.blit(BG_IMG, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                croc.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                croc.jump()

        # croc update
        croc.update()
        croc.draw()

        # Pipes update
        remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.update()
            pipe.draw()
            # Collision
            if croc.get_rect().colliderect(pipe.get_top_rect()) or croc.get_rect().colliderect(pipe.get_bottom_rect()):
                running = False
            # Score
            if not pipe.passed and pipe.x + PIPE_WIDTH < croc.x:
                pipe.passed = True
                score += 1
                add_pipe = True
                POINT_SOUND.play()  # Toca o som ao pontuar
            # Remove os canos que saem da tela
            if pipe.x + PIPE_WIDTH < 0:
                remove.append(pipe)
        for r in remove:
            pipes.remove(r)
        if add_pipe:
            pipes.append(Pipe(WIDTH + 50))

    
        if croc.y - croc.radius < 0 or croc.y + croc.radius > HEIGHT:
            running = False # Croc cai fora da tela

        # PONTUAÇÃO
        score_text = FONT.render(str(score), True, BLACK)
        SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        pygame.display.flip()

    # Game over
    show_game_over_screen(score)

if __name__ == "__main__":
    main()