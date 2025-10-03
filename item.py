from efeito import Efeito
from tipo import Tipo

class Item:
    def __init__(self, nome: str, tipo: Tipo, efeitos: Efeito):
        self.__nome = nome
        self.__tipo = tipo
        self.__efeitos = efeitos

    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def efeitos(self):
        return self.__efeitos

    def usarconsumivel(self, alma):
        # CORREÇÃO: Usa self.tipo.nome
        if self.tipo.nome == 'consumivel':
            if self.efeitos.cura > 0:
                alma.vida += self.efeitos.cura
                print(f"O item {self.nome} foi usado! A vida da alma aumentou em {self.efeitos.cura}.")
            else:
                print(f"O item {self.nome} não tem efeito de cura.")
        else:
            print(f"O item {self.nome} não é um item consumível.")
