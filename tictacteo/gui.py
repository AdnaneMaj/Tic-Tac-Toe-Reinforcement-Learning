import numpy as np
from enum import Enum


class Player(Enum):
    X: int = 1
    O: int = -1


class TicTacTeoGUI:

    states: np.array
    map_repr: np.array

    def __init__(self):

        self.sep = ("+" + "-" * 3) * 3 + "+" 
        self.reset()

    def reset(self):
        self.states = np.zeros(9, dtype=np.int8)
        self.map_repr = np.full(9, "", dtype=str)


    def allowed_moves(self):
        return list(np.where(self.states==0)[0]+1)

    def play(self, player: Player, move: int):
        
        move -= 1
        if  (0 <= move <= 8):

            if self.states[move] == 0:
                self.states[move] = player.value
            else: 
                print("⛔ This moves already taken")
                print("Legal Moves:", self.allowed_moves())
        else: 
            print("\n ⛔ This Move is not Allowed \n")
            print("Legal Moves:", self.allowed_moves())

    def _impute(self, val: int, imp_val: str):
        self.map_repr[np.where(self.states == val)] = imp_val

    def is_winner(self, player: Player):

        states = self.states.copy().reshape(3, 3)

        states[states == (player.value * -1)] = 0
        states[states == player.value ] = 1

        sums = [
            states.sum(axis=0), 
            states.sum(axis=1), 
            [np.diag(states).sum(), ], 
            [np.diag(np.fliplr(states)).sum(), ]
        ]

        for sum_ in sums:
            if 3 in sum_: return True 

        return False
    
    def draw(self):
        return self.allowed_moves() == []
    
    def undo_move(self, move: int):
        self.states[move - 1] = 0


    def game_over(self, player: Player):
        print("=" * 5, "GAME OVER", "=" * 10)
        
        if self.is_winner(player=player):
            print("| player", "x" if player.value == 1 else "o", "win the game  |")
        else:
            print("| wither 'x' or 'o' win the game  |")
        
        print("=" * 26) 


    def render(self):

        map_repr = self.sep + "\n"
 
        self._impute(val= 1, imp_val= "x")
        self._impute(val= -1, imp_val= "o")
        self._impute(val= 0, imp_val= " ")

        for row in self.map_repr.reshape(3, 3):
            map_repr += "| " + " | ".join(row) + " |"
            map_repr += "\n" + self.sep + "\n"

        print(map_repr)


