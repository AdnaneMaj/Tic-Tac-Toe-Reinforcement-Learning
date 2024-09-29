import numpy as np
from enum import Enum


class XOChoice(Enum):
    X: int = 1
    O: int = -1


class XOGame:

    states: np.array
    map_repr: np.array

    def __init__(self):

        self.sep = ("+" + "-" * 3) * 3 + "+" 
        self.reset()

    def reset(self):
        self.states = np.zeros(9, dtype=np.int8)
        self.map_repr = np.full(9, "", dtype=str)

    def play(self, choice: XOChoice, pos: int):
        
        pos -= 1
        if  0 <= pos <= 8:

            if self.states[pos] == 0:
                self.states[pos] = choice.value
        else: 
            print("\n ⛔ This Move is not Allowed\n")

        print("Legal Moves:", list(np.where(self.states==0)[0]+1))

    def _impute(self, val: int, imp_val: str):
        self.map_repr[np.where(self.states == val)] = imp_val

    def check_winner(self, player: int):

        states = self.states.copy().reshape(3, 3)

        states[states == (player * -1)] = 0
        states[states == player] = 1

        sums = [
            states.sum(axis=0), 
            states.sum(axis=1), 
            [np.diag(states).sum(), ], 
            [np.diag(np.fliplr(states)).sum(), ]
        ]

        for sum_ in sums:
            if 3 in sum_: return True 

        return False


    def render(self):

        map_repr = self.sep + "\n"
 
        self._impute(val= 1, imp_val= "x")
        self._impute(val= -1, imp_val= "o")
        self._impute(val= 0, imp_val= " ")

        for row in self.map_repr.reshape(3, 3):
            map_repr += "| " + " | ".join(row) + " |"
            map_repr += "\n" + self.sep + "\n"

        print(map_repr)


