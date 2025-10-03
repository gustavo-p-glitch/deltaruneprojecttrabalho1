from entidade import Entidade
from alma import Alma
from habilidade import Habilidade
from acao import Acao
from checar import Checar


class Jogador(Entidade):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, alma: Alma):
        super().__init__(nome, magia, atk, defn)
        self.__alma = alma
        self.__habilidades = []
        self.__inventario = []
        self.__equipado = {}
        self.__acoes = []
        self.fogo_dano = 0
        self.fogo_duracao = 0
        self.defn_base = defn
        self.defesa_duracao = 0

    @property
    def vida(self):
        return self.__alma.vida

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

    def leveidano(self, dano: int):
        print(f"{self.nome} sente o impacto do golpe!")
        self.__alma.leveidano(dano)

    def estouvivo(self):
        return self.__alma.estouvivo()

    def coletaritem(self, item):
        self.__inventario.append(item)
        print(f"{self.nome} coletou o item {item.nome}!")

    def equiparitem(self, item):
        # CORREÇÃO: Checa item.tipo.nome e acessa item.efeitos
        if hasattr(item.tipo, 'nome') and item.tipo.nome == 'equipavel':

            bonus_atk = item.efeitos.aumentar_ataque

            if bonus_atk > 0:
                self.atk += bonus_atk
                self.__equipado['arma'] = item
                print(f"{self.nome} equipou o item {item.nome}. Ataque atual: {self.atk}.")
            else:
                print(f"{item.nome} é equipável, mas não fornece bônus de ataque.")

        else:
            print(f"{item.nome} não é um item equipável.")


    def desequiparitem(self, nomeitem):
        if nomeitem in self.__equipado:
            # Lógica de desequipar (pode ser expandida para remover bônus)
            self.__equipado.pop(nomeitem)
            print(f"{self.nome} desequipou o item {nomeitem}. Seus atributos voltaram ao normal.")
        else:
            print(f"{self.nome} não tem o item {nomeitem} equipado.")

    def usaritem(self, nomeitem):
        itemencontrado = None
        for item in self.__inventario:
            if item.nome == nomeitem:
                itemencontrado = item
                break

        if itemencontrado:
            # CORREÇÃO: Checa itemencontrado.tipo.nome
            if hasattr(itemencontrado.tipo, 'nome') and itemencontrado.tipo.nome == 'consumivel':
                itemencontrado.usarconsumivel(self.__alma)
                self.__inventario.remove(itemencontrado)

            else:
                print(f"O item {itemencontrado.nome} não pode ser usado neste momento.")
        else:
            print(f"{self.nome} não tem o item {nomeitem} no inventário.")

    def aprenderhabilidade(self, habilidade: Habilidade):
        self.__habilidades.append(habilidade)
        print(f"{self.nome} aprendeu a habilidade {habilidade.nome}!")

    def usarhabilidade(self, nomehabilidade, alvo):
        habilidadeencontrada = None
        for hab in self.__habilidades:
            if hab.nome == nomehabilidade:
                habilidadeencontrada = hab
                break

        if habilidadeencontrada:
            habilidadeencontrada.usar(self, alvo)
            print(f"{self.nome} usou a habilidade {nomehabilidade}.")
        else:
            print(f"{self.nome} não conhece a habilidade {nomehabilidade}.")

    def atacar(self, alvo):
        if self.estouvivo():
            print(f"{self.nome} ataca!")
            alvo.leveidano(self.atk - alvo.defn)

    def aprender_acao(self, acao):
        if isinstance(acao, Acao) or isinstance(acao, Checar):
            if acao not in self.__acoes:
                self.__acoes.append(acao)
                print(f"{self.nome} agora sabe {acao.nome}!")

    def usar_acao(self, nome_acao, alvo):
        acao_encontrada = None
        for act in self.__acoes:
            if act.nome == nome_acao:
                acao_encontrada = act
                break

        if acao_encontrada:
            acao_encontrada.executar(self, alvo)
            print(f"{self.nome} {nome_acao} com {alvo.nome}.")
        else:
            print(f"{self.nome} não sabe {nome_acao}.")

    def poupar(self, alvo):
        if alvo.contador == 4:
            alvo.poupado = True
            print(f'{self.nome} poupou {alvo.nome}')
        else:
            print(f'{self.nome} falhou em convencer {alvo.nome}')

    def aplicar_fogo(self, dano, duracao):
        self.fogo_dano = dano
        self.fogo_duracao = duracao
        print(f"{self.nome} está pegando fogo!")

    def aplicar_dano_fogo(self):
        if self.fogo_duracao > 0:
            self.leveidano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")

    def aplicar_dano_fogo(self):
        if self.fogo_duracao > 0:
            self.leveidano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")
