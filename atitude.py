from abc import ABC, abstractmethod

class Atitude(ABC):
    def __init__(self, nome: str):
        self.__nome = nome #

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def executar(self, jogador_usando, alvo):
        pass
