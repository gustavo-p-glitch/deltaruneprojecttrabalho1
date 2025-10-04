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
        self.rect.center = (400 // 2, 400 // 2)
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
                    if jogador.estouvivo():
                        jogador.leveidano(damage)
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
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)


import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed_x, speed_y, dano: int, pass_through=False):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 33
        self.rect.height = 33
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.dano = dano
        self.pass_through = pass_through

    def update(self, battle_box, alma=None):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if alma and self.rect.colliderect(alma.rect):
            alma.take_damage(self.dano)
            if not self.pass_through:
                self.kill()

        if not battle_box.rect.colliderect(self.rect):
            self.kill()


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

class Jogador(Entidade, pygame.sprite.Sprite):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, image, vida: int, pos=(0,0)):
        super().__init__(nome, magia, atk, defn)
        pygame.sprite.Sprite.__init__(self)
        self.__vida = vida
        self.vida_max = vida
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

    def estouvivo(self):
        return self.vida > 0

    def coletaritem(self, item):
        self.__inventario.append(item)
        print(f"{self.nome} coletou o item {item.nome}!")

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
        print(f"{self.nome} usou {nomeitem} (implementar lógica de consumível).")

    def atacar(self, alvo):
        if self.estouvivo():
            danocausado = max(0, self.atk - alvo.defn)
            alvo.leveidano(danocausado)
            print(f"{self.nome} atacou {alvo.nome}, causando {danocausado} de dano!")

    def aprenderhabilidade(self, habilidade: Habilidade):
        self.__habilidades.append(habilidade)
        print(f"{self.nome} aprendeu {habilidade.nome}!")

    def usarhabilidade(self, nomehabilidade, alvo):
        hab = next((h for h in self.__habilidades if h.nome == nomehabilidade), None)
        if hab:
            hab.usar(self, alvo)
            print(f"{self.nome} usou {nomehabilidade}!")
        else:
            print(f"{self.nome} não conhece {nomehabilidade}.")

    def aprender_acao(self, acao):
        if isinstance(acao, (Acao, Checar)) and acao not in self.__acoes:
            self.__acoes.append(acao)
            print(f"{self.nome} agora sabe {acao.nome}!")

    def usar_acao(self, nome_acao, alvo):
        act = next((a for a in self.__acoes if a.nome == nome_acao), None)
        if act:
            act.executar(self, alvo)
            print(f"{self.nome} usou {nome_acao} em {alvo.nome}.")
        else:
            print(f"{self.nome} não sabe {nome_acao}.")

    def aplicar_fogo(self, dano, duracao):
        self.fogo_dano = dano
        self.fogo_duracao = duracao
        print(f"{self.nome} está pegando fogo!")

    def aplicar_dano_fogo(self):
        if hasattr(self, 'fogo_duracao') and self.fogo_duracao > 0:
            self.levei_dano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")


import pygame
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
        if getattr(self.tipo, 'nome', '') == 'consumivel':
            mensagem = ''
            if getattr(self.efeitos, 'cura', 0) > 0:
                jogador.vida += self.efeitos.cura
                if hasattr(jogador, 'vida_max'):
                    jogador.vida = min(jogador.vida, jogador.vida_max)
                    mensagem = f"{self.nome} usado! {jogador.nome} recupera {self.efeitos.cura} de vida."
                else:
                    mensagem = f"{self.nome} não tem efeito de cura."
                return mensagem
            else:
                return f"{self.nome} não é um item consumível."


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

#nao esquecer de tirar none da imagem do jogador e colocar algo decente
import pygame
import sys
import math
from battlebox import BattleBox
from alma import Alma
from bullet import Bullet

# --- 1. SETUP CONSTANTS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

# Battle Box dimensions
box_width = 300
box_height = 200
box_x = (SCREEN_WIDTH - box_width) // 2
box_y = (SCREEN_HEIGHT - box_height + 150) // 2

# HP Bar constants
HP_BAR_X = 50
HP_BAR_Y = 550
HP_BAR_WIDTH = 250
HP_BAR_HEIGHT = 15

# Attack State variables
STATE = "ENEMY_TURN"
attack_timer = 0
ATTACK_DURATION = 1200  # 6 seconds at 60 FPS

# --- 2. INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Deltarune_project")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)
running = True

# Dummy class for player logic
class DummyJogador:
    def __init__(self):
        self.vida = 100
        self.vida_max = 100

    def estouvivo(self):
        return self.vida > 0

# --- Game objects ---
battle_box = BattleBox(box_x, box_y, box_width, box_height)
player_logic = DummyJogador()
player_sprite = Alma(player_logic)
player_sprite.rect.center = battle_box.rect.center

# Sprite Groups
all_sprites_list = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# Bullet resources
BULLET_IMAGE = 'osso.png'

# --- 3. HELPER FUNCTIONS ---
def draw_hp_bar(screen, alma, x, y, width, height):
    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    ratio = alma.current_hp / alma.max_hp if alma.max_hp > 0 else 0
    pygame.draw.rect(screen, RED, (x, y, width * ratio, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
    hp_text = FONT.render(f"HP: {alma.current_hp}/{alma.max_hp}", True, WHITE)
    screen.blit(hp_text, (x + width + 10, y))

def spawn_bullet(x, y, speed_x, speed_y, damage: int, pass_through=False):
    bullet = Bullet(x, y, BULLET_IMAGE, speed_x, speed_y, damage, pass_through)
    bullet_group.add(bullet)
    all_sprites_list.add(bullet)

def simple_shotgun_pattern(timer, box_rect):
    """Spawn 5 bullets in a fan pattern from the top-center of the battle box every second."""
    if timer % 60 == 0:
        start_x = box_rect.centerx
        start_y = box_rect.top
        speed = 3
        damage = 10
        for i in range(-2, 3):
            angle_degrees = 90 + (i * 15)
            angle_radians = math.radians(angle_degrees)
            speed_x = speed * math.cos(angle_radians)
            speed_y = speed * math.sin(angle_radians)  # positive = downward
            spawn_bullet(start_x, start_y, speed_x, speed_y, damage)

# --- 4. MAIN GAME LOOP ---
while running:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- GAME LOGIC ---
    if player_sprite.current_hp <= 0:
        STATE = "GAME_OVER"

    if STATE == "ENEMY_TURN":
        # Spawn bullets
        simple_shotgun_pattern(attack_timer, battle_box.rect)
        attack_timer += 1

        # Update player movement
        player_sprite.update(battle_box)

        # Update bullets
        for bullet in list(bullet_group):
            bullet.update(battle_box)

        # Collision detection with pass-through support
        hits = pygame.sprite.spritecollide(player_sprite, bullet_group, False)
        for bullet in hits:
            player_sprite.take_damage(bullet.dano)
            if not getattr(bullet, 'pass_through', False):
                bullet.kill()

        # End of attack phase
        if attack_timer > ATTACK_DURATION:
            STATE = "PLAYER_TURN"
            attack_timer = 0
            for bullet in list(bullet_group):
                bullet.kill()

    elif STATE == "PLAYER_TURN":
        player_sprite.update(battle_box)

    # --- DRAWING ---
    screen.fill(BLACK)
    battle_box.draw(screen)
    bullet_group.draw(screen)
    player_sprite.draw(screen)
    draw_hp_bar(screen, player_sprite, HP_BAR_X, HP_BAR_Y, HP_BAR_WIDTH, HP_BAR_HEIGHT)

    pygame.display.flip()
    clock.tick(FPS)

# --- CLEANUP ---
pygame.quit()
sys.exit()





