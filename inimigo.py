from entidade import Entidade
class Inimigo(Entidade):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int):
        super().__init__(nome, magia, atk, defn)
        self.__vida = vida


    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida: str):
        self.__vida = vida

    def leveidano(self, dano: int):
        self.__vida = self.__vida - dano
        print(f"{self.nome} recebe {dano} de dano! Vida restante: {self.__vida}")

    def estouvivo(self):
        if self.__vida > 0:
            return True
        else:
            return False

    def agir(self, alvo):
        if self.estouvivo():
            print(f"O inimigo {self.nome} age, decidindo atacar!")
            self.atacar(alvo)



