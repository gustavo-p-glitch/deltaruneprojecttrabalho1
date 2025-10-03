from tipo import Tipo
from efeito import Efeito

class Habilidade:
    def __init__(self, nome: str, tipo: Tipo, customagia: int, efeitos: Efeito):
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

            if self.efeitos.dano > 0:
                alvo.leveidano(self.efeitos.dano)

            if self.efeitos.cura > 0:
                alvo.vida += self.efeitos.cura
                print(f"{alvo.nome} foi curado em {self.efeitos.cura} pontos de vida!")

            if self.efeitos.aumentar_ataque > 0:
                jogadorusando.atk += self.efeitos.aumentar_ataque
                print(f"O ataque de {jogadorusando.nome} aumentou em {self.efeitos.aumentar_ataque}!")

            if self.efeitos.fogo_dano > 0 and self.efeitos.fogo_duracao > 0:
                alvo.aplicar_fogo(self.efeitos.fogo_dano, self.efeitos.fogo_duracao)

            if self.efeitos.congelamento:
                alvo.aplicar_congelamento()

        else:
            print(f"{jogadorusando.nome} não tem magia suficiente para usar {self.nome}.")
