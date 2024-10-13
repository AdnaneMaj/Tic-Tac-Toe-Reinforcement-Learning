from .gui import TicTacTeoGUI, Player


class TicTacTeoGame:

    def __init__(self) -> None:
        
        self.gui = TicTacTeoGUI()
        self.done: bool = False

    def next_player(self, player):
        return Player(player.value * -1)

    def reset(self):
        self.gui.reset()

    def step(self, player: Player, move: int):

        self.gui.play(player=player, move=move)

        self.done = self.gui.is_winner(player=player) | self.gui.draw()

        return self.done
        
    def render(self):
        self.gui.render()



