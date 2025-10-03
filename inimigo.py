from entidade import Entidade
import random


class Inimigo(Entidade):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int, lootouro: int):
        super().__init__(nome, magia, atk, defn)
        self.__vida = vida
        self.__lootouro = lootouro
        self.fogo_dano = 0
        self.fogo_duracao = 0
        self.congelado = False
        self.__num = random.randint(1, 4)
        self.__contador = 0
        self.__poupado = False

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

    def leveidano(self, dano: int):
        dano_recebido = max(0, dano)
        self.__vida -= dano_recebido
        print(f"{self.nome} recebe {dano_recebido} de dano! Vida restante: {self.__vida}")

    def estouvivo(self):
        return self.__vida > 0

    def agir(self, alvo):
        if self.estouvivo():
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
            self.leveidano(self.fogo_dano)
            self.fogo_duracao -= 1
            if self.fogo_duracao == 0:
                print(f"O fogo em {self.nome} se apagou.")

    def aplicar_congelamento(self):
        self.congelado = True
        print(f"{self.nome} foi congelado e não pode se mover!")



