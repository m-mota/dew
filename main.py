# -*- coding: utf-8 -*-
import pygame
import random
import math
import sys

# =========================
# COSMIC HEAT DELUXE FINAL
# Controls:
# Arrows or WASD = move
# Space = shoot
# P = pause
# R = restart on game over
# ESC = exit
# =========================

pygame.init()

LARGURA = 900
ALTURA = 650
FPS = 60

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cosmic Heat Deluxe  - Final")
RELOGIO = pygame.time.Clock()

# Paleta
BRANCO      = (255, 255, 255)
PRETO       = (5, 8, 18)
AZUL_NEON   = (0, 220, 255)
AZUL_CLARO  = (120, 220, 255)
AZUL        = (60, 160, 255)
ROSA_CHOQUE = (255, 0, 255)
AMARELO     = (255, 210, 80)
VERMELHO    = (255, 60, 60)
VERDE_LIMA  = (80, 255, 150)
VERDE       = (80, 255, 150)
ROXO        = (170, 90, 255)
LARANJA     = (255, 140, 60)
CINZA       = (120, 130, 150)

fonte_tiny   = pygame.font.SysFont("arial", 18)
fonte_pequena = pygame.font.SysFont("arial", 24)
fonte_media  = pygame.font.SysFont("arial", 36, bold=True)
fonte_grande = pygame.font.SysFont("arial", 62, bold=True)


#                                          
# UTILIT RIOS
#                                          

def texto(msg, fonte, cor, x, y, centro=True):
    img = fonte.render(msg, True, cor)
    rect = img.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    TELA.blit(img, rect)


def barra(x, y, atual, maximo, largura, cor_fill, cor_fundo=(50, 50, 50)):
    atual = max(0, atual)
    pygame.draw.rect(TELA, cor_fundo, (x, y, largura, 16), border_radius=6)
    if maximo > 0:
        fill = int(largura * atual / maximo)
        if fill > 0:
            pygame.draw.rect(TELA, cor_fill, (x, y, fill, 16), border_radius=6)
    pygame.draw.rect(TELA, BRANCO, (x, y, largura, 16), 2, border_radius=6)


def criar_estrelas(qtd=100):
    return [[random.randint(0, LARGURA), random.randint(0, ALTURA), random.randint(1, 3)] for _ in range(qtd)]


def desenhar_fundo(estrelas):
    TELA.fill(PRETO)
    for e in estrelas:
        pygame.draw.circle(TELA, BRANCO, (e[0], e[1]), e[2])
        e[1] += e[2]
        if e[1] > ALTURA:
            e[0] = random.randint(0, LARGURA)
            e[1] = 0


#                                          
# SISTEMA DE PART CULAS
#                                          

class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y, cor):
        super().__init__()
        tamanho = random.randint(3, 7)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        pygame.draw.circle(self.image, cor, (tamanho // 2, tamanho // 2), tamanho // 2)
        self.rect = self.image.get_rect(center=(x, y))
        speed = random.uniform(1.5, 5)
        angle = random.uniform(0, math.pi * 2)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.vida = 255

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 0.15   # leve gravidade
        self.vida -= 12
        if self.vida <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.vida)


def criar_explosao(x, y, cor, grupo_particulas, todos, qtd=18):
    for _ in range(qtd):
        p = Particula(x, y, cor)
        grupo_particulas.add(p)
        todos.add(p)


#                                          
# CLASSES DE SPRITES
#                                          

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((56, 64), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, AZUL_CLARO, [(28, 0), (0, 62), (28, 48), (56, 62)])
        pygame.draw.polygon(self.image, AZUL,       [(28, 10), (12, 55), (28, 45), (44, 55)])
        pygame.draw.circle(self.image, BRANCO, (28, 28), 7)
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA - 80))
        self.vel = 7
        self.vida = 100
        self.vida_max = 100
        self.escudo = 0          # escudo absorve dano antes da vida
        self.tiros = 150
        self.ultimo_tiro = 0
        self.delay_tiro = 160
        self.powerup_triplo = 0  # frames restantes de tiro triplo
        self.invencivel = 0      # frames de invencibilidade apos levar dano

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]: self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: self.rect.x += self.vel
        if teclas[pygame.K_UP]    or teclas[pygame.K_w]: self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]: self.rect.y += self.vel

        self.rect.left   = max(0, self.rect.left)
        self.rect.right  = min(LARGURA, self.rect.right)
        self.rect.top    = max(0, self.rect.top)
        self.rect.bottom = min(ALTURA, self.rect.bottom)

        if self.powerup_triplo > 0: self.powerup_triplo -= 1
        if self.invencivel > 0:     self.invencivel -= 1

        # pisca quando invencivel
        if self.invencivel > 0 and (self.invencivel // 5) % 2 == 0:
            self.image.set_alpha(80)
        else:
            self.image.set_alpha(255)

    def levar_dano(self, dano):
        if self.invencivel > 0:
            return False
        if self.escudo > 0:
            self.escudo = max(0, self.escudo - dano)
        else:
            self.vida -= dano
        self.invencivel = 40
        return True

    def atirar(self, grupo_tiros, todos):
        agora = pygame.time.get_ticks()
        if self.tiros > 0 and agora - self.ultimo_tiro > self.delay_tiro:
            self.ultimo_tiro = agora
            if self.powerup_triplo > 0:
                for angulo in [-0.2, 0, 0.2]:
                    t = Tiro(self.rect.centerx, self.rect.top, angulo)
                    grupo_tiros.add(t); todos.add(t)
            else:
                t = Tiro(self.rect.centerx, self.rect.top)
                grupo_tiros.add(t); todos.add(t)
            self.tiros -= 1


class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo=0, cor=AMARELO, vel_y=-12):
        super().__init__()
        self.image = pygame.Surface((8, 22), pygame.SRCALPHA)
        pygame.draw.rect(self.image, cor, (2, 0, 4, 22), border_radius=4)
        pygame.draw.circle(self.image, BRANCO, (4, 3), 4)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = vel_y
        self.vel_x = angulo * 10

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.bottom < 0 or self.rect.top > ALTURA:
            self.kill()


class TiroInimigo(pygame.sprite.Sprite):
    """Projetil disparado por inimigos / boss."""
    def __init__(self, x, y, alvo_x, alvo_y, vel=5):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, VERMELHO, (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        dx = alvo_x - x
        dy = alvo_y - y
        dist = max(1, math.hypot(dx, dy))
        self.vel_x = vel * dx / dist
        self.vel_y = vel * dy / dist

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.top > ALTURA or self.rect.bottom < 0
                or self.rect.left > LARGURA or self.rect.right < 0):
            self.kill()


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, nivel=1):
        super().__init__()
        tamanho = random.randint(34, 52)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        self.cor = random.choice([ROSA_CHOQUE, VERMELHO, LARANJA, ROXO])
        pygame.draw.polygon(self.image, self.cor,
                            [(tamanho // 2, tamanho), (0, 8), (tamanho // 2, 18), (tamanho, 8)])
        pygame.draw.circle(self.image, BRANCO, (tamanho // 2, tamanho // 2), 5)
        self.rect = self.image.get_rect(center=(random.randint(40, LARGURA - 40), -40))
        self.vel_y = random.uniform(2 + nivel * 0.4, 5 + nivel * 0.5)
        self.vel_x = random.choice([-2, -1, 0, 1, 2])
        self.vida = 1 + nivel // 3
        self.vida_max = self.vida
        # atirador ocasional
        self.pode_atirar = random.random() < 0.25
        self.ultimo_tiro_ini = 0

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.left < 0 or self.rect.right > LARGURA:
            self.vel_x *= -1
        if self.rect.top > ALTURA:
            self.kill()

    def tentar_atirar(self, jogador, grupo_ti, todos):
        agora = pygame.time.get_ticks()
        if self.pode_atirar and agora - self.ultimo_tiro_ini > 2500:
            self.ultimo_tiro_ini = agora
            t = TiroInimigo(self.rect.centerx, self.rect.bottom,
                            jogador.rect.centerx, jogador.rect.centery)
            grupo_ti.add(t); todos.add(t)


class Meteoro(pygame.sprite.Sprite):
    def __init__(self, nivel=1):
        super().__init__()
        tamanho = random.randint(28, 70)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CINZA,     (tamanho // 2, tamanho // 2), tamanho // 2)
        pygame.draw.circle(self.image, (80, 85, 95),  (tamanho // 3, tamanho // 3), tamanho // 7)
        pygame.draw.circle(self.image, (70, 75, 85),  (tamanho * 2 // 3, tamanho // 2), tamanho // 8)
        self.rect = self.image.get_rect(center=(random.randint(30, LARGURA - 30), -50))
        self.vel_y = random.randint(3, 6 + nivel)
        self.vel_x = random.choice([-1, 0, 1])
        self.vida = 2 + nivel // 2
        self.vida_max = self.vida

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.top > ALTURA:
            self.kill()


class Boss(pygame.sprite.Sprite):
    FASE_PADRAO = 0
    FASE_RAIVA  = 1   # ativado abaixo de 40% de vida

    def __init__(self, nivel=1):
        super().__init__()
        self.image = pygame.Surface((180, 100), pygame.SRCALPHA)
        self._desenhar()
        self.rect = self.image.get_rect(center=(LARGURA // 2, 90))
        self.vida = 60 + nivel * 20
        self.vida_max = self.vida
        self.vel_x = 3 + nivel * 0.5
        self.fase = self.FASE_PADRAO
        self.ultimo_tiro_boss = 0
        self.angulo_tiro = 0

    def _desenhar(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, ROXO,    (0, 15, 180, 70))
        pygame.draw.ellipse(self.image, (100, 40, 180), (20, 25, 140, 50))
        pygame.draw.rect(self.image, VERMELHO,   (40, 40, 100, 22), border_radius=8)
        pygame.draw.circle(self.image, AMARELO, (65, 50), 9)
        pygame.draw.circle(self.image, AMARELO, (115, 50), 9)
        pygame.draw.circle(self.image, BRANCO,  (65, 50), 5)
        pygame.draw.circle(self.image, BRANCO,  (115, 50), 5)
        # propulsores
        pygame.draw.rect(self.image, AZUL_NEON, (10, 75, 30, 12), border_radius=4)
        pygame.draw.rect(self.image, AZUL_NEON, (140, 75, 30, 12), border_radius=4)

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.left < 0 or self.rect.right > LARGURA:
            self.vel_x *= -1

        # entra em "raiva" com menos de 40% de vida
        if self.vida < self.vida_max * 0.4 and self.fase == self.FASE_PADRAO:
            self.fase = self.FASE_RAIVA
            self.vel_x = (abs(self.vel_x) + 2) * (1 if self.vel_x > 0 else -1)

    def atirar(self, jogador, grupo_ti, todos):
        agora = pygame.time.get_ticks()
        delay = 1000 if self.fase == self.FASE_RAIVA else 1800
        if agora - self.ultimo_tiro_boss > delay:
            self.ultimo_tiro_boss = agora
            if self.fase == self.FASE_RAIVA:
                # rajada em leque
                for ang in range(-30, 31, 15):
                    rad = math.radians(ang + 90)
                    vx = math.cos(rad) * 5
                    vy = math.sin(rad) * 5
                    t = TiroInimigo(self.rect.centerx, self.rect.bottom,
                                    self.rect.centerx + vx * 10,
                                    self.rect.bottom + vy * 10, vel=5)
                    grupo_ti.add(t); todos.add(t)
            else:
                t = TiroInimigo(self.rect.centerx, self.rect.bottom,
                                jogador.rect.centerx, jogador.rect.centery)
                grupo_ti.add(t); todos.add(t)


class PowerUp(pygame.sprite.Sprite):
    TIPOS = ["vida", "tiro", "triplo", "escudo", "pontos"]

    def __init__(self):
        super().__init__()
        self.tipo = random.choice(self.TIPOS)
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        cores = {
            "vida":   VERDE_LIMA,
            "tiro":   AMARELO,
            "triplo": AZUL_NEON,
            "escudo": ROXO,
            "pontos": ROSA_CHOQUE,
        }
        simbolos = {"vida": "+", "tiro": "T", "triplo": "3", "escudo": "S", "pontos": "$"}
        cor = cores[self.tipo]
        pygame.draw.circle(self.image, cor, (18, 18), 17)
        pygame.draw.circle(self.image, BRANCO, (18, 18), 17, 2)
        img_s = fonte_pequena.render(simbolos[self.tipo], True, PRETO)
        self.image.blit(img_s, img_s.get_rect(center=(18, 18)))
        self.rect = self.image.get_rect(center=(random.randint(30, LARGURA - 30), -30))
        self.vel_y = 3
        # anima ao flutuante
        self.base_y = -30
        self.t = 0

    def update(self):
        self.t += 0.1
        self.rect.y += self.vel_y
        self.rect.x += int(math.sin(self.t) * 0.8)
        if self.rect.top > ALTURA:
            self.kill()


#                                          
# HUD / UI
#                                          

def desenhar_hud(jogador, pontos, nivel, bosses, combo, melhor):
    # Painel lateral esquerdo
    pygame.draw.rect(TELA, (15, 20, 40, 200), (10, 10, 230, 140), border_radius=8)
    pygame.draw.rect(TELA, AZUL_NEON, (10, 10, 230, 140), 1, border_radius=8)

    texto("INTEGRIDADE", fonte_tiny, VERDE_LIMA, 15, 18, centro=False)
    barra(15, 35, jogador.vida, jogador.vida_max, 220, VERDE_LIMA)

    if jogador.escudo > 0:
        texto("ESCUDO", fonte_tiny, ROXO, 15, 58, centro=False)
        barra(15, 75, jogador.escudo, 50, 220, ROXO)

    texto(f"AMMO: {jogador.tiros}", fonte_tiny, AMARELO, 15, 98, centro=False)
    texto(f"N VEL: {nivel}", fonte_tiny, AZUL_CLARO, 15, 120, centro=False)
    if jogador.powerup_triplo > 0:
        texto(f"TRIPLO: {jogador.powerup_triplo // 60 + 1}s", fonte_tiny, AZUL_NEON, 120, 120, centro=False)

    # Painel direito
    pygame.draw.rect(TELA, (15, 20, 40), (LARGURA - 200, 10, 190, 100), border_radius=8)
    pygame.draw.rect(TELA, ROSA_CHOQUE, (LARGURA - 200, 10, 190, 100), 1, border_radius=8)
    texto(f"SCORE",  fonte_tiny,    BRANCO,     LARGURA - 200, 18, centro=False)
    texto(f"{pontos}", fonte_media, AZUL_NEON,  LARGURA - 105, 55)
    texto(f"MELHOR: {melhor}", fonte_tiny, CINZA, LARGURA - 200, 95, centro=False)

    # Combo
    if combo >= 3:
        cor_combo = AMARELO if combo < 8 else ROSA_CHOQUE
        texto(f"COMBO x{combo}!", fonte_media, cor_combo, LARGURA // 2, 30)

    # Barra do boss
    for boss in bosses:
        cor_boss = VERMELHO if boss.fase == Boss.FASE_RAIVA else ROXO
        label = "BOSS BOSS RAIVA!" if boss.fase == Boss.FASE_RAIVA else "BOSS"
        texto(label, fonte_pequena, cor_boss, LARGURA // 2, 160)
        barra(LARGURA // 2 - 200, 185, boss.vida, boss.vida_max, 400, cor_boss, (30, 10, 10))


#                                          
# MENUS
#                                          

def menu_inicial():
    estrelas = criar_estrelas(120)
    while True:
        desenhar_fundo(estrelas)
        texto("COSMIC HEAT", fonte_grande, AZUL_NEON, LARGURA // 2, 160)
        texto("D E L U X E", fonte_media, ROSA_CHOQUE, LARGURA // 2, 220)

        pygame.draw.rect(TELA, (20, 30, 60), (LARGURA // 2 - 200, 280, 400, 240), border_radius=12)
        pygame.draw.rect(TELA, AZUL_NEON, (LARGURA // 2 - 200, 280, 400, 240), 2, border_radius=12)

        linhas = [
            ("ENTER - Come ar",        AMARELO),
            ("Setas / WASD - Mover",   BRANCO),
            ("ESPA O - Atirar",        BRANCO),
            ("P - Pausar | ESC - Sair",BRANCO),
            ("R - Reiniciar (game over)",CINZA),
        ]
        for i, (msg, cor) in enumerate(linhas):
            texto(msg, fonte_pequena, cor, LARGURA // 2, 310 + i * 42)

        pygame.display.flip()
        RELOGIO.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


def tela_game_over(pontos, venceu, melhor):
    estrelas = criar_estrelas(80)
    while True:
        desenhar_fundo(estrelas)
        camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        camada.fill((0, 0, 0, 160))
        TELA.blit(camada, (0, 0))

        if venceu:
            texto("VOC  VENCEU!", fonte_grande, VERDE_LIMA, LARGURA // 2, ALTURA // 2 - 120)
        else:
            texto("GAME OVER", fonte_grande, VERMELHO, LARGURA // 2, ALTURA // 2 - 120)

        texto(f"Pontua ao: {pontos}", fonte_media, BRANCO, LARGURA // 2, ALTURA // 2 - 30)
        texto(f"Melhor: {melhor}", fonte_media, AMARELO, LARGURA // 2, ALTURA // 2 + 30)
        texto("ENTER - jogar novamente  |  ESC - sair", fonte_pequena, CINZA, LARGURA // 2, ALTURA // 2 + 100)

        pygame.display.flip()
        RELOGIO.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True   # reiniciar
                if evento.key == pygame.K_ESCAPE:
                    return False  # sair


#                                          
# LOOP PRINCIPAL
#                                          

def criar_grupos():
    todos       = pygame.sprite.Group()
    tiros       = pygame.sprite.Group()
    tiros_ini   = pygame.sprite.Group()
    inimigos    = pygame.sprite.Group()
    meteoros    = pygame.sprite.Group()
    powerups    = pygame.sprite.Group()
    bosses      = pygame.sprite.Group()
    particulas  = pygame.sprite.Group()
    jogador = Nave()
    todos.add(jogador)
    return todos, tiros, tiros_ini, inimigos, meteoros, powerups, bosses, particulas, jogador


def jogo():
    menu_inicial()

    melhor = 0

    while True:   # loop de partidas
        (todos, tiros, tiros_ini, inimigos,
         meteoros, powerups, bosses, particulas, jogador) = criar_grupos()

        estrelas = criar_estrelas(100)
        pontos   = 0
        nivel    = 1
        pausado  = False
        venceu   = False
        shake    = 0
        combo    = 0
        combo_timer = 0

        SPAWN_INI  = pygame.USEREVENT + 1
        SPAWN_MET  = pygame.USEREVENT + 2
        SPAWN_PWR  = pygame.USEREVENT + 3

        pygame.time.set_timer(SPAWN_INI, 850)
        pygame.time.set_timer(SPAWN_MET, 1300)
        pygame.time.set_timer(SPAWN_PWR, 6000)

        rodando = True
        while rodando:
            RELOGIO.tick(FPS)
            dt = RELOGIO.get_time()

            #    Eventos   
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if evento.key == pygame.K_p:
                        pausado = not pausado

                if not pausado:
                    if evento.type == SPAWN_INI:
                        i = Inimigo(nivel)
                        inimigos.add(i); todos.add(i)
                    if evento.type == SPAWN_MET:
                        m = Meteoro(nivel)
                        meteoros.add(m); todos.add(m)
                    if evento.type == SPAWN_PWR:
                        p = PowerUp()
                        powerups.add(p); todos.add(p)

            if pausado:
                desenhar_fundo(estrelas)
                todos.draw(TELA)
                camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                camada.fill((0, 0, 0, 140))
                TELA.blit(camada, (0, 0))
                texto("PAUSADO", fonte_grande, AMARELO, LARGURA // 2, ALTURA // 2)
                texto("P - continuar", fonte_pequena, BRANCO, LARGURA // 2, ALTURA // 2 + 70)
                pygame.display.flip()
                continue

            #    Atirar   
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                jogador.atirar(tiros, todos)

            #    Update   
            todos.update()
            nivel = 1 + pontos // 300

            # Inimigos atiram
            for ini in inimigos:
                ini.tentar_atirar(jogador, tiros_ini, todos)

            # Boss spawn (cada 800 pontos, m x 3 bosses simult neos)
            if pontos >= 500 and len(bosses) == 0 and not venceu:
                b = Boss(nivel)
                bosses.add(b); todos.add(b)
            for b in bosses:
                b.atirar(jogador, tiros_ini, todos)

            #    Colisoes   

            # tiro do jogador   inimigos
            acertos = pygame.sprite.groupcollide(inimigos, tiros, False, True)
            for ini, _ in acertos.items():
                ini.vida -= 1
                if ini.vida <= 0:
                    criar_explosao(ini.rect.centerx, ini.rect.centery, ini.cor, particulas, todos)
                    ini.kill()
                    pontos += 30 + nivel * 5
                    combo += 1
                    combo_timer = 180
                    if random.random() < 0.15:
                        pw = PowerUp()
                        pw.rect.center = ini.rect.center
                        powerups.add(pw); todos.add(pw)

            # tiro do jogador   meteoros
            acertos_met = pygame.sprite.groupcollide(meteoros, tiros, False, True)
            for met, _ in acertos_met.items():
                met.vida -= 1
                if met.vida <= 0:
                    criar_explosao(met.rect.centerx, met.rect.centery, CINZA, particulas, todos)
                    met.kill()
                    pontos += 15

            # tiro do jogador   boss
            acertos_boss = pygame.sprite.groupcollide(bosses, tiros, False, True)
            for boss, lista in acertos_boss.items():
                boss.vida -= len(lista) * 5
                pontos += 10 * len(lista)
                if boss.vida <= 0:
                    criar_explosao(boss.rect.centerx, boss.rect.centery, ROXO, particulas, todos, qtd=40)
                    boss.kill()
                    pontos += 1000
                    venceu = True

            # tiro inimigo   jogador
            if pygame.sprite.spritecollide(jogador, tiros_ini, True):
                if jogador.levar_dano(12):
                    shake = 6
                    criar_explosao(jogador.rect.centerx, jogador.rect.top, VERMELHO, particulas, todos, qtd=10)

            # inimigos   jogador
            if pygame.sprite.spritecollide(jogador, inimigos, True):
                if jogador.levar_dano(20):
                    shake = 10
                    combo = 0
                    criar_explosao(jogador.rect.centerx, jogador.rect.top, VERMELHO, particulas, todos)

            # meteoros   jogador
            if pygame.sprite.spritecollide(jogador, meteoros, True):
                if jogador.levar_dano(25):
                    shake = 12
                    combo = 0

            # boss   jogador (contato)
            for b in pygame.sprite.spritecollide(jogador, bosses, False):
                if jogador.levar_dano(1):
                    shake = max(shake, 5)

            # powerups   jogador
            for pw in pygame.sprite.spritecollide(jogador, powerups, True):
                if pw.tipo == "vida":
                    jogador.vida = min(jogador.vida_max, jogador.vida + 30)
                elif pw.tipo == "tiro":
                    jogador.tiros += 60
                elif pw.tipo == "triplo":
                    jogador.powerup_triplo = 600  # ~10 segundos
                elif pw.tipo == "escudo":
                    jogador.escudo = min(50, jogador.escudo + 50)
                elif pw.tipo == "pontos":
                    pontos += 150

            #    Combo timer   
            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo = 0

            #    B nus de combo   
            if combo >= 5:
                pontos += combo // 5   # b nus passivo por combo alto

            if shake > 0: shake -= 1

            #    Desenho   
            desenhar_fundo(estrelas)

            ox = random.randint(-shake, shake) if shake else 0
            oy = random.randint(-shake, shake) if shake else 0
            for sprite in todos:
                TELA.blit(sprite.image, (sprite.rect.x + ox, sprite.rect.y + oy))

            desenhar_hud(jogador, pontos, nivel, bosses, combo, melhor)

            #    Game Over / Vitoria   
            if jogador.vida <= 0 or venceu:
                if pontos > melhor:
                    melhor = pontos
                pygame.display.flip()
                pygame.time.wait(800)
                reiniciar = tela_game_over(pontos, venceu, melhor)
                rodando = False
                if not reiniciar:
                    pygame.quit(); sys.exit()

            pygame.display.flip()


#                                          
if __name__ == "__main__":
    jogo()