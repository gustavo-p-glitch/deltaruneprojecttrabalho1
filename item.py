class Item:
    def __init__(self, nome: str, tipo: str, efeitos: dict):
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
        if self.tipo == 'consumivel':
            if 'vida' in self.efeitos:
                cura = self.efeitos['vida']
                alma.vida += cura
                print(f"O item {self.nome} foi usado! A vida da alma aumentou em {cura}.")
            else:
                print(f"O item {self.nome} não tem efeito de cura.")
        else:
            print(f"O item {self.nome} não é um item consumível.")
