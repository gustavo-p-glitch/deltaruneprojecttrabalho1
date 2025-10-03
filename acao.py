from atitude import Atitude

class Acao(Atitude):
    def __init__(self, nome: str, num: int):
        super().__init__(nome)
        self.__num = num

    @property
    def num(self):
        return self.__num

    def executar(self, jogador_usando, alvo):
        if alvo.num == self.num:
            # Garante que o inimigo tenha o atributo contador
            if hasattr(alvo, 'contador'):
                alvo.contador += 1
            print(f'{jogador_usando.nome} tenta convencer {alvo.nome}')
