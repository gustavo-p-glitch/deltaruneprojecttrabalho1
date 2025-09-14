class Habilidade:
    def __init__(self, nome: str, tipo: str, customagia: int, efeitos: dict):
        self.__nome = nome
        self.__tipo = tipo
        self.__customagia = customagia
        self.__efeitos = efeitos

    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def customagia(self):
        return self.__customagia

    @property
    def efeitos(self):
        return self.__efeitos

    def usar(self, jogadorusando, alvo):
        if jogadorusando.magia >= self.customagia:
            jogadorusando.magia -= self.customagia

            print(f"{jogadorusando.nome} usa {self.nome}!")

            if self.tipo == 'ataque' and 'dano' in self.efeitos:
                dano = self.efeitos['dano']
                alvo.leveidano(dano)
            elif self.tipo == 'cura' and 'cura' in self.efeitos:
                cura = self.efeitos['cura']
                alvo.vida += cura
                print(f"{alvo.nome} foi curado em {cura} pontos de vida!")
        else:
            print(f"{jogadorusando.nome} não tem magia suficiente para usar {self.nome}.")
