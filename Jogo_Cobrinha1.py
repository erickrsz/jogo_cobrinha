import pygame
import random
import sys

pygame.init()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

LARGURA = 600
ALTURA = 600
TAMANHO_BLOCO = 20
VELOCIDADE = 10

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Cobrinha')
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont('Arial', 25)

def desenhar_cobra(pixels, tamanho_bloco):
    for pos in pixels:
        pygame.draw.rect(tela, VERDE, [pos[0], pos[1], tamanho_bloco, tamanho_bloco])

def desenhar_comida(pos_x, pos_y, tamanho_bloco):
    pygame.draw.rect(tela, VERMELHO, [pos_x, pos_y, tamanho_bloco, tamanho_bloco])

def exibir_pontuacao(pontuacao):
    texto = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto, [10, 10])

def exibir_game_over(pontuacao):
    tela.fill(PRETO)
    texto_game_over = fonte.render("GAME OVER", True, VERMELHO)
    texto_pontuacao = fonte.render(f"Pontuação final: {pontuacao}", True, BRANCO)
    texto_reiniciar = fonte.render("Pressione ESPAÇO para jogar novamente ou ESC para sair", True, BRANCO)
    
    tela.blit(texto_game_over, [LARGURA // 2 - 70, ALTURA // 2 - 50])
    tela.blit(texto_pontuacao, [LARGURA // 2 - 100, ALTURA // 2])
    tela.blit(texto_reiniciar, [LARGURA // 2 - 250, ALTURA // 2 + 50])
    pygame.display.update()

def iniciar_jogo():
    game_over = False
    game_encerrado = False
    
    x = LARGURA // 2
    y = ALTURA // 2
    
    dx = TAMANHO_BLOCO
    dy = 0
    
    corpo_cobra = []
    tamanho_cobra = 1
    
    comida_x = round(random.randrange(0, LARGURA - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
    comida_y = round(random.randrange(0, ALTURA - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
    
    pontuacao = 0
    
    while not game_over:
        
        while game_encerrado:
            exibir_game_over(pontuacao)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    game_over = True
                    game_encerrado = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        game_over = True
                        game_encerrado = False
                    if evento.key == pygame.K_SPACE:
                        iniciar_jogo()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and dx == 0:
                    dx = -TAMANHO_BLOCO
                    dy = 0
                elif evento.key == pygame.K_RIGHT and dx == 0:
                    dx = TAMANHO_BLOCO
                    dy = 0
                elif evento.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -TAMANHO_BLOCO
                elif evento.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = TAMANHO_BLOCO
        
        if x >= LARGURA or x < 0 or y >= ALTURA or y < 0:
            game_encerrado = True
        
        x += dx
        y += dy
        
        tela.fill(PRETO)
        
        desenhar_comida(comida_x, comida_y, TAMANHO_BLOCO)
        
        cabeca_cobra = []
        cabeca_cobra.append(x)
        cabeca_cobra.append(y)
        corpo_cobra.append(cabeca_cobra)
        
        if len(corpo_cobra) > tamanho_cobra:
            del corpo_cobra[0]
        
        for segmento in corpo_cobra[:-1]:
            if segmento == cabeca_cobra:
                game_encerrado = True
        
        desenhar_cobra(corpo_cobra, TAMANHO_BLOCO)
        
        exibir_pontuacao(pontuacao)
        
        pygame.display.update()
        
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, LARGURA - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
            comida_y = round(random.randrange(0, ALTURA - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
            tamanho_cobra += 1
            pontuacao += 10
        
        relogio.tick(VELOCIDADE)
    
    pygame.quit()
    sys.exit()

iniciar_jogo()
