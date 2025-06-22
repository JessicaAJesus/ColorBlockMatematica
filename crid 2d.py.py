import pygame   #biblioteca para importar elementos de jogos
import random   #biblioteca para gerar números aleatórios nos blocos

pygame.init()
largura = 800      #largura e altura da tela do jogo
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("JOGO BLOCOS")

amarelo = (255, 255, 0)      #cores que serão usadas nos blocos
vermelho = (255, 0, 0)
verde= (0, 255, 0)
azul= (0, 0, 255)
roxo = (128, 0, 128)
laranja = (255, 165, 0)

tela_fundo= (0, 0, 0)    #cor preta para a tela de fundo 

largura_bloco = 70        #larguraXaltura dos blocos + espaço entre eles
altura_bloco = 70
espaço = 33

fonte=pygame.font.Font(None,44)     #definindo fontes, tamanho e variável para as cores dos blocos
numero_cor=(255,255,255)

def matriz_bloco(cores):         #função para desenhar os blocos a partir de uma matriz 
    matriz = []
    for linha_index, linha_cores in enumerate(cores):
        linha_blocos = []
        for coluna_index, cor in enumerate(linha_cores):
            x = coluna_index * (largura_bloco + espaço)
            y = linha_index * (altura_bloco + espaço)
            bloco_rect = pygame.Rect(x, y, largura_bloco, altura_bloco)
            num_aleatorio=random.randint(1,99)                 #números aleatórios que serão colocados nos blocos
            linha_blocos.append((bloco_rect, cor,num_aleatorio))   #parâmetros para colocar os blocos, cores e números
        matriz.append(linha_blocos)
    return matriz

matriz_cores = [
    [vermelho, amarelo, azul, verde, verde, vermelho, laranja, azul, verde, roxo],
    [verde, roxo, vermelho, amarelo, azul, verde, roxo, laranja, amarelo, azul],
    [amarelo, azul, verde, roxo, vermelho, amarelo, azul, verde, roxo, laranja],          #posição de uma matriz para cada cor de bloco
    [azul, verde, roxo, vermelho, laranja, azul, verde, roxo, vermelho, amarelo],
    [roxo, vermelho, amarelo, azul, verde, roxo, laranja, amarelo, azul, verde]
]

desenhar_matriz= matriz_bloco(matriz_cores)

rodar = True
while rodar:                           
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodar = False

    tela.fill(tela_fundo) 

    for linha in desenhar_matriz:           #desenhar blocos
        for bloco_data in linha: 
            bloco_rect = bloco_data[0]
            cor_do_bloco = bloco_data[1]
            numero_bloco=bloco_data[2]
            pygame.draw.rect(tela, cor_do_bloco, bloco_rect)

            texto=fonte.render(str(numero_bloco),True,numero_cor)     #ajustar os números centralizados nos blocos
            texto_rect=texto.get_rect(center=bloco_rect.center)
            tela.blit(texto,texto_rect)
    pygame.display.flip() 
pygame.quit()