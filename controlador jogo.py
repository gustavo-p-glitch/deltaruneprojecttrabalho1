from jogador import Jogador
from menu import Menu
from batalha import Batalha
from alma import Alma
from habilidade import Habilidade
from acao import Acao
from checar import Checar
from tipo import Tipo
from efeito import Efeito
from defender import Defender
from poupar import Poupar
from item import Item


class ControladorJogo:
    def __init__(self):
        self.menu = Menu()

        # 1. CRIA OS ITENS PRIMEIRO e armazena na classe (resolve o erro de escopo)
        self.hamburguer, self.espada_de_madeira = self.criar_itens()

        # 2. CHAMA criar_jogadores PASSANDO os itens
        self.jogadores = self.criar_jogadores(self.hamburguer, self.espada_de_madeira)

    # A função agora recebe as instâncias de Item
    def criar_jogadores(self, hamburguer: Item, espada_de_madeira: Item):
        # === 1. CRIAÇÃO DE PERSONAGENS ===
        alma_kris = Alma(nome="Kris", vida=160, poder="Determinação")
        kris = Jogador(nome="Kris", magia=0, atk=20, defn=2, alma=alma_kris)

        alma_susie = Alma(nome="Susie", vida=190, poder="Brutalidade")
        susie = Jogador(nome="Susie", magia=50, atk=45, defn=25, alma=alma_susie)

        alma_ralsei = Alma(nome="Ralsei", vida=110, poder="Gentileza")
        ralsei = Jogador(nome="Ralsei", magia=150, atk=2, defn=2, alma=alma_ralsei)

        # === 2. HABILIDADES E AÇÕES ===
        tipo_ataque = Tipo(nome="Ataque Mágico", descricao="Causa dano ao inimigo.")
        tipo_gelo = Tipo(nome="Magia de Gelo", descricao="Congela o inimigo.")

        # CORRIGIDO: Usa 'valor_defesa' (resolve o TypeError: unexpected keyword argument 'aumento_defesa')
        acao_defender = Defender(valor_defesa=15, duracao=1)
        # acao_poupar = Poupar() # REMOVIDO: A função Poupar será adicionada automaticamente pela Batalha

        efeito_dano = Efeito(dano=20)
        efeito_fogo = Efeito(dano=10, fogo_dano=5, fogo_duracao=3)
        efeito_gelo = Efeito(dano=5, congelamento=True)

        rude_buster = Habilidade(nome="Rude buster", tipo=tipo_ataque, customagia=10, efeitos=efeito_dano)
        habilidade_fogo = Habilidade(nome="Fúria Flamejante", tipo=tipo_ataque, customagia=15, efeitos=efeito_fogo)
        habilidade_gelo = Habilidade(nome="Tempestade Gélida", tipo=tipo_gelo, customagia=12, efeitos=efeito_gelo)

        susie.aprenderhabilidade(rude_buster)
        ralsei.aprenderhabilidade(habilidade_fogo)
        ralsei.aprenderhabilidade(habilidade_gelo)

        # Ensina ações customizadas (Defender, Checar, Acalmar)
        for p in [kris, susie, ralsei]:
            p.aprender_acao(acao_defender)

        # REMOVIDO: As linhas p.aprender_acao(acao_poupar) foram retiradas para evitar duplicação no menu.
        # O método 'poupar' (função) será adicionado no menu de Batalha.

        # Ações específicas de Kris
        kris.aprender_acao(Checar(num=1))
        kris.aprender_acao(Acao(nome='flertar', num=2))
        kris.aprender_acao(Acao(nome="Acalmar", num=3))
        kris.aprender_acao(Acao(nome='contar piada', num=4))

        # Ações específicas de Susie/Ralsei
        susie.aprender_acao(Acao(nome="Flertar", num=2))
        ralsei.aprender_acao(Acao(nome="Acalmar", num=3))

        # REMOVIDO: Nenhuma Acao(nome='Ataque Básico') ou similar deve ser adicionada aqui,
        # pois o método 'atacar' já é adicionado em Batalha.py.

        # === 3. DISTRIBUIÇÃO DE ITENS ===
        kris.coletaritem(hamburguer)
        susie.coletaritem(hamburguer)
        ralsei.coletaritem(hamburguer)

        kris.coletaritem(espada_de_madeira)
        kris.equiparitem(espada_de_madeira)

        return [kris, susie, ralsei]

    def iniciar_jogo(self):
        inimigo_escolhido = self.menu.iniciar_menu_batalha()
        batalha = Batalha(self.jogadores, inimigo_escolhido)
        batalha.iniciar_batalha()

    def criar_itens(self):
        # --- 1. Definição dos Tipos ---
        tipo_consumivel = Tipo(nome="consumivel", descricao="Pode ser usado para curar ou dar buff em batalha.")
        tipo_equipavel = Tipo(nome="equipavel", descricao="Pode ser equipado para aumentar atributos.")

        # --- 2. Criação dos Efeitos ---
        efeito_cura_pequena = Efeito(cura=30)
        efeito_espada_basica = Efeito(aumentar_ataque=10)

        # --- 3. Criação dos Itens ---
        hamburguer = Item(nome="Hamburger", tipo=tipo_consumivel, efeitos=efeito_cura_pequena)
        espada_de_madeira = Item(nome="Espada de Madeira", tipo=tipo_equipavel, efeitos=efeito_espada_basica)

        return hamburguer, espada_de_madeira


# REMOVIDO: A chamada externa de criar_itens() foi movida para o construtor da classe.
# if __name__ == "__main__":
#     jogo = ControladorJogo()
#     jogo.iniciar_jogo()

if __name__ == "__main__":
    jogo = ControladorJogo()
    jogo.iniciar_jogo()
