import pygame
import sys
from jogador import Jogador
from inimigo import Inimigo
from alma import Alma
from menu import MenuBatalha
from battlebox import BattleBox
from bullet import Bullet
from item import Item
from tipo import Tipo
from efeito import Efeito
from acao import Acao

def damage_target(target, damage):
    if hasattr(target, "levei_dano"):
        target.levei_dano(damage)
    elif hasattr(target, "leveidano"):
        target.leveidano(damage)
    elif hasattr(target, "take_damage"):
        target.take_damage(damage)
    else:
        if hasattr(target, "vida"):
            target.vida = max(0, target.vida - damage)

def is_alive(target):
    if hasattr(target, "estou_vivo"):
        return target.estou_vivo()
    elif hasattr(target, "estouvivo"):
        return target.estouvivo()
    elif hasattr(target, "vida"):
        return getattr(target, "vida", 0) > 0
    return True

class GameState:
    def __init__(self):
        self.turn = "player"
        self.current_player_index = 0
        self.message_log = []
        self.enemy_bullets = []
        self.battle_box_active = False

    def add_message(self, message):
        if isinstance(message, list):
            self.message_log.extend(message)
        else:
            self.message_log.append(message)
        if len(self.message_log) > 3:
            self.message_log = self.message_log[-3:]

    def next_turn(self):
        if self.turn == "player":
            self.turn = "enemy"
            self.battle_box_active = True
        else:
            self.turn = "player"
            self.current_player_index = (self.current_player_index + 1) % len(players)
            self.battle_box_active = False

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Deltarune - PyGame")
clock = pygame.time.Clock()

PIXEL_FONT = pygame.font.Font(None, 20)
TITLE_FONT = pygame.font.Font(None, 24)

BOX_W, BOX_H = 400, 200
box_x = (SCREEN_WIDTH - BOX_W) // 2
box_y = 300
BATTLE_BOX = BattleBox(box_x, box_y, BOX_W, BOX_H)

players = [
    Jogador("Kris", magia=30, atk=20, defn=5, image='kris.png', vida=100, pos=(100, 450)),
    Jogador("Susie", magia=20, atk=25, defn=8, image='susie.png', vida=120, pos=(200, 450)),
    Jogador("Ralsei", magia=40, atk=15, defn=3, image='ralsei.png', vida=80, pos=(300, 450))
]

enemies = [
    Inimigo("sans", vida=80, magia=0, atk=12, defn=2, lootouro=10, images='sans')
]

for enemy in enemies:
    enemy.rect.center = (SCREEN_WIDTH // 2, box_y - 80)

alma = Alma(jogadores=players)
alma.rect.center = (SCREEN_WIDTH // 2, box_y + BOX_H // 2)
game_state = GameState()
menu = MenuBatalha(players, enemies, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)

pocao_cura = Item("Poção de Cura", Tipo("consumivel", "Restaura HP"), Efeito(cura=30))
pocao_ataque = Item("Poção de Ataque", Tipo("consumivel", "Aumenta ataque"), Efeito(aumentar_ataque=10))

players[0].coletaritem(pocao_cura)
players[1].coletaritem(pocao_ataque)
players[2].coletaritem(pocao_cura)

acoes_disponiveis = [
    Acao("Conversar Amigavelmente", 1),
    Acao("Fazer Piada", 2),
    Acao("Dar Conselho", 3),
    Acao("Elogiar", 4)
]

for player in players:
    for acao in acoes_disponiveis:
        player.aprender_acao(acao)

def create_enemy_bullet_pattern(enemy, alma):
    bullets = []
    if enemy.nome == "sans":
        for i in range(3):
            bullet = Bullet(
                enemy.rect.centerx, enemy.rect.centery,
                'osso.png',
                speed_x=(alma.rect.centerx - enemy.rect.centerx) / 90 + (i - 1) * 1.5,
                speed_y=(alma.rect.centery - enemy.rect.centery) / 90,
                dano=enemy.atk
            )
            bullets.append(bullet)
    else:
        bullet = Bullet(
            enemy.rect.centerx, enemy.rect.centery,
            'osso.png',
            speed_x=(alma.rect.centerx - enemy.rect.centerx) / 90,
            speed_y=(alma.rect.centery - enemy.rect.centery) / 90,
            dano=enemy.atk
        )
        bullets.append(bullet)
    return bullets

running = True
while running:
    dt = clock.tick(60)
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # ALWAYS update alma, not just during enemy turn
    alma.update(BATTLE_BOX)

    if game_state.turn == "player":
        menu.update(events)
    else:
        # Update enemy bullets
        for bullet in game_state.enemy_bullets[:]:
            bullet.update(BATTLE_BOX, alma)
            if not bullet.active:
                game_state.enemy_bullets.remove(bullet)

        # Enemy attack logic
        if len(game_state.enemy_bullets) == 0:
            for enemy in enemies:
                if is_alive(enemy):
                    new_bullets = create_enemy_bullet_pattern(enemy, alma)
                    game_state.enemy_bullets.extend(new_bullets)
                    game_state.add_message(f"{enemy.nome} attacks!")
                    break
            # Don't immediately end turn - wait for bullets to finish
            # game_state.next_turn()  # REMOVED THIS LINE

    # Check if enemy turn should end (all bullets gone)
    if game_state.turn == "enemy" and len(game_state.enemy_bullets) == 0:
        # Add a small delay before ending turn
        if pygame.time.get_ticks() % 1000 < 50:  # Check every second
            game_state.next_turn()

    for enemy in enemies:
        if is_alive(enemy):
            enemy.atualizar_animacao(dt)

    screen.fill((0, 0, 0))

    if game_state.battle_box_active:
        BATTLE_BOX.draw(screen)

    for enemy in enemies:
        if is_alive(enemy):
            enemy.draw(screen)

    # ALWAYS draw alma, not just during enemy turn (for visibility)
    alma.draw(screen)

    for player in players:
        if is_alive(player):
            player.draw(screen, player.rect.x, player.rect.y)

    for bullet in game_state.enemy_bullets:
        bullet.draw(screen)

    menu.draw(screen)

    turn_text = PIXEL_FONT.render(f"Turn: {game_state.turn.upper()}", True, (255, 255, 255))
    screen.blit(turn_text, (10, 10))

    for i, message in enumerate(game_state.message_log):
        msg_surf = PIXEL_FONT.render(message, True, (255, 255, 200))
        screen.blit(msg_surf, (10, 40 + i * 25))

    pygame.display.flip()

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed_x, speed_y, dano: int, pass_through=False):
        super().__init__()
        try:
            self.image = pygame.image.load(image).convert_alpha()
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.dano = dano
        self.pass_through = pass_through
        self.active = True

    def update(self, battle_box, alma=None):
        if not self.active:
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if alma and self.rect.colliderect(alma.rect):
            alma.take_damage(self.dano)
            if not self.pass_through:
                self.active = False

        if not battle_box.rect.colliderect(self.rect):
            self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)

import pygame
from abc import ABC, abstractmethod

class Entidade(ABC, pygame.sprite.Sprite):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, image, pos=(0,0)):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.__nome = nome
        self.__magia = magia
        self.__atk = atk
        self.__defn = defn
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
    @property
    def magia(self):
        return self.__magia
    @magia.setter
    def magia(self, magia: int):
        self.__magia = magia
    @property
    def atk(self):
        return self.__atk
    @atk.setter
    def atk(self, atk: int):
        self.__atk = atk
    @property
    def defn(self):
        return self.__defn
    @defn.setter
    def defn(self, defn: int):
        self.__defn= defn
    @abstractmethod
    def levei_dano(self, dano: int):
        pass
    @abstractmethod
    def estou_vivo(self):
        pass
    def atacar(self, alvo):
        dano_causado = max(0, self.__atk - alvo.defn)
        alvo.levei_dano(dano_causado)
        print(f"{self.__nome} ataca {alvo.nome}, causando {dano_causado} de dano!")
    def draw_character(self,surface, pos):
        self.rect.center = pos
        surface.blit(self.image, self.rect)


import pygame
from entidade import Entidade
from habilidade import Habilidade
from acao import Acao
from checar import Checar
from defender import Defender
from item import Item

class Jogador(Entidade, pygame.sprite.Sprite):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, image, vida: int, pos=(0,0)):
        super().__init__(nome, magia, atk, defn, image)
        pygame.sprite.Sprite.__init__(self)
        self.__vida = vida
        self.vida_max = vida
        self.__magia_max = magia
        self.__habilidades = []
        self.__inventario = []
        self.__equipado = {}
        self.__acoes = []
        self.fogo_dano = 0
        self.fogo_duracao = 0
        self.defn_base = defn
        self.defesa_duracao = 0
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)


    @property
    def vida(self):
        return self.__vida
    @vida.setter
    def vida(self, vida: int):
        self.__vida = vida
    @property
    def habilidades(self):
        return self.__habilidades
    @property
    def inventario(self):
        return self.__inventario
    @property
    def tem_itens(self):
        return len(self.__inventario) > 0
    @property
    def acoes(self):
        return self.__acoes
    def levei_dano(self, dano: int):
        self.vida -= dano
        print(f"{self.nome} recebeu {dano} de dano! Vida atual: {self.vida}/{self.vida_max}")

    def estou_vivo(self):
        return self.vida > 0

    def coletaritem(self, item: Item):
        self.__inventario.append(item)
        print(f"{self.nome} coletou o item {item.nome}!")

    def curar(self, quantidade: int):
        self.vida += quantidade
        if self.vida > self.vida_max:
            self.vida = self.vida_max

    def equiparitem(self, item):
        if hasattr(item.tipo, 'nome') and item.tipo.nome == 'equipavel':
            bonus_atk = item.efeitos.aumentar_ataque
            if bonus_atk > 0:
                self.atk += bonus_atk
                print(f"{self.nome} equipou {item.nome}. Ataque: {self.atk}")
            else:
                print(f"{item.nome} não fornece bônus de ataque.")
        else:
            print(f"{item.nome} não é equipável.")

    def desequiparitem(self, nomeitem):
        print(f"{self.nome} desequipou {nomeitem}.")

    def usaritem(self, nomeitem):
        for item in self.__inventario:
            if item.nome == nomeitem:
                if item.tipo.nome == 'consumivel':
                    mensagens = item.usarconsumivel(self)
                    self.__inventario.remove(item)
                    return mensagens
                return [f"O item {item.nome} não pode ser usado agora."]
            return [f"{self.nome} não tem o item {nomeitem}."]

    def atacar(self, alvo):
        if self.estou_vivo():
            danocausado = max(1, self.atk - alvo.defn)
            alvo.levei_dano(danocausado)
            return [f"{self.nome} ataca {alvo.nome}, causando {danocausado} de dano!"]
        return [f"{self.nome} não pode atacar porque está fora de combate."]

    def aprender_habilidade(self, habilidade: Habilidade):
        self.__habilidades.append(habilidade)
        return f"{self.nome} aprendeu {habilidade.nome}!"

    def usar_habilidade(self, nomehabilidade, alvo):
        for hab in self.__habilidades:
            if hab.nome == nomehabilidade:
                return hab.executar(self, alvo)
        return [f"{self.nome} não conhece {nomehabilidade}."]

    def aprender_acao(self, acao):
        if isinstance(acao, (Acao, Checar, Defender)) and acao not in self.__acoes:
            self.__acoes.append(acao)
            return f"{self.nome} agora sabe {acao.nome}!"

    def usar_acao(self, nome_acao, alvo):
        for act in self.__acoes:
            if act.nome == nome_acao:
                return act.executar(self, alvo)
        return [f"{self.nome} não sabe {nome_acao}."]

    def aplicar_fogo(self, dano, duracao):
        self.fogo_dano = dano
        self.fogo_duracao = duracao
        return f"{self.nome} está em chamas!"

    def aplicar_dano_fogo(self):
        mensagens = []
        if self.fogo_duracao > 0:
            self.levei_dano(self.fogo_dano)
            mensagens.append(f"{self.nome} sofre {self.fogo_dano} de dano por queimadura!")
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                mensagens.append(f"O fogo em {self.nome} se apagou.")
        return mensagens

    def defender(self):
        self.defn += 10
        self.defesa_duracao = 1
        return [f"{self.nome} se defende! Defesa aumentada temporariamente."]

    def poupar(self, alvo):
        if hasattr(alvo, "contador") and alvo.contador >= 4:
            alvo.poupado = True
            return [f"{self.nome} poupou {alvo.nome}!"]
        return [f"{self.nome} falhou em convencer {alvo.nome}."]

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)

from atitude import Atitude

class Poupar(Atitude):
    def __init__(self):
        super().__init__("Poupar")

    def executar(self, jogador_usando, alvo, message_log=None):
        resultado = jogador_usando.poupar(alvo)
        if message_log is not None:
            message_log.add_message(resultado)
        else:
            print(resultado)


import pygame
import random
import os
from entidade import Entidade

class Inimigo(Entidade):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int, lootouro: int, images = None):
        super().__init__(nome, magia, atk, defn, 'osso.png')
        self.__vida = vida
        self.vida_max = vida
        self.__lootouro = lootouro
        self.fogo_dano = 0
        self.fogo_duracao = 0
        self.congelado = False
        self.__contador = 0
        self.__poupado = False
        self.num = random.randint(1,4)
        self.frames = []
        self.frame_indice = 0
        self.animacao_timer = 0
        self.animacao_velocidade = 120
        if images:
            self.carregar_animacao(images)
        #aq eu to carregando a primeira imagem da pasta se tiver, escrevendo pra n esquecer pq foi dificil achar essa funcao
        if self.frames:
            self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(400, 200))


    def draw(self, tela):
        if self.image:
            tela.blit(self.image, self.rect)

    def carregar_animacao(self, imagens):
        if os.path.isdir(imagens):
            for arquivo in sorted(os.listdir(imagens)):
                if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                    caminho = os.path.join(imagens, arquivo)
                    imagem = pygame.image.load(caminho).convert_alpha()
                    imagem_aumentada = pygame.transform.scale(imagem, (imagem.get_width() * 1.5, imagem.get_height() * 1.5))
                    self.frames.append(imagem_aumentada)

        if not self.frames:
            print(f"[AVISO] Nenhum frame encontrado em '{imagens}'.")

    def atualizar_animacao(self, dt):
        if not self.frames:
            return
        self.animacao_timer += dt

        if self.animacao_timer > self.animacao_velocidade:
            self.animacao_timer = 0
            self.frame_indice = (self.frame_indice + 1) % len(self.frames)
            self.image = self.frames[self.frame_indice]

    @property
    def poupado(self):
        return self.__poupado

    @poupado.setter
    def poupado(self, valor: bool):
        if isinstance(valor, bool):
            self.__poupado = valor

    @property
    def contador(self):
        return self.__contador

    @contador.setter
    def contador(self, valor: int):
        self.__contador = valor

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida: int):
        self.__vida = vida

    @property
    def lootouro(self):
        return self.__lootouro

    @lootouro.setter
    def lootouro(self, lootouro: int):
        self.__lootouro = lootouro

    def levei_dano(self, dano: int):
        dano_recebido = max(0, dano)
        self.__vida -= dano_recebido
        print(f"{self.nome} recebe {dano_recebido} de dano! Vida restante: {self.__vida}")

    def estou_vivo(self):
        return self.__vida > 0

    def agir(self, alvo):
        if self.estou_vivo():
            if self.congelado:
                print(f"{self.nome} está congelado e perdeu o turno!")
                self.congelado = False
                return

            print(f"O inimigo {self.nome} age, decidindo atacar!")
            alvo.leveidano(self.atk - alvo.defn)

    def aplicar_fogo(self, dano, duracao):
        self.fogo_dano = dano
        self.fogo_duracao = duracao
        print(f"{self.nome} está pegando fogo!")

    def aplicar_dano_fogo(self):
        if self.fogo_duracao > 0:
            self.levei_dano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")

    def aplicar_congelamento(self):
        self.congelado = True
        print(f"{self.nome} foi congelado e não pode se mover!")


import pygame
pygame.init()
pygame.mixer.init()

class Alma(pygame.sprite.Sprite):
    def __init__(self, jogadores: list):
        super().__init__()
        self.image = pygame.image.load('soul2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        self.rect.center = (400 // 2, 400 // 2)
        self.rect.width = 33
        self.rect.height = 33
        self.speed = 3
        self.jogadores = jogadores
        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 120
        self.blink_rate = 5
        self.hurt_sound = pygame.mixer.Sound("damage.mp3")
        self.hurt_sound.set_volume(0.5)

    @property
    def current_hp(self):
        return sum(player.vida for player in self.jogadores if player.estouvivo())

    @property
    def max_hp(self):
        return sum(player.vida_max for player in self.jogadores)


    def take_damage(self, damage):
            if not self.invincible:
                for jogador in self.jogadores:
                    if jogador.estou_vivo():
                        jogador.levei_dano(damage)
                self.invincible = True
                self.invincibility_timer = self.invincibility_duration
            self.hurt_sound.play()

    def draw(self, surface):
        if self.invincible:
            blink_cycle_timer = self.invincibility_duration - self.invincibility_timer
            if (blink_cycle_timer // self.blink_rate) % 2 == 0:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)



    def update(self, battle_box):
        if not any(jogador.estou_vivo() for jogador in self.jogadores):
            return
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        temp_rect = self.rect.copy()
        temp_rect.x = new_x
        temp_rect.y = new_y

        if battle_box.rect.contains(temp_rect):
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            self.rect.clamp_ip(battle_box.rect)

import pygame

class BattleBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)


import pygame
import random
import os
from entidade import Entidade

class Inimigo(Entidade):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int, lootouro: int, images = None):
        super().__init__(nome, magia, atk, defn, 'osso.png')
        self.__vida = vida
        self.vida_max = vida
        self.__lootouro = lootouro
        self.fogo_dano = 0
        self.fogo_duracao = 0
        self.congelado = False
        self.__contador = 0
        self.__poupado = False
        self.num = random.randint(1,4)
        self.frames = []
        self.frame_indice = 0
        self.animacao_timer = 0
        self.animacao_velocidade = 120
        if images:
            self.carregar_animacao(images)
        #aq eu to carregando a primeira imagem da pasta se tiver, escrevendo pra n esquecer pq foi dificil achar essa funcao
        if self.frames:
            self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(400, 200))


    def draw(self, tela):
        if self.image:
            tela.blit(self.image, self.rect)

    def carregar_animacao(self, imagens):
        if os.path.isdir(imagens):
            for arquivo in sorted(os.listdir(imagens)):
                if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                    caminho = os.path.join(imagens, arquivo)
                    imagem = pygame.image.load(caminho).convert_alpha()
                    imagem_aumentada = pygame.transform.scale(imagem, (imagem.get_width() * 1.5, imagem.get_height() * 1.5))
                    self.frames.append(imagem_aumentada)

        if not self.frames:
            print(f"[AVISO] Nenhum frame encontrado em '{imagens}'.")

    def atualizar_animacao(self, dt):
        if not self.frames:
            return
        self.animacao_timer += dt

        if self.animacao_timer > self.animacao_velocidade:
            self.animacao_timer = 0
            self.frame_indice = (self.frame_indice + 1) % len(self.frames)
            self.image = self.frames[self.frame_indice]

    @property
    def poupado(self):
        return self.__poupado

    @poupado.setter
    def poupado(self, valor: bool):
        if isinstance(valor, bool):
            self.__poupado = valor

    @property
    def contador(self):
        return self.__contador

    @contador.setter
    def contador(self, valor: int):
        self.__contador = valor

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida: int):
        self.__vida = vida

    @property
    def lootouro(self):
        return self.__lootouro

    @lootouro.setter
    def lootouro(self, lootouro: int):
        self.__lootouro = lootouro

    def levei_dano(self, dano: int):
        dano_recebido = max(0, dano)
        self.__vida -= dano_recebido
        print(f"{self.nome} recebe {dano_recebido} de dano! Vida restante: {self.__vida}")

    def estou_vivo(self):
        return self.__vida > 0

    def agir(self, alvo):
        if self.estou_vivo():
            if self.congelado:
                print(f"{self.nome} está congelado e perdeu o turno!")
                self.congelado = False
                return

            print(f"O inimigo {self.nome} age, decidindo atacar!")
            alvo.leveidano(self.atk - alvo.defn)

    def aplicar_fogo(self, dano, duracao):
        self.fogo_dano = dano
        self.fogo_duracao = duracao
        print(f"{self.nome} está pegando fogo!")

    def aplicar_dano_fogo(self):
        if self.fogo_duracao > 0:
            self.levei_dano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")

    def aplicar_congelamento(self):
        self.congelado = True
        print(f"{self.nome} foi congelado e não pode se mover!")


import pygame
from pygame.locals import *
from defender import Defender
from poupar import Poupar
from atkbarra import AtkBarra

class MenuBatalha:
    def __init__(self, jogadores, inimigos, largura, altura, game_state):
        self.jogadores = jogadores
        self.inimigos = inimigos
        self.largura = largura
        self.altura = altura
        self.game_state = game_state
        self.opcoes = ['FIGHT', 'ACT', 'ITEM', 'MERCY']
        self.opcao_selecionada = 0
        self.estado = 'menu_principal'
        self.atk_barra = None
        self.inimigo_selecionado = 0
        self.acao_selecionada = 0
        self.item_selecionado = 0

        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 24)

        try:
            self.soul_image = pygame.image.load('soul2.png').convert_alpha()
            self.soul_image = pygame.transform.scale(self.soul_image, (33, 33))
        except:
            self.soul_image = pygame.Surface((33, 33))
            self.soul_image.fill((255, 0, 0))

    def update(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if self.estado == 'menu_principal':
                    self._handle_main_menu(e)
                elif self.estado == 'submenu_acao':
                    self._handle_action_menu(e)
                elif self.estado == "submenu_item":
                    self._handle_item_menu(e)
                elif self.estado == "escolher_inimigo":
                    self._handle_enemy_select(e)
                elif self.estado == "escolher_poupar":
                    self._handle_poupar_select(e)
                elif self.estado == "ataque":
                    if self.atk_barra:
                        self.atk_barra.update(e)

        if self.atk_barra:
            self.atk_barra.tick()

    def _handle_main_menu(self, e):
        if e.key == K_w:
            self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
        elif e.key == K_s:
            self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
        elif e.key == K_a:
            self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
        elif e.key == K_d:
            self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
        elif e.key == K_k:
            opcao = self.opcoes[self.opcao_selecionada]
            if opcao == "FIGHT":
                self.estado = "escolher_inimigo"
                self.inimigo_selecionado = 0
            elif opcao == "ACT":
                self.estado = "submenu_acao"
                self.acao_selecionada = 0
            elif opcao == "ITEM":
                self.estado = "submenu_item"
                self.item_selecionado = 0
            elif opcao == "MERCY":
                self.estado = "escolher_poupar"
                self.inimigo_selecionado = 0
        elif e.key == K_l:
            pass

    def _handle_action_menu(self, e):
        current_player = self.get_current_player()
        acoes = getattr(current_player, 'acoes', [])

        if e.key == K_w:
            if acoes:
                self.acao_selecionada = (self.acao_selecionada - 1) % len(acoes)
        elif e.key == K_s:
            if acoes:
                self.acao_selecionada = (self.acao_selecionada + 1) % len(acoes)
        elif e.key == K_k:
            if acoes and self.acao_selecionada < len(acoes):
                acao = acoes[self.acao_selecionada]
                alive_enemies = [e for e in self.inimigos if e.estou_vivo()]
                if alive_enemies:
                    target = alive_enemies[0]
                    result = acao.executar(current_player, target)
                    self.game_state.add_message(result)

                    if hasattr(target, 'contador') and target.contador >= 4:
                        self.game_state.add_message(f"{target.nome} can now be SPARED!")

                    self.game_state.next_turn()
                    self.estado = "menu_principal"
        elif e.key == K_l:
            self.estado = "menu_principal"

    def _handle_item_menu(self, e):
        current_player = self.get_current_player()
        items = getattr(current_player, 'inventario', [])

        if e.key == K_w:
            if items:
                self.item_selecionado = (self.item_selecionado - 1) % len(items)
        elif e.key == K_s:
            if items:
                self.item_selecionado = (self.item_selecionado + 1) % len(items)
        elif e.key == K_k:
            if items and self.item_selecionado < len(items):
                item = items[self.item_selecionado]
                result = current_player.usaritem(item.nome)
                if isinstance(result, list):
                    self.game_state.add_message(" ".join(result))
                else:
                    self.game_state.add_message(result)
                self.game_state.next_turn()
                self.estado = "menu_principal"
        elif e.key == K_l:
            self.estado = "menu_principal"

    def _handle_enemy_select(self, e):
        alive_enemies = [e for e in self.inimigos if e.estou_vivo()]

        if e.key == K_w:
            self.inimigo_selecionado = (self.inimigo_selecionado - 1) % len(alive_enemies)
        elif e.key == K_s:
            self.inimigo_selecionado = (self.inimigo_selecionado + 1) % len(alive_enemies)
        elif e.key == K_k:
            if alive_enemies and 0 <= self.inimigo_selecionado < len(alive_enemies):
                target = alive_enemies[self.inimigo_selecionado]
                self.atk_barra = AtkBarra(self.get_current_player(), target, self, self.game_state)
                self.estado = "ataque"
        elif e.key == K_l:
            self.estado = "menu_principal"

    def _handle_poupar_select(self, e):
        alive_enemies = [e for e in self.inimigos if e.estou_vivo()]

        if e.key == K_w:
            self.inimigo_selecionado = (self.inimigo_selecionado - 1) % len(alive_enemies)
        elif e.key == K_s:
            self.inimigo_selecionado = (self.inimigo_selecionado + 1) % len(alive_enemies)
        elif e.key == K_k:
            if alive_enemies and 0 <= self.inimigo_selecionado < len(alive_enemies):
                target = alive_enemies[self.inimigo_selecionado]

                if hasattr(target, 'contador') and target.contador >= 4:
                    target.poupado = True
                    self.game_state.add_message(f"{target.nome} was SPARED!")
                    self.inimigos.remove(target)
                else:
                    self.game_state.add_message(f"{target.nome} is not ready to be spared yet! (Progress: {target.contador}/4)")

                self.game_state.next_turn()
                self.estado = "menu_principal"
        elif e.key == K_l:
            self.estado = "menu_principal"

    def get_current_player(self):
        return self.jogadores[self.game_state.current_player_index]

    def draw(self, screen):
        menu_width = 300
        menu_height = 120
        menu_x = self.largura - menu_width - 20
        menu_y = self.altura - menu_height - 20

        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (0, 0, 0), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

        if self.estado == "menu_principal":
            self._draw_main_menu(screen, menu_rect)
        elif self.estado == "escolher_inimigo":
            self._draw_enemy_selection(screen, menu_rect, "CHOOSE TARGET:")
        elif self.estado == "escolher_poupar":
            self._draw_enemy_selection(screen, menu_rect, "CHOOSE TO SPARE:")
        elif self.estado == "submenu_acao":
            self._draw_action_menu(screen, menu_rect)
        elif self.estado == "submenu_item":
            self._draw_item_menu(screen, menu_rect)
        elif self.estado == "ataque" and self.atk_barra:
            self.atk_barra.draw(screen)

    def _draw_main_menu(self, screen, menu_rect):
        for i, opcao in enumerate(self.opcoes):
            row = i // 2
            col = i % 2
            x_pos = menu_rect.x + 20 + col * 140
            y_pos = menu_rect.y + 20 + row * 40

            color = (255, 255, 255)
            text = self.font.render(opcao, True, color)
            screen.blit(text, (x_pos, y_pos))

            if i == self.opcao_selecionada:
                soul_x = x_pos - 40
                soul_y = y_pos - 5
                screen.blit(self.soul_image, (soul_x, soul_y))

    def _draw_enemy_selection(self, screen, menu_rect, title_text):
        title = self.font.render(title_text, True, (255, 255, 255))
        screen.blit(title, (menu_rect.x + 10, menu_rect.y + 10))

        alive_enemies = [e for e in self.inimigos if e.estou_vivo()]
        for i, inimigo in enumerate(alive_enemies):
            color = (255, 255, 255) if i == self.inimigo_selecionado else (255, 0, 0)
            nome = f"{inimigo.nome} (HP: {inimigo.vida}/{inimigo.vida_max})"
            if hasattr(inimigo, 'contador'):
                nome += f" [ACT: {inimigo.contador}/4]"
            text = self.font.render(nome, True, color)
            screen.blit(text, (menu_rect.x + 20, menu_rect.y + 40 + i * 25))

            if i == self.inimigo_selecionado:
                soul_x = menu_rect.x
                soul_y = menu_rect.y + 40 + i * 25 - 5
                screen.blit(self.soul_image, (soul_x, soul_y))

    def _draw_action_menu(self, screen, menu_rect):
        title = self.font.render("ACTIONS:", True, (255, 255, 255))
        screen.blit(title, (menu_rect.x + 10, menu_rect.y + 10))

        current_player = self.get_current_player()
        acoes = getattr(current_player, 'acoes', [])
        if acoes:
            for i, acao in enumerate(acoes):
                color = (255, 255, 255) if i == self.acao_selecionada else (200, 200, 200)
                text = self.font.render(acao.nome, True, color)
                screen.blit(text, (menu_rect.x + 20, menu_rect.y + 40 + i * 25))

                if i == self.acao_selecionada:
                    soul_x = menu_rect.x
                    soul_y = menu_rect.y + 40 + i * 25 - 5
                    screen.blit(self.soul_image, (soul_x, soul_y))
        else:
            text = self.font.render("No actions available", True, (200, 200, 200))
            screen.blit(text, (menu_rect.x + 20, menu_rect.y + 40))

    def _draw_item_menu(self, screen, menu_rect):
        title = self.font.render("ITEMS:", True, (255, 255, 255))
        screen.blit(title, (menu_rect.x + 10, menu_rect.y + 10))

        current_player = self.get_current_player()
        items = getattr(current_player, 'inventario', [])
        if items:
            for i, item in enumerate(items):
                color = (255, 255, 255) if i == self.item_selecionado else (200, 200, 200)
                text = self.font.render(item.nome, True, color)
                screen.blit(text, (menu_rect.x + 20, menu_rect.y + 40 + i * 25))

                if i == self.item_selecionado:
                    soul_x = menu_rect.x
                    soul_y = menu_rect.y + 40 + i * 25 - 5
                    screen.blit(self.soul_image, (soul_x, soul_y))
        else:
            text = self.font.render("No items available", True, (200, 200, 200))
            screen.blit(text, (menu_rect.x + 20, menu_rect.y + 40))

import pygame
from pygame.locals import *


class AtkBarra:
    def __init__(self, jogador, alvo, menu, game_state):
        self.jogador = jogador
        self.alvo = alvo
        self.menu = menu
        self.game_state = game_state
        self.pos_x = 100
        self.bar_y = 300
        self.speed = 8
        self.active = True
        self.bar_width = 400
        self.hit_zone = pygame.Rect(300, self.bar_y - 20, 40, 80)

    def tick(self):
        if self.active:
            self.pos_x += self.speed
            if self.pos_x > self.bar_width + 100:
                self._miss()

    def update(self, e):
        if not self.active:
            return
        if e.type == KEYDOWN and e.key == K_k:
            self._try_hit()

    def _try_hit(self):
        if self.hit_zone.left < self.pos_x < self.hit_zone.right:
            dano = self.jogador.atk
            self.game_state.add_message("perfeito")
        else:
            dano = int(self.jogador.atk * 0.5)
            self.game_state.add_message("dano fraco")

        # Use universal damage function
        if hasattr(self.alvo, 'levei_dano'):
            self.alvo.levei_dano(dano)
        elif hasattr(self.alvo, 'vida'):
            self.alvo.vida = max(0, self.alvo.vida - dano)

        self.end_attack()

    def _miss(self):
        self.game_state.add_message("errou")
        self.end_attack()

    def end_attack(self):
        self.active = False
        self.menu.estado = "menu_principal"
        self.game_state.next_turn()

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (95, self.bar_y - 10, self.bar_width + 10, 30))
        pygame.draw.rect(screen, (255, 255, 255), (100, self.bar_y, self.bar_width, 10))
        pygame.draw.rect(screen, (0, 255, 0), self.hit_zone)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos_x), self.bar_y + 5), 8)
        font = pygame.font.Font(None, 24)
        text = font.render("aperte K quando o indicador estiver no verde", True, (255, 255, 255))
        screen.blit(text, (150, self.bar_y + 30))


from abc import ABC, abstractmethod

class Atitude(ABC):
    def __init__(self, nome: str):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def executar(self, jogador_usando, alvo):
        pass
    def draw_text(self, surface, font, pos, color=(255,255,255)):
        text = font.render(self.nome, True, color)
        surface.blit(text, pos)


from atitude import Atitude
class Acao(Atitude):
    def __init__(self, nome: str, num: int):
        super().__init__(nome)
        self.__num = num

    @property
    def num(self):
        return self.__num

    def executar(self, jogador_usando, alvo):
        if hasattr(alvo, 'num') and alvo.num == self.num:
            if hasattr(alvo, 'contador'):
                alvo.contador += 1
        return f"{jogador_usando.nome} tenta convencer {alvo.nome}!"


from atitude import Atitude
class Checar(Atitude):
    def __init__(self, num: int):
        super().__init__("Checar")
        self.__num = num

    @property
    def num(self):
        return self.__num

    def executar(self, jogador_usando, alvo):
        vida_max = getattr(alvo, 'vida_max', 0)
        return (f"{jogador_usando.nome} checa {alvo.nome}: "
                f"Vida: {alvo.vida}/{vida_max}, "
                f"Magia: {alvo.magia}, "
                f"Ataque: {alvo.atk}, "
                f"Defesa: {alvo.defn}")

class Defender:
    def __init__(self, valor_defesa: int = 15, duracao: int = 1):
        self.nome = 'defender'
        self.valor_defesa = valor_defesa
        self.duracao = duracao

    def executar(self, jogador_usando):
        if not hasattr(jogador_usando, 'defn_base'):
            jogador_usando.defn_base = jogador_usando.defn

        jogador_usando.defn += self.valor_defesa
        jogador_usando.defesa_duracao = self.duracao
        return f"{jogador_usando.nome} se defende! Defesa aumentada em {self.valor_defesa} por {self.duracao} turno(s)."





from efeito import Efeito
from tipo import Tipo

class Item:
    def __init__(self, nome: str, tipo: Tipo, efeitos: Efeito):
        self.nome = nome
        self.tipo = tipo
        self.efeitos = efeitos

    def usarconsumivel(self, jogador):
        if getattr(self.tipo, 'nome', '') != 'consumivel':
            return f"{self.nome} não é um item consumível."
        mensagens = []
        if self.efeitos.cura > 0:
            jogador.vida += self.efeitos.cura
            if hasattr(jogador, 'vida_max'):
                jogador.vida = min(jogador.vida, jogador.vida_max)
            mensagens.append(f"{jogador.nome} recupera {self.efeitos.cura} de vida!")

        if self.efeitos.aumentar_ataque > 0:
            jogador.atk += self.efeitos.aumentar_ataque
            mensagens.append(f"{jogador.nome} recebe +{self.efeitos.aumentar_ataque} de ataque!")

        if self.efeitos.fogo_dano > 0 and self.efeitos.fogo_duracao > 0:
            jogador.fogo_dano = self.efeitos.fogo_dano
            jogador.fogo_duracao = self.efeitos.fogo_duracao
            mensagens.append(f"{jogador.nome} está pegando fogo por {self.efeitos.fogo_duracao} turnos!")

        if self.efeitos.congelamento:
            jogador.congelado = True
            mensagens.append(f"{jogador.nome} foi congelado!")

        return " ".join(mensagens) if mensagens else f"{self.nome} não teve efeito."


from atitude import Atitude
from efeito import Efeito
from tipo import Tipo

class Habilidade(Atitude):
    def __init__(self, nome: str, tipo: Tipo, custo_magia: int, efeitos: Efeito):
        super().__init__(nome)
        self.__tipo = tipo
        self.__custo_magia = custo_magia
        self.__efeitos = efeitos
    @property
    def tipo(self):
        return self.__tipo
    @property
    def custo_magia(self):
        return self.__custo_magia
    @property
    def efeitos(self):
        return self.__efeitos
    def executar(self, jogador_usando, alvo):
        mensagens = []
        if jogador_usando.magia >= self.custo_magia:
            jogador_usando.magia -= self.__custo_magia
            mensagens.append(f"{jogador_usando.nome} usa {self.nome}!")
            if self.__efeitos.cura > 0:
                alvo.curar(self.__efeitos.cura)
                mensagens.append(f"{alvo.nome} foi curado em {self.__efeitos.cura} pontos de vida!")

            if self.__efeitos.aumentar_ataque > 0:
                jogador_usando.atk += self.__efeitos.aumentar_ataque
                mensagens.append(f"O ataque de {jogador_usando.nome} aumentou em {self.__efeitos.aumentar_ataque}!")

            if self.__efeitos.fogo_dano > 0 and self.__efeitos.fogo_duracao > 0:
                alvo.aplicar_fogo(self.__efeitos.fogo_dano, self.__efeitos.fogo_duracao)
                mensagens.append(f"{alvo.nome} foi incendiado!")

            if self.__efeitos.congelamento:
                if hasattr(alvo, 'aplicar_congelamento'):
                    alvo.aplicar_congelamento()
                    mensagens.append(f"{alvo.nome} foi congelado!")
        else:
            mensagens.append(f"{jogador_usando.nome} não tem magia suficiente para usar {self.nome}.")
        return mensagens

class Efeito:
    def __init__(self, dano=0, cura=0, aumentar_ataque=0, aumentar_defesa=0, congelamento=False, fogo_dano=0, fogo_duracao=0):
        self.dano = dano
        self.cura = cura
        self.aumentar_ataque = aumentar_ataque
        self.aumentar_defesa = aumentar_defesa
        self.congelamento = congelamento
        self.fogo_dano = fogo_dano
        self.fogo_duracao = fogo_duracao


class Tipo:
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao




















pygame.quit()
sys.exit
