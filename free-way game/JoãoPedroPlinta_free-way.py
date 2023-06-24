# Feito por João Pedro Plinta

import pygame
import os
from pathlib import Path

# Inicializa o pygame
pygame.init()

# Configura a janela do jogo
largura_tela = 900
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Free Way")

# Define as cores
branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (16, 167, 227)
vermelho = (255, 0, 0)
roxo = (128, 0, 128)

def caminho_arquivo(nome:str):
    caminho = os.path.dirname(os.path.realpath(__file__))
    caminhoAbsoluto = Path(os.path.join(caminho, "img/", nome))
    return caminhoAbsoluto

# Carrega o background
background = pygame.image.load(caminho_arquivo("background-frogger.png"))
background = pygame.transform.scale(background, (largura_tela, altura_tela))

# Configura o sapo
tamanho_sapo = 45

posicao_sapo = [largura_tela/2, altura_tela - tamanho_sapo]
retangulo_sapo = pygame.Rect(posicao_sapo[0], posicao_sapo[1], tamanho_sapo, tamanho_sapo)

# Configura os carros
largura_carro = 70
altura_carro = 50
espacamento_entre_grupos = 100
carros_grupo1 = [
    pygame.Rect(320, altura_tela - altura_carro * 2, largura_carro, altura_carro),
    pygame.Rect(110, altura_tela - altura_carro * 3, largura_carro, altura_carro),
    pygame.Rect(550, altura_tela - altura_carro * 4, largura_carro, altura_carro),
    pygame.Rect(840, altura_tela - altura_carro * 5, largura_carro, altura_carro)
]
carros_grupo2 = [
    pygame.Rect(510, altura_tela - altura_carro * 5 - espacamento_entre_grupos, largura_carro, altura_carro),
    pygame.Rect(660, altura_tela - altura_carro * 6 - espacamento_entre_grupos, largura_carro, altura_carro),
    pygame.Rect(750, altura_tela - altura_carro * 7 - espacamento_entre_grupos, largura_carro, altura_carro),
    pygame.Rect(900, altura_tela - altura_carro * 8 - espacamento_entre_grupos, largura_carro, altura_carro)
]

# Define as velocidades dos carros
velocidades_carro_grupo1 = [3, 4, 5, 6]
velocidades_carro_grupo2 = [2, 3, 4, 5]

# Carrega a imagem do carro
imagem_carro = pygame.image.load(caminho_arquivo("carro.png"))
imagem_carro = pygame.transform.scale(imagem_carro, (largura_carro, altura_carro))

# Carrega a imagem do sapo
imagem_sapo = pygame.image.load(caminho_arquivo("frogger.png"))
imagem_sapo = pygame.transform.scale(imagem_sapo, (tamanho_sapo, tamanho_sapo))

# Carrega a imagem de derrota
imagem_derrota = pygame.image.load(caminho_arquivo("perdeu.png"))
imagem_derrota = pygame.transform.scale(imagem_derrota, (largura_tela, altura_tela))

# Configura o relógio
relogio = pygame.time.Clock()

# Define a função de instruções
def instrucoes():
    instrucoes_texto = [
        ("Instruções:", branco),
        ("- Use as setas do teclado para mover o sapo.", branco),
        ("- Desvie dos carros e atravesse a rua em segurança.", branco),
        ("- O objetivo é chegar ao outro lado da rua.", branco),
        ("", branco),
        ("- Cuidado para não perder todas as vidas!", vermelho),
        ("", branco),
        ("Pressione ESPAÇO para voltar ao menu.", azul)
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

        tela.fill(preto)
        fonte_instrucoes = pygame.font.SysFont(None, 30)

        for i, (linha, cor) in enumerate(instrucoes_texto):
            texto = fonte_instrucoes.render(linha, True, cor)
            x = largura_tela/2 - texto.get_width()/2
            y = altura_tela/2 - len(instrucoes_texto)/2 * texto.get_height() + i * texto.get_height()
            tela.blit(texto, (x, y))

        pygame.display.flip()

# Define a função de menu
def menu():
    opcoes = ["Jogar", "Instruções", "Sair"]
    selecao = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecao = (selecao - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecao = (selecao + 1) % len(opcoes)
                elif evento.key == pygame.K_SPACE:
                    if selecao == 0:
                        return
                    elif selecao == 1:
                        instrucoes()
                    elif selecao == 2:
                        pygame.quit()
                        exit()

        tela.fill(preto)
        fonte_menu = pygame.font.SysFont(None, 40)

        for i, opcao in enumerate(opcoes):
            cor = azul if i == selecao else branco
            texto = fonte_menu.render(opcao, True, cor)
            x = largura_tela/2 - texto.get_width()/2
            y = altura_tela/2 - len(opcoes)/2 * texto.get_height() + i * texto.get_height()
            tela.blit(texto, (x, y))

        pygame.display.flip()

# Define a função de derrota
def derrota():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

        tela.blit(imagem_derrota, (0, 0))
        pygame.display.flip()

# Loop principal do jogo
menu()
fim_de_jogo = False
vidas = 3
voltar_menu = False
linha_final = False
posicao_anterior_sapo = posicao_sapo[0]  # Adiciona essa linha para armazenar a posição anterior do sapo
moveu_para_frente = False  # Variável para controlar se o sapo se moveu para frente
while True:
    if fim_de_jogo:
        vidas -= 1
        if vidas <= 0:
            derrota()
            vidas = 3
            moveu_para_frente = False  # Reinicia o controle de movimento para frente
            voltar_menu = True
        posicao_sapo = [largura_tela/2, altura_tela - tamanho_sapo]
        retangulo_sapo = pygame.Rect(posicao_sapo[0], posicao_sapo[1], tamanho_sapo, tamanho_sapo)
        fim_de_jogo = False

    # Lida com eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Volta para o menu se voltar_menu for True
    if voltar_menu:
        menu()
        voltar_menu = False

    # Move o sapo
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a] and posicao_sapo[0] > 0:
        posicao_sapo[0] -= 5
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d] and posicao_sapo[0] < largura_tela - tamanho_sapo:
        posicao_anterior_sapo = posicao_sapo[0]  # Atualiza a posição anterior do sapo
        posicao_sapo[0] += 5
    elif teclas[pygame.K_UP] or teclas[pygame.K_w] and posicao_sapo[1] > 0:
        posicao_sapo[1] -= 5
    elif teclas[pygame.K_DOWN] or teclas[pygame.K_s] and posicao_sapo[1] < altura_tela - tamanho_sapo:
        posicao_sapo[1] += 5
        moveu_para_frente = False
    retangulo_sapo = pygame.Rect(posicao_sapo[0], posicao_sapo[1], tamanho_sapo, tamanho_sapo)

    # Move os carros do grupo 1
    for i, retangulo_carro in enumerate(carros_grupo1):
        velocidade_carro = velocidades_carro_grupo1[i % len(velocidades_carro_grupo1)]
        retangulo_carro.move_ip(velocidade_carro, 0)
        if retangulo_carro.right > largura_tela:
            retangulo_carro.left = 0

    # Move os carros do grupo 2
    for i, retangulo_carro in enumerate(carros_grupo2):
        velocidade_carro = velocidades_carro_grupo2[i % len(velocidades_carro_grupo2)]
        retangulo_carro.move_ip(velocidade_carro, 0)
        if retangulo_carro.right > largura_tela:
            retangulo_carro.left = 0

    # Verifica por colisões
    for retangulo_carro in carros_grupo1 + carros_grupo2:
        if retangulo_sapo.colliderect(retangulo_carro):
            fim_de_jogo = True
            break

    # Verifica se o sapo chegou ao final
    if posicao_sapo[1] < tamanho_sapo:
        if not linha_final:
            linha_final = True
            posicao_sapo[1] = altura_tela - tamanho_sapo
        else:
            posicao_sapo = [largura_tela/2, altura_tela - tamanho_sapo]
            retangulo_sapo = pygame.Rect(posicao_sapo[0], posicao_sapo[1], tamanho_sapo, tamanho_sapo)
            linha_final = False

    # Desenha tudo
    tela.blit(background, (0, 0))
    tela.blit(imagem_sapo, retangulo_sapo)
    for retangulo_carro in carros_grupo1 + carros_grupo2:
        tela.blit(imagem_carro, retangulo_carro)

    # Desenha as vidas na tela
    fonte_vidas = pygame.font.SysFont(None, 30)
    texto_vidas = fonte_vidas.render(f"Vidas: {vidas}", True, preto)

    # Define as dimensões e posição do retângulo de fundo das vidas
    largura_texto_vidas = texto_vidas.get_width()
    altura_texto_vidas = texto_vidas.get_height()
    retangulo_background_vidas = pygame.Rect(10, 10, largura_texto_vidas + 10, altura_texto_vidas + 10)

    # Desenha o retângulo de fundo das vidas
    pygame.draw.rect(tela, branco, retangulo_background_vidas)

    # Desenha o texto das vidas em cima do retângulo de fundo
    tela.blit(texto_vidas, (retangulo_background_vidas.x + 5, retangulo_background_vidas.y + 5))

    pygame.display.flip()

    # Define a taxa de quadros por segundo
    relogio.tick(60)