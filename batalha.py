from jogador import Jogador
from inimigo import Inimigo
from interfacebatalha import InterfaceBatalha
from habilidade import Habilidade
from atitude import Atitude
from acao import Acao
from checar import Checar
from defender import Defender
from poupar import Poupar


class Batalha:
    def __init__(self, jogadores: list[Jogador], inimigo: Inimigo):
        self.jogadores = jogadores
        self.inimigo = inimigo
        # A interface precisa da lista para mostrar o status de todos
        self.interface = InterfaceBatalha(jogadores, inimigo)
        self.turno_atual = 1

        # CORREÇÃO 1: Inicializa defn_base e defesa_duracao para CADA jogador
        # Isso resolve Attribute Error: 'list' object has no attribute 'defn'
        for jogador_item in self.jogadores:
            if not hasattr(jogador_item, 'defn_base'):
                jogador_item.defn_base = jogador_item.defn
            if not hasattr(jogador_item, 'defesa_duracao'):
                jogador_item.defesa_duracao = 0

    def iniciar_batalha(self):
        print("=" * 60)
        print(f"!!! UMA BATALHA CONTRA {self.inimigo.nome.upper()} COMEÇOU !!!")
        print("=" * 60)

        # CORREÇÃO 2: Usa 'any' para checar se algum jogador na lista está vivo
        # Isso resolve Attribute Error: 'list' object has no attribute 'estouvivo'
        while any(p.estouvivo() for p in self.jogadores) and self.inimigo.estouvivo() and not self.inimigo.poupado:
            print(f"\n--- TURNO {self.turno_atual} ---")

            self.aplicar_efeitos_passivos()
            if not self.inimigo.estouvivo() or self.inimigo.poupado: break

            # Loop para dar o turno a CADA jogador
            for jogador_atual in self.jogadores:
                if jogador_atual.estouvivo() and self.inimigo.estouvivo() and not self.inimigo.poupado:
                    self.turnojogador(jogador_atual)

            if not self.inimigo.estouvivo() or self.inimigo.poupado: break

            self.turnoinimigo()
            if not any(p.estouvivo() for p in self.jogadores): break

            self.reduzir_duracao_status()
            self.turno_atual += 1

        self.fimbatalha()

    # Método stub para aplicar_efeitos_passivos (necessário para a classe rodar)
    def aplicar_efeitos_passivos(self):
        # Lógica de fogo para o inimigo (do inimigo.py)
        if self.inimigo.fogo_duracao > 0:
            self.inimigo.aplicar_dano_fogo()

        # Lógica de fogo para os jogadores (do jogador.py)
        for jogador in self.jogadores:
            if jogador.fogo_duracao > 0:
                jogador.aplicar_dano_fogo()

    def reduzir_duracao_status(self):
        # Lógica de buff de Defesa para TODOS os jogadores
        for jogador in self.jogadores:
            # Reduz a duração do Fogo
            if jogador.fogo_duracao > 0:
                jogador.fogo_duracao -= 1
                # Não precisa de lógica extra aqui se jogador.aplicar_dano_fogo() já trata o final

            # Reduz a duração da Defesa
            if hasattr(jogador, 'defesa_duracao') and jogador.defesa_duracao > 0:
                jogador.defesa_duracao -= 1

                if jogador.defesa_duracao == 0:
                    if hasattr(jogador, 'defn_base'):
                        jogador.defn = jogador.defn_base
                        print(f"[Status] A defesa de {jogador.nome} voltou ao normal.")

    def turnojogador(self, jogador: Jogador):

        while True:
            self.interface.mostrar_status()

            # CORREÇÃO CRÍTICA DO MENU: Adiciona as funções (atacar e poupar) e DEPOIS as classes
            # Se você removeu as classes Poupar e Acao(nome='Ataque Básico') do ControladorJogo,
            # o menu estará correto aqui.
            acoes_base = [jogador.atacar, jogador.poupar] + jogador.habilidades + jogador.acoes

            escolha_str = self.interface.mostrar_opcoes_jogador(jogador, acoes_base)

            try:
                escolha_int = int(escolha_str)

                # 1. Opção de Item
                indice_item = len(acoes_base) + 1
                if escolha_int == indice_item and jogador.tem_itens:
                    turno_gasto = self.executar_acao_item(jogador)
                    if turno_gasto:
                        break
                    else:
                        continue

                        # 2. Executar Ação Base (Ataque, Poupar, Habilidade ou Atitude)
                indice_acao = escolha_int - 1
                if 0 <= indice_acao < len(acoes_base):
                    acao_escolhida = acoes_base[indice_acao]

                    # Checa se é uma função (Ataque Básico ou Poupar)
                    if callable(acao_escolhida):
                        # As funções de Jogador (atacar e poupar) esperam o alvo
                        acao_escolhida(self.inimigo)

                    # Checa se é uma Habilidade ou Ação/Atitude
                    elif isinstance(acao_escolhida, Habilidade):
                        if jogador.magia >= acao_escolhida.customagia:
                            acao_escolhida.usar(jogador, self.inimigo)
                        else:
                            print(f"{jogador.nome} não tem magia suficiente para usar {acao_escolhida.nome}.")
                            continue
                    elif isinstance(acao_escolhida, Atitude):
                        acao_escolhida.executar(jogador, self.inimigo)

                    break
                else:
                    print("Escolha inválida. Tente novamente.")
                    continue

            except ValueError:
                print("Entrada inválida. Digite um número.")
                continue

    def executar_acao_item(self, jogador):
        # Assumindo que este método está correto e retorna True se gastar turno
        item_escolhido, tipo_nome = self.interface.mostrar_menu_inventario(jogador)

        if item_escolhido is None:
            return False

        if tipo_nome == 'consumivel':
            jogador.usaritem(item_escolhido.nome)
            return True
        elif tipo_nome == 'equipavel':
            jogador.equiparitem(item_escolhido)
            return True
        else:
            print("Tipo de item desconhecido. Ação cancelada.")
            return False

    def turnoinimigo(self):
        print("\n--- É o turno do inimigo! ---")
        # Inimigo ataca o primeiro jogador vivo que encontrar
        alvo_vivo = next((p for p in self.jogadores if p.estouvivo()), None)
        if alvo_vivo:
            self.inimigo.agir(alvo_vivo)

    def fimbatalha(self):
        print("\n--- A batalha terminou! ---")
        if self.inimigo.poupado:
            print(f"{self.inimigo.nome} foi poupado! Não houve derramamento de sangue.")
        elif any(p.estouvivo() for p in self.jogadores):
            print(f"Vitória! O grupo derrotou {self.inimigo.nome}!")
        else:
            print(f"Derrota! O grupo foi derrotado.")
