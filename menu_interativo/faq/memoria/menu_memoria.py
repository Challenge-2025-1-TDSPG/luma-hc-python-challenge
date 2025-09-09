"""
Operações de perguntas em memória do FAQ.
"""

class MenuMemoria:
    def __init__(self, perguntas_memoria):
        self.perguntas_memoria = perguntas_memoria

    def listar_perguntas_memoria(self):
        if not self.perguntas_memoria:
            print('Nenhuma pergunta em memória.')
        else:
            for p in self.perguntas_memoria:
                print(f'ID: {p["id"]} | Pergunta: {p["pergunta"]}')
            print(f'Total em memória: {len(self.perguntas_memoria)}')
