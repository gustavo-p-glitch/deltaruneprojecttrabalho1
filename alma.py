from entidade import Entidade
class Alma(Entidade):
    def __init__(self, nome: str, vida: int, poder: str):
        super().__init__(nome, 0, 0, 0)
        self.__vida = vida
        self.__poder = poder

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida: int):
        self.__vida = vida

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, poder: str):
        self.__poder = poder

    def leveidano(self, dano: int):
        self.vida = self.vida - dano
        print(f"{self.nome} recebe {dano} de dano! Vida restante: {self.vida}")

    def estouvivo(self):
        if self.vida > 0:
            return True
        else:
            return False


