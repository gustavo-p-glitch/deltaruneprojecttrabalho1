from entidade import Entidade
from alma import Alma
from habilidade import Habilidade
class Jogador(Entidade):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, alma: Alma):
        super().__init__(nome, magia, atk, defn)
        self.__alma = alma
        self.__habilidades = []
        self.__inventario = []
        self.__equipado = {}
    @property
    def vida(self):
        return self.__alma.vida
    @property
    def habilidades(self):
        return self.__habilidades


    def leveidano(self, dano: int):
        print(f"{self.nome} sente o impacto do golpe!")
        self.__alma.leveidano(dano)

    def estouvivo(self):
        return self.__alma.estouvivo()

    def coletaritem(self, item):
        self.__inventario.append(item)
        print(f"{self.nome} coletou o item {item.nome}!")

    def equiparitem(self, item):
        if item.tipo == 'equipavel':
            if 'arma' in self.__equipado and self.__equipado['arma'] == item:
                print(f"{self.nome} já está com {item.nome} equipado.")
                return


            self.atk += item.valor_efeito
            self.__equipado['arma'] = item
            print(f"{self.nome} equipou o item {item.nome}. Ataque atual: {self.atk}.")
        else:
            print(f"{item.nome} não é um item equipável.")

    def desequiparitem(self, nomeitem):
        if nomeitem in self.__equipado:
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
            if itemencontrado.tipo == 'consumivel':
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






