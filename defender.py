from atitude import Atitude


class Defender(Atitude):
    # CORREÇÃO: O argumento deve ser valor_defesa
    def __init__(self, valor_defesa: int = 15, duracao: int = 1):
        super().__init__("Defender")
        self.__valor_defesa = valor_defesa
        self.__duracao = duracao

    # O método executar deve aceitar 'alvo', mesmo que não o use.
    def executar(self, jogador_usando, alvo=None):
        if not hasattr(jogador_usando, 'defn_base'):
            jogador_usando.defn_base = jogador_usando.defn

        jogador_usando.defn += self.__valor_defesa
        jogador_usando.defesa_duracao = self.__duracao

        print(
            f'{jogador_usando.nome} se defende! Defesa aumentada em {self.__valor_defesa} por {self.__duracao} turno(s).')
