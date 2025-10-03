from abc import ABC, abstractmethod

class Entidade(ABC):

    def __init__(self, nome: str, magia: int, atk: int, defn: int):
        self.__nome = nome
        self.__magia = magia
        self.__atk = atk
        self.__defn = defn

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def magia(self):
        return self.__magia

    @magia.setter
    def magia(self, magia: int):
        self.__magia = magia

    @property
    def atk(self):
        return self.__atk

    @atk.setter
    def atk(self, atk: int):
        self.__atk = atk

    @property
    def defn(self):
        return self.__defn

    @defn.setter
    def defn(self, defn: int):
        self.__defn = defn

    @abstractmethod
    def leveidano(self, dano: int):
        pass

    @abstractmethod
    def estouvivo(self):
        pass


    def atacar(self, alvo):
        danocausado = self.__atk - alvo.defn
        if danocausado < 0:
            danocausado = 0
        alvo.leveidano(danocausado)
        print(f"{self.__nome} ataca {alvo.nome}, causando {danocausado} de dano!")
