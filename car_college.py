# Car College
# prog: Ant. Edward Facundo
# game design: Bruno Saraiva
# game art: Helton Barata e Fernando Santos
'''
Importa os modulos necessarios, incluso no diretorio.
'''
from copy import *
import sys, pygame, os, time,eztext, random
from pygame.locals import *

'''
definicoes
'''
pygame.init()                                     # inicializa a engine pygame
pygame.display.set_caption("FGF - Car College")   # define titulo do game
tTamanho = width,height = 800,600 #320,233        # define o tamanho da tela.
tela =  pygame.display.set_mode(tTamanho)         # inicializa a tela e seta o tamanho
FULLSCREEN = False                                # flag para indicar o estado do game
SAINDO = False
PLAYING = False
DEBUG = False
trilha = {}
trilha['musica'] = "audio/carcollege.wav"
trilha['loop'] = "audio/carcollege_2.wav"
trilha['tocando'] = False


level = ''
playRect = ( 350, 390, 100, 35 );
menuRect = ( 350, 440, 100, 35 );
regrasRect = ( 480, 200, 100, 35 );
rankingRect = ( 480, 250, 100, 35 );
gameRect = ( 480, 300, 100, 35 );
exitRect = ( 350, 540, 100, 35 );
exitRankingRect = ( 160, 560, 100, 35 );
menuRankingRect = ( 560, 560, 100, 35 ) 
gamePontuacaoRect  = ( 856, 50, 100, 35) 
gameScoreRect  = ( 856, 80, 100, 35) 
gameFuelRect  = ( 856, 110, 100, 35)
gameFuelPontosRect  = ( 856, 140, 100, 35)
gameLivesRect  = ( 856, 170, 100, 35)   
iMenuPrincipal = '' 
iRanking = ''
iPontuacao = ''
iGame = '' 
iCarPlayer = '' 
iCarCinza = pygame.Surface
iCarPreto = ''
iCarPlayerSprite = pygame.sprite.Sprite()
iBuraco = pygame.sprite.Sprite()
iCarPos = ''
iGameOver = ''
carMovendo = ''
carCinzaMovendo = ''
iFumaca = 0
item_gasolina_rect = (0,0,0,0)
buraco = pygame.Surface
telaBorda = 30
item_gasolina = ''
item_bandeira = ''
item_posicao = ''
txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt="DIGITE SEU NOME: ")
item_gasolina_ativo = False
item_bandeira_ativo = False
fumaca = {}
tela_atual = ''
segundo_inicial = 0
segundo_atual = 0
bloco1 = pygame.sprite.Sprite()
bloco2 = pygame.sprite.Sprite()
bloco3 = pygame.sprite.Sprite()
bloco4 = pygame.sprite.Sprite()
bloco5 = pygame.sprite.Sprite()
bloco6 = pygame.sprite.Sprite()
bloco7 = pygame.sprite.Sprite()
bloco8 = pygame.sprite.Sprite()
bloco9 = pygame.sprite.Sprite()
bloco10 = pygame.sprite.Sprite()
bloco11 = pygame.sprite.Sprite()
bloco12 = pygame.sprite.Sprite()
bloco13 = pygame.sprite.Sprite()
bloco14 = pygame.sprite.Sprite()
bloco16 = pygame.sprite.Sprite()
bloco17 = pygame.sprite.Sprite()
bloco18 = pygame.sprite.Sprite()
bloco19 = pygame.sprite.Sprite()
bloco20 = pygame.sprite.Sprite()
bloco21 = pygame.sprite.Sprite()

item_posicoes = {}
item_posicoes[0] = ( 30, 40  )
item_posicoes[1] = ( 740,40  )
item_posicoes[2] = ( 740,500 )
item_posicoes[3] = ( 30, 500  )
'''
definicao da classe jogador
'''
class Jogador(pygame.sprite.Sprite):
        def __init__(self):
                self.lives = 3
                self.nome = ''
                self.carPos = [350,390]        
                self.carMov = 5
                self.carDirecao =  'direita'
                self.Pontuacao = 0
                self.Fuel = 0
               # pygame.sprite.Sprite.__init__(self)
                #self.image =  carregarImg("carplayer.png",-1)
            
'''
funcoes e classes auxiliares
'''
class Contador():
        ''' Por motivos praticos usaremos contadores proprios - Adicionar thread '''
        minuto =  0
        segundo = 0
        
        def __init__(self,ordem = "cresc", minutos = 00, segundos = 00):
                self.minuto = minutos
                self.segundo = segundos
                self.ordem = ordem
                
        def tick(self,ordem, segundos = 1): # melhorar o direcionamento do tick
                self.ordem = ordem
                self.tickSegundo(segundos)
                                       
        def tickMinuto(self,minutos = 1):
                if self.ordem == "cresc" and self.minuto != 0:
                        self.minuto = self.minuto + minutos
                if self.ordem == "decres" and self.minuto != 0:
                        self.minuto = self.minuto - minutos                
                
        def tickSegundo(self,segundos):
                if self.segundo <= 59  and self.segundo > 0 :
                        if self.ordem == "cresc":
                                self.segundo = self.segundo + segundos
                        if self.ordem == "decres":
                                self.segundo = self.segundo - segundos 
                else:
                        if self.ordem == "cresc":
                                self.segundo = 00
                        if self.ordem == "decres":
                                self.segundo = 59
                                
                        self.tickMinuto()                   
          
        def minutoDecimal(self):
                if self.minuto < 10:
                        return "0"+str(self.minuto)
                else:
                        return str(self.minuto)
        
        def segundoDecimal(self):
                if self.segundo < 10:
                        return "0"+str(self.segundo)
                else:
                        return str(self.segundo)    



def carregarImg(arquivo, colorkey=False, diretorio='imgs'):
    file = os.path.join(diretorio, arquivo)
    image = pygame.image.load(file)
    if colorkey:
        if colorkey == -1: 
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        image = image.convert()
    else: 
        image = image.convert_alpha()
    return image
    
def carregarTxt(texto,tamanho,cor,posicao):
        font = pygame.font.Font(None, tamanho)
        text = font.render(texto, 1, cor)
        tela.blit(text,posicao)
        
def ranking(nome = None,pontuacao = None):
            arquivo = open(".ranking","r")
            infos = arquivo.read()
            infos = infos.split("|")
            jogadores = infos[0]
            jogadores = jogadores.split(":")
            pontos = infos[1].rstrip()
            pontos = pontos.split(":")
            
            if ( nome != None ) and ( pontuacao != None ):
                pontos.append(pontuacao)
                jogadores.append(nome)
            else:
                pontos.append(0)
                jogadores.append("ghost")
                
            pontuacao1 = int(pontos[0])
            pontuacao2 = int(pontos[1])
            pontuacao3 = int(pontos[2])
            pontuacao4 = int(pontos[3])
            
            ranking_final = {}
                        
            # implementacao rustica comparativa de maior-numero. Nada elegante mas didatica.
            
            if  ( pontuacao1 > pontuacao2 ) and ( pontuacao1 > pontuacao3 ) and ( pontuacao1 > pontuacao4 ):
                ranking_final[0] = ( jogadores[0], pontuacao1 )
                del pontos[0]
                del jogadores[0]
            if  ( pontuacao2 > pontuacao1 ) and ( pontuacao2 > pontuacao3 ) and ( pontuacao1 > pontuacao4 ):
                ranking_final[0] = ( jogadores[1], pontuacao2 )
                del pontos[1]
                del jogadores[1]
            if  ( pontuacao3 > pontuacao1 ) and ( pontuacao3 > pontuacao2 ) and ( pontuacao1 > pontuacao4 ):   
                ranking_final[0] = ( jogadores[2], pontuacao3 )
                del pontos[2]
                del jogadores[2]
            if  ( pontuacao4 > pontuacao1 ) and ( pontuacao > pontuacao2 ) and ( pontuacao > pontuacao3 ):   
                ranking_final[0] = ( jogadores[3], pontuacao4 )
                del pontos[3]
                del jogadores[3]
 
            pontuacao1 = pontos[0]
            pontuacao2 = pontos[1]
            pontuacao3 = pontos[2]
            
            jogador1 = jogadores[0]
            jogador2 = jogadores[1]
            jogador3 = jogadores[2]
                        
            if  ( pontuacao1 > pontuacao2 ) and ( pontuacao1 > pontuacao3 ):
                ranking_final[1] = ( jogador1, pontuacao1 )
                del pontos[0]
                del jogadores[0]
            if  ( pontuacao2 > pontuacao1 ) and ( pontuacao2 > pontuacao3 ):
                ranking_final[1] = ( jogador2, pontuacao2 )
                del pontos[1]
                del jogadores[1]
            if  ( pontuacao3 > pontuacao1 ) and ( pontuacao3 > pontuacao2 ):   
                ranking_final[1] = ( jogador3, pontuacao3 )
                del pontos[2]
                del jogadores[2]
            
            pontuacao1 = pontos[0]
            pontuacao2 = pontos[1]
            jogador1 = jogadores[0]
            jogador2 = jogadores[1]
            
                       
            if  ( pontuacao1 > pontuacao2 ):
                ranking_final[2] = ( jogador1, pontuacao1 )
                ranking_final[3] = ( jogador2, pontuacao2 )
                
            if  ( pontuacao2 > pontuacao1 ):
                ranking_final[2] = ( jogador2, pontuacao2 )
                ranking_final[3] = ( jogador1, pontuacao1 ) 
                
            ranking_buffer = "%s:%s:%s|%s:%s:%s" % (ranking_final[0][0],ranking_final[1][0],ranking_final[2][0],ranking_final[0][1],ranking_final[1][1],ranking_final[2][1])
            arquivo.close()
            arquivo = open("ranking","w")
            arquivo.write(ranking_buffer)
            if DEBUG:
                print ranking_buffer
            
            
            return ranking_final
            
def colisaoTxt(rect):
        mouse = pygame.mouse.get_pos()
        #debug - print mouse
        if ( ( (mouse[0] >= rect[0] ) & (mouse[1] >= rect[1]) ) &  ( (mouse[0] <= rect[0]  + rect[2] ) & (mouse[1] <= rect[1] + rect[3]) )  ) :
                return True
       
#carrega a trilha
pygame.mixer.music.load(trilha['musica'])

#video de Introducao
introVideo = pygame.movie.Movie("video/intro.mpg")
if ( introVideo.has_video() ):
        introVideo.set_display(tela)
        introVideo.play()
else:
        print 'Video de Introducao Nao Encontrado...'
        sys.exit()
        
class Fumaca (pygame.sprite.Sprite):
    
    images = []
    pos = (0,0)
    animaIndex = 0
    
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images.append(carregarImg("fumaca01.png"))
        self.images.append(carregarImg("fumaca02.png"))
        self.images.append(carregarImg("fumaca03.png"))
        self.images.append(carregarImg("fumaca04.png")) 
        self.sprite = self.images[0]
        self.rect = self.sprite.get_rect()
        self.tick = 0
        self.animSentido = "frente"
        self.stop = False
        self.seguir = False
        
    def anima(self):
        if self.tick <= self.tick_limit:
            self.tick += 1
        else:
            if not self.stop:
                if self.animSentido == "frente" and self.animaIndex < len(self.images):
                    self.animaIndex += 1
                    if self.animaIndex == len(self.images):
                        self.animSentido = "tras"
                        
                if self.animSentido == "tras" and self.animaIndex > 0:
                    self.animaIndex -= 1
                    if self.animaIndex == 0:
                        self.animSentido = "frente"
                    
                self.sprite = self.images[self.animaIndex - 1]
                self.tick = 0

    def set_tick(self,numero):
        self.tick_limit = numero
        

class Bandeira (pygame.sprite.Sprite):
    
    images = []
    pos = (0,0)
    animaIndex = 0
    
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images.append(carregarImg("bandeira01.png"))
        self.images.append(carregarImg("bandeira02.png"))
        self.images.append(carregarImg("bandeira03.png"))
        self.sprite = self.images[0]
        self.rect = self.sprite.get_rect()
        self.tick = 0
        self.animSentido = "frente"
        self.stop = False
        self.seguir = False
        
    def anima(self):
        if self.tick <= self.tick_limit:
            self.tick += 1
        else:
            if not self.stop:
                if self.animSentido == "frente" and self.animaIndex < len(self.images):
                    self.animaIndex += 1
                    if self.animaIndex == len(self.images):
                        self.animSentido = "tras"
                        
                if self.animSentido == "tras" and self.animaIndex > 0:
                    self.animaIndex -= 1
                    if self.animaIndex == 0:
                        self.animSentido = "frente"
                    
                self.sprite = self.images[self.animaIndex - 1]
                self.tick = 0

    def set_tick(self,numero):
        self.tick_limit = numero

contador = Contador()
botao = carregarImg("btdefault.png")    
brect = botao.get_rect()

def jogar():
        ''' 
        Aqui esta o core do game play, regras, pontuacao e renderizacao do game principal.
        '''
        clock = pygame.time.Clock()
        tTamanho = width,height = 1024,600 #320,233                  # define o tamanho da tela.
        pygame.display.set_mode(tTamanho)
        global carCinzaMovendo, iCarCinza, iCarCinza_pos, txbx, iBuraco, clock, tela_atual, telaAtual, tela, iCarPlayer, iCarPos, PLAYING, item_gasolina, item_posicao, item_gasolina_ativo, contador, segundo_inical, segundo_atual,level, fumaca, iFumaca, item_gasolina_rect, bandeira
        pygame.mixer.music.stop()
        segundos_inicial = contador.segundo
        iFumaca = 0
        item_bandeira_ativo = False
        bandeira = Bandeira()
        bandeira.set_tick(5)
        iCarCinza_pos = [30,40]
        carCinzaMovendo = 'direita'
#        pygame.mixer.music.load(trilha['engines']);
#        pygame.mixer.music.play()
#        if not ( pygame.mixer.music.busy() ):
        pygame.mixer.music.load(trilha['loop']);
        pygame.mixer.music.play(-1)
        iGame =   carregarImg("mapaBordas.png", (255,194,150))
        iRanking = carregarImg("ranking.png")                                
        iGameOver = carregarImg("gameover.png")
        iPontuacao = carregarImg("mapaBordas.png")
        iCarPlayer = carregarImg("carplayer.png",-1)
        iCarCinza = carregarImg("carro_cinza.png",-1)
        iCarPlayerSprite.image = iCarPlayer
        iCarPlayerSprite.rect = iCarPlayerSprite.image.get_rect()
        item_gasolina = carregarImg("gasolina.png")
        buraco = carregarImg("buraco.png")
        iBuraco.image = buraco
        iBuraco.rect = iBuraco.image.get_rect()
        iBuraco.pos = [0,0]
        iBuraco.ativo = False
        pygame.display.update()
        
        '''cenario'''
        
        bloco1.img  = carregarImg('quarteirao01.png');
        bloco1.rect = bloco1.img.get_rect()
        bloco1.pos = [90,80]
        bloco1.rect[0] = 90
        bloco1.rect[1] = 80
        
        bloco2.img  = carregarImg('quarteirao02.png');
        bloco2.rect = bloco2.img.get_rect()
        bloco2.pos = [bloco1.pos[0] + bloco1.img.get_width( ) + 120 ,80]
        bloco2.rect[0] = bloco1.pos[0] + bloco1.img.get_width( ) + 120
        bloco2.rect[1] = 80
        
        bloco3.img  = carregarImg('quarteirao03.png');
        bloco3.rect = bloco3.img.get_rect()
        bloco3.pos = [bloco2.pos[0] + bloco2.img.get_width( ) + 120 ,80]
        bloco3.rect[0] = bloco2.pos[0] + bloco2.img.get_width( ) + 120
        bloco3.rect[1] = 80
        
        bloco4.img  = carregarImg('quarteirao04.png');
        bloco4.rect = bloco4.img.get_rect()
        bloco4.pos = [bloco3.pos[0] + bloco3.img.get_width( ) - 1 ,79]
        bloco4.rect[0] = bloco3.pos[0] + bloco3.img.get_width( ) - 1 
        bloco4.rect[1] = 80
        
        bloco5.img  = carregarImg('quarteirao05.png');
        bloco5.rect = bloco5.img.get_rect()
        bloco5.pos = [bloco4.pos[0] + bloco4.img.get_width( ) + 120 ,80]
        bloco5.rect[0] = bloco4.pos[0] + bloco4.img.get_width( ) + 120
        bloco5.rect[1] = 80
        
        bloco6.img  = carregarImg('quarteirao06.png');
        bloco6.rect = bloco6.img.get_rect()
        bloco6.pos = [90,300]
        bloco6.rect[0] = 90
        bloco6.rect[1] = 300            
        
        bloco7.img  = carregarImg('quarteirao07.png');
        bloco7.rect = bloco7.img.get_rect()
        bloco7.pos = [bloco6.pos[0] + bloco6.img.get_width( ) + 120 ,250]
        bloco7.rect[0] = bloco6.pos[0] + bloco6.img.get_width( ) + 120
        bloco7.rect[1] = 250            

        bloco8.img  = carregarImg('quarteirao08.png');
        bloco8.rect = bloco8.img.get_rect()
        bloco8.pos = [bloco7.pos[0] + bloco7.img.get_width( ) + 120 ,250]
        bloco8.rect[0] = bloco7.pos[0] + bloco7.img.get_width( ) + 120
        bloco8.rect[1] = 250              

        bloco9.img  = carregarImg('quarteirao09.png');
        bloco9.rect = bloco9.img.get_rect()
        bloco9.pos = [bloco8.pos[0] + bloco8.img.get_width( ) + 120 ,250]
        bloco9.rect[0] = bloco8.pos[0] + bloco8.img.get_width( ) + 120
        bloco9.rect[1] = 250              
          

        bloco10.img  = carregarImg('quarteirao10.png');
        bloco10.rect = bloco10.img.get_rect()
        bloco10.pos = [90,300]
        bloco10.rect[0] = 90
        bloco10.rect[1] = 300            

        bloco11.img  = carregarImg('quarteirao11.png');
        bloco11.rect = bloco11.img.get_rect()
        bloco11.pos = [bloco8.pos[0] + bloco8.img.get_width( ) + 120 ,250]
        bloco11.rect[0] = bloco8.pos[0] + bloco8.img.get_width( ) + 120
        bloco11.rect[1] = 250                

        bloco12.img  = carregarImg('quarteirao12.png');
        bloco12.rect = bloco12.img.get_rect()
        bloco12.pos = [bloco9.pos[0] + bloco9.img.get_width( ) + 120 ,250]
        bloco12.rect[0] = bloco9.pos[0] + bloco9.img.get_width( ) + 60
        bloco12.rect[1] = 250             

        bloco13.img  = carregarImg('quarteirao13.png');
        bloco13.rect = bloco13.img.get_rect()
        bloco13.pos = [90,300]
        bloco13.rect[0] = 90
        bloco13.rect[1] = 300            

        bloco14.img  = carregarImg('quarteirao14.png');
        bloco14.rect = bloco14.img.get_rect()
        bloco14.pos = [bloco9.pos[0] + bloco9.img.get_width( ) + 120 ,250]
        bloco14.rect[0] = bloco9.pos[0] + bloco9.img.get_width( ) + 60
        bloco14.rect[1] = 250            

        bloco16.img  = carregarImg('quarteirao16.png');
        bloco16.rect = bloco16.img.get_rect()
        bloco16.pos = [bloco6.pos[0] + bloco6.img.get_width( ) + 120 ,460 ]
        bloco16.rect[0] = bloco6.pos[0] + bloco6.img.get_width( ) + 120
        bloco16.rect[1] = 460
        
        bloco17.img  = carregarImg('quarteirao16.png');
        bloco17.rect = bloco17.img.get_rect()
        bloco17.pos = [bloco16.pos[0] + bloco16.img.get_width( ) + 120 ,460 ]
        bloco17.rect[0] = bloco16.pos[0] + bloco16.img.get_width( ) + 120
        bloco17.rect[1] = 460
        
        bloco18.img  = carregarImg('quarteirao18.png');
        bloco18.rect = bloco18.img.get_rect()
        bloco18.pos = [bloco17.pos[0] + bloco17.img.get_width( ) + 120 ,460 ]
        bloco18.rect[0] = bloco17.pos[0] + bloco17.img.get_width( ) + 120
        bloco18.rect[1] = 460

        bloco19.img  = carregarImg('quarteirao19.png');
        bloco19.rect = bloco19.img.get_rect()
        bloco19.pos = [bloco18.pos[0] + bloco18.img.get_width( ) + 120 ,460 ]
        bloco19.rect[0] = bloco18.pos[0] + bloco18.img.get_width( ) + 120
        bloco19.rect[1] = 460
        
        bloco20.img  = carregarImg('quarteirao20.png');
        bloco20.rect = bloco20.img.get_rect()
        bloco20.pos = [bloco19.pos[0] + bloco19.img.get_width( ) + 120 ,460 ]
        bloco20.rect[0] = bloco19.pos[0] + bloco19.img.get_width( ) + 120
        bloco20.rect[1] = 460
        
        bloco21.img  = carregarImg('quarteirao21.png');
        bloco21.rect = bloco21.img.get_rect()
        bloco21.pos = [bloco20.pos[0] + bloco20.img.get_width( ) + 120 ,460 ]
        bloco21.rect[0] = bloco20.pos[0] + bloco20.img.get_width( ) + 120
        bloco21.rect[1] = 460

        level = [ bloco1, bloco2, bloco3, bloco4, bloco5, bloco6, bloco7, \
                 bloco8, bloco9, bloco10, bloco11, bloco12,   \
                 bloco16, bloco17, bloco18 ]

        telaAtual = iGame
        PLAYING = True
        
#executa a trilha sonora
pygame.mixer.music.play(-1) 
trilha['tocando'] = True
iMenu = carregarImg("car_college.png")
telaAtual = iMenu
jogador = Jogador()
sprite_effects = []

#loop principal
while 1:
        contador.tick("cresc")
        for event in pygame.event.get():    
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if telaAtual == iMenu:
                                iMenuPrincipal = carregarImg("menu.png")      
                                if colisaoTxt(playRect):
                                        jogar()
                                      
                                if  colisaoTxt(menuRect):
                                        telaAtual = iMenuPrincipal
                                        
                        if telaAtual == iMenuPrincipal:
                                if  colisaoTxt(exitRect):
                                        telaAtual = iMenu # nao preciso carregar novamente
                                
                                if  colisaoTxt(rankingRect):
                                        telaAtual = iRanking 
                                 
                                if  colisaoTxt(regrasRect):
                                        tela_atual = "regras"     
                                           
                        if telaAtual == "gameover":
                                telaAtual = carregarImg("gameover.png")
                                if  colisaoTxt(exitRankingRect):
                                       SAINDO = True
                                       
                        if  telaAtual == "pontuacao":
                            telaAtual = carregarImg("menuBordas.png")  
                            tTamanho = width,height = 800,600
                            if ( FULLSCREEN ):
                                        tela = pygame.display.set_mode(tTamanho)
                                        FULLSCREEN = False
                            else:
                                        tela = pygame.display.set_mode(tTamanho,pygame.FULLSCREEN)
                                        FULLSCREEN = True
                            tela.blit(iRanking,(0,0)) 
                            bMenu_pos = ( 350, 485 )
                            menuRect = ( bMenu_pos[0], bMenu_pos[1] , brect[2],brect[3] )                                                     
                            tela.blit(botao,bMenu_pos)
                            carregarTxt("MENU ", 40, (255, 255, 255),  ( 460, 520, 100, 35)  )  
                            ranking_atual = ranking(jogador.Nome,jogador.Pontuacao)
                            carregarTxt("%s  %s " % (ranking_atual[0][0],ranking_atual[0][1]), 40, (0, 0, 0),  ( 412, 200, 100, 35)  )  
                            carregarTxt("%s  %s " % (ranking_atual[1][0],ranking_atual[1][1]), 40, (0, 0, 0),  ( 412, 276, 100, 35)  )  
                            carregarTxt("%s  %s " % (ranking_atual[2][0],ranking_atual[2][1]), 40, (0, 0, 0),  ( 412, 347, 100, 35)  )  
                            if  colisaoTxt(menuRankingRect):
                                        telaAtual = iMenuPrincipal # nao preciso carregar novamente
                            if  colisaoTxt(exitRankingRect):
                                       SAINDO = True    
                            pygame.display.flip()               
                        
                        if  telaAtual == "ranking":
                                telaAtual = carregarImg("ranking.png")  
                        
                        
                        if  tela_atual == "regras":
                                telaAtual = carregarImg("regras.png")
                                if  colisaoTxt(exitRect):
                                        tela_atual = ''
                                        telaAtual = iMenu # nao preciso carregar novamente        
                                carregarTxt("EXIT", 50, (255, 255, 255), exitRankingRect )
                                        
                                
                if event.type == KEYDOWN:
                        if ( event.key == K_ESCAPE or event.key == K_q ):
                                print 'saindo do jogo...'
                                SAINDO = True
                        # tecla F (fullscreen)
                        if ( event.key == K_f  ):
                                if ( FULLSCREEN ):
                                        tela = pygame.display.set_mode(tTamanho)
                                        FULLSCREEN = False
                                else:
                                        tela = pygame.display.set_mode(tTamanho,pygame.FULLSCREEN)
                                        FULLSCREEN = True
                                 
                          # tecla MUTE        
                        if ( event.key == K_s ):
                                if ( trilha['tocando'] == True ):
                                        pygame.mixer.music.pause()
                                        trilha['tocando'] = False
                                else :
                                        pygame.mixer.music.unpause()
                                        trilha['tocando'] = True
                                        
                        if PLAYING:
                             
                              '''
                                        TODO: adicionar a todos a checagem de o carro pode virar.
                              '''
                              if ( event.key == K_UP ): 
                                        if not ( carMovendo == 'colisao' and jogador.carDirecao == 'cima'):
                                                carMovendo = 'cima'
                                                if  jogador.carDirecao == 'baixo':
                                                        iCarPlayer = pygame.transform.flip(iCarPlayer, False,True)
                                                elif  jogador.carDirecao == 'direita':
                                                        if carMovendo != 'parado':
                                                                jogador.carPos[0] = jogador.carPos[0] + ( iCarPlayer.get_width( ) / 2 )
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, 90)
                                                elif ( jogador.carDirecao == 'esquerda'):
                                                        #jogador.carPos[0] = jogador.carPos[0] - iCarPlayer.get_height( )
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, -90)
                                                jogador.carDirecao = 'cima'
                                        
                              if ( event.key == K_DOWN ):
                                        if not ( carMovendo == 'colisao' and jogador.carDirecao == 'baixo'):
                                                carMovendo = 'baixo'        
                                                if  jogador.carDirecao == 'cima':
                                                        iCarPlayer = pygame.transform.flip(iCarPlayer, False,True)
                                                elif  jogador.carDirecao == 'direita':
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, -90)
                                                        if carMovendo != 'parado':
                                                                jogador.carPos[0] = jogador.carPos[0] +  ( iCarPlayer.get_height( ) / 2 )
                                                elif ( jogador.carDirecao == 'esquerda'):
                                                #        jogador.carPos[0] = jogador.carPos[0] -  iCarPlayer.get_height( )
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, 90)
                                                jogador.carDirecao = 'baixo'     
                                                                           	
                              if ( event.key == K_RIGHT ):
                                        if not ( carMovendo == 'colisao' and jogador.carDirecao == 'direita'):
                                                carMovendo = 'direita'
                                                if  jogador.carDirecao == 'esquerda':
                                                        iCarPlayer = pygame.transform.flip(iCarPlayer,True, False)
                                                elif  jogador.carDirecao == 'cima':
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, -90)
                                                elif ( jogador.carDirecao == 'baixo'):
                                                        if carMovendo != 'parado':
                                                                jogador.carPos[1] = jogador.carPos[1] +  ( iCarPlayer.get_height( ) / 2 )
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, 90)
                                                jogador.carDirecao = 'direita'
                                                
                              if ( event.key == K_LEFT ):
                                        if not ( carMovendo == 'colisao' and jogador.carDirecao == 'esquerda'):
                                                carMovendo = 'esquerda'
                                                if  jogador.carDirecao == 'direita':
                                                        iCarPlayer = pygame.transform.flip(iCarPlayer, True, False)
                                                elif  jogador.carDirecao == 'cima':
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, 90)
                                                elif ( jogador.carDirecao == 'baixo'):
                                                        if carMovendo != 'parado':
                                                                jogador.carPos[1] = jogador.carPos[1] + ( iCarPlayer.get_height( ) / 2 )
                                                        iCarPlayer = pygame.transform.rotate(iCarPlayer, -90)
                                                jogador.carDirecao = 'esquerda'
                                      
                                                          
                              if ( event.key == K_SPACE ):
                                    if  len(fumaca) < 4: # adicionar condicional para liberar a fumaca 
                                        fumaca[iFumaca] = Fumaca()
                                        fumaca[iFumaca].set_tick(5)
                                        fumaca[iFumaca].duracao = 3
                                        fumaca[iFumaca].pos = list()
                                        fumaca[iFumaca].tempo_inicial = contador.segundo
                                        sprite_effects.append(fumaca[iFumaca])
                                        iFumaca += 1
                            
                              
                                    
                                                  
        if ( SAINDO == False ):                
                tela.fill((168,168,168))
                if telaAtual == "pontuacao":
                        telaAtual = carregarImg("mapaBordas.png")
                if telaAtual == "gameover":
                        telaAtual = carregarImg("gameover.png")
                      
                tela.blit(telaAtual,[0,0])
                if ( telaAtual == iMenu ): 
                        carregarTxt("PLAY!", 50, (0, 0, 0), playRect  )
                        carregarTxt("MENU", 50, (0, 0, 0), menuRect )
        
                if ( telaAtual == iMenuPrincipal ):
                        carregarTxt("REGRAS", 40, (255, 255, 255), regrasRect )
                        carregarTxt("RANKING", 40, (255, 255, 255), rankingRect )
                        carregarTxt("GAME", 40, (255, 255, 255), gameRect )
                        carregarTxt("EXIT", 50, (255, 255, 255), exitRect )
            
                if ( tela_atual == "regras"):
                        carregarTxt("EXIT", 50, (255, 255, 255), exitRect )
            
                
                if ( telaAtual == iRanking ) or  ( telaAtual == iGameOver ):
                        carregarTxt("MENU", 50, (255, 255, 255), menuRankingRect )
                        carregarTxt("EXIT", 50, (255, 255, 255), exitRankingRect )
                
                
                if ( tela_atual == "pontuacao" ):
                        clock.tick(30)
                        carregarTxt("SEUS PONTOS: %s" % jogador.Pontuacao,  80, (255, 255, 255),  ( 300, 150, 100, 35)  )
                        txtbx.set_pos(300,200)
                        #carregarTxt("DIGITE SEU NOME: ",  40, (255, 255, 255),  ( 300, 200, 100, 35)  )
                        events = pygame.event.get() 
                        if txtbx.update(events) != False:
                            txtbx.draw(tela)
                            bMenu_pos = ( 350, 485 )
                            menuRect = ( bMenu_pos[0], bMenu_pos[1] , brect[2],brect[3] )                                                     
                            tela.blit(botao,bMenu_pos)
                            carregarTxt("MENU ", 40, (255, 255, 255),  ( 460, 520, 100, 35)  )  
                            pygame.display.flip()
                        else:
                            jogador.Nome = txtbx.value
                            telaAtual = "ranking"
                
                
                
            
                if  ( PLAYING ) :
                        carCinzaInvert =  True
                        pygame.mouse.set_visible(False)                        
                        carregarTxt("SCORE ", 40, (255, 255, 255), gamePontuacaoRect )
                        carregarTxt(str(jogador.Pontuacao), 40, (255, 255, 255), gameScoreRect )
                        carregarTxt("FUEL ", 40, (255, 255, 255), gameFuelRect )
                        jogador.Tempo = " %s : %s " % ( contador.minutoDecimal(), contador.segundoDecimal() )
                        carregarTxt(jogador.Tempo, 30, (255, 255, 255),   gameFuelPontosRect )
                        if ((jogador.carPos[0] < ( (800 - iCarPlayer.get_width( )) - telaBorda)) & ( carMovendo == 'direita' )) :
                                jogador.carPos[0] = jogador.carPos[0] + jogador.carMov
                        if ((jogador.carPos[0] > 0 + telaBorda  ) & ( carMovendo == 'esquerda' )):
                                jogador.carPos[0] = jogador.carPos[0] - jogador.carMov
                        if ((jogador.carPos[1] < (  ( 600 - iCarPlayer.get_height() ) - telaBorda)) & ( carMovendo == 'baixo')):
                                jogador.carPos[1] = jogador.carPos[1] + jogador.carMov
                        if ((jogador.carPos[1] > 0 + telaBorda ) & ( carMovendo == 'cima')):
                                jogador.carPos[1] = jogador.carPos[1] - jogador.carMov
                        
                        if ((iCarCinza_pos[0] < ( (800 - iCarCinza.get_width( )) - telaBorda)) & ( carCinzaMovendo == 'direita' )) :
                                iCarCinza_pos[0] = iCarCinza_pos[0] + jogador.carMov
                                iCarCinza_rect = ''
                                iCarCinza_rect = iCarCinza.get_rect()
                                iCarCinza_rect[0] = iCarCinza_pos[0]
                                iCarCinza_rect[1] = iCarCinza_pos[1]
                                
                        else:
                            carCinzaInvert = True
                            carCinzaMovendo = 'esquerda'

                            
                        if ((iCarCinza_pos[0] > 0 + telaBorda  ) & ( carCinzaMovendo == 'esquerda' )):
                                iCarCinza_pos[0] = iCarCinza_pos[0] - jogador.carMov
                                iCarCinza_rect = ''
                                iCarCinza_rect = iCarCinza.get_rect()
                                iCarCinza_rect[0] = iCarCinza_pos[0]
                                iCarCinza_rect[1] = iCarCinza_pos[1]
                                
                        else:
                            carCinzaMovendo = 'direita'
                            
                        if carCinzaMovendo == 'esquerda' and carCinzaInvert:
                            iCarCinza = pygame.transform.rotate(iCarCinza, -180)
                            carCinzaInvert = False
                            
                        iCarPlayerSprite.rect = iCarPlayer.get_rect()
                        iCarPlayerSprite.rect[0] = jogador.carPos[0]
                        iCarPlayerSprite.rect[1] = jogador.carPos[1]
                        
                        for bloco in level:
                            tela.blit(bloco.img,bloco.pos)
                            if iCarPlayerSprite.rect.colliderect(bloco):
                                carMovendo = 'colisao' 
                                  
                                
                        if iCarPlayerSprite.rect.colliderect(bandeira.rect):
                            item_bandeira_ativo = False
                            jogador.Pontuacao += 100
                        
                        if iCarPlayerSprite.rect.colliderect(item_gasolina_rect):
                            item_gasolina_ativo = False
                            contador.segundo += 30
                        
                        if iCarPlayerSprite.rect.colliderect(iBuraco.rect) :
                            iBuraco.image = carregarImg("explosao.png")
                            iBuraco.ativo = False
                            tela.blit(iBuraco.image,iBuraco.pos)
                            pygame.display.flip()
                            time.sleep(3)
                            iBuraco.image = carregarImg("buraco.png")
                            jogador.carPos = [350,390]
                            jogador.lives -= 1
                            if jogador.lives == 0:
                                telaAtual = "pontuacao"
                                tela_atual = "pontuacao"
                                PLAYING = False
                                
                        if iCarPlayerSprite.rect.colliderect(iCarCinza_rect):
                            iCarCinza = carregarImg("explosao.png")
                            tela.blit(iCarCinza,iCarCinza_pos)
                            pygame.display.flip()
                            time.sleep(3)
                            iCarCinza = carregarImg("carro_cinza.png")
                            jogador.carPos = [350,390]
                            jogador.lives -= 1
                            if jogador.lives == 0:
                                telaAtual = "pontuacao"
                                tela_atual = "pontuacao"
                                PLAYING = False
                        
                        
                            
                      #  if iCarPlayerSprite.rect.colliderect(bloco1)  or iCarPlayerSprite.rect.colliderect(bloco2) \
                       #     or iCarPlayerSprite.rect.colliderect(bloco3) or  iCarPlayerSprite.rect.colliderect(bloco4) \
                        #    or iCarPlayerSprite.rect.colliderect(bloco5) or iCarPlayerSprite.rect.colliderect(bloco6) \
                         #   or iCarPlayerSprite.rect.colliderect(bloco7) or iCarPlayerSprite.rect.colliderect(bloco16) \
                          #  or iCarPlayerSprite.rect.colliderect(bloco8) or iCarPlayerSprite.rect.colliderect(bloco11) \
                           # or iCarPlayerSprite.rect.colliderect(bloco9) or iCarPlayerSprite.rect.colliderect(bloco10) : 
                            
                            
                        tela.blit(iCarPlayer,jogador.carPos)
                        tela.blit(iCarCinza,iCarCinza_pos)
                        # desenhando outros elementos
                        
                        for se in sprite_effects:
                            #print se.animaIndex
                            
                            if ( se.seguir == False  ):
                                se.pos = deepcopy(jogador.carPos)
                                if jogador.carDirecao == 'cima': 
                                    se.pos[1] = se.pos[1] + ( iCarPlayer.get_height() / 2 )
                                if jogador.carDirecao == 'esquerda': 
                                    se.pos[0] = se.pos[0] + ( iCarPlayer.get_width() / 2 )
                                if jogador.carDirecao == 'direita': 
                                    se.pos[0] = se.pos[0] - ( iCarPlayer.get_width() / 2 )
                                se.seguir = True
                                
                            se.anima()
                            tela.blit(se.sprite,se.pos)
                            if DEBUG:
                                print "Atual: %s " % contador.segundo 
                                print "Inicial:  %s" %  se.tempo_inicial 
                            if ( contador.segundo == se.tempo_inicial + 5):
                                sprite_effects.remove(se)
                            
                            
                            
                        if  item_gasolina_ativo  ==  False :
                            item_posicao = random.choice(item_posicoes)
                            while ( item_posicao == bandeira.pos ):
                                item_posicao = random.choice(item_posicoes)
                            tela.blit(item_gasolina,item_posicao)
                            item_gasolina_ativo = True
                            item_gasolina_rect = item_gasolina.get_rect()
                            item_gasolina_rect[0] = item_posicao[0]
                            item_gasolina_rect[1] = item_posicao[1]
                            segundo_inicial = contador.segundo
                            
                        if  item_bandeira_ativo  ==  False :
                            bandeira.pos = random.choice(item_posicoes)
                            while ( bandeira.pos == item_posicao ):
                                bandeira.pos = random.choice(item_posicoes)
                            bandeira.rect[0] = bandeira.pos[0]
                            bandeira.rect[1] = bandeira.pos[1]
                            item_bandeira_ativo = True
                        
                        if  item_bandeira_ativo == True: 
                            bandeira.anima()
                            tela.blit(bandeira.sprite,bandeira.pos)
                        
                        if item_gasolina_ativo == True: 
                            tela.blit(item_gasolina,item_posicao)
                            
                        segundo_atual = contador.segundo
                        if segundo_atual == segundo_inicial + 20:
                            segundo_inicial = contador.segundo
                            #item_gasolina_ativo = False    
                            
                        if iBuraco.ativo == False:
                            iBuraco.pos[0] = random.randrange(30,740)
                            iBuraco.pos[1] = random.randrange(40,500)
                            iBuraco.rect[0] = iBuraco.pos[0]
                            iBuraco.rect[1] = iBuraco.pos[1]
                            for bloco in level:
                                if iBuraco.rect.colliderect(bloco):
                                    iBuraco.pos[0] = random.randrange(30,740)
                                    iBuraco.pos[1] = random.randrange(40,500)
                                    iBuraco.rect[0] = iBuraco.pos[0]
                                    iBuraco.rect[1] = iBuraco.pos[1]
                            iBuraco.ativo = True
                        else:
                            tela.blit(iBuraco.image,iBuraco.pos)
                                  
                        if DEBUG == True:
                                print iCarPlayerSprite.rect
                                print jogador.carPos
                                print carMovendo
                                print jogador.carDirecao
                else:
                        pygame.mouse.set_visible(True)        

                
                pygame.display.flip()
        else:
                pygame.quit()
                sys.exit()
