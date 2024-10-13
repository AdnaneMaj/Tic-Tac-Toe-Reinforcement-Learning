import tictacteo as tic
import numpy as np
from abc import ABC, abstractmethod

class Strategy(ABC):

    def __init__(self, player: tic.Player):
        self.player = player

    @abstractmethod
    def best_move(self, game: tic.TicTacTeoGame):
        pass


class RandomStrategy(Strategy):

    def best_move(self, game: tic.TicTacTeoGame):
        return np.random.choice(a=game.gui.allowed_moves())



class MiniMaxStrategy(Strategy):

    def best_move(self, game: tic.TicTacTeoGame) -> int:
        best_score = float('-inf')
        best_move = None
        
        for move in game.gui.allowed_moves():
        
            game.gui.play(self.player, move)
            
            score = self._minimax(game, 0, False)
            
            game.gui.undo_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _minimax(self, game: tic.TicTacTeoGame, depth: int, is_maximizing: bool) -> int:
        
        if game.gui.is_winner(self.player):
            return 1
        elif game.gui.is_winner(game.next_player(self.player)):
            return -1
        elif game.gui.draw():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            player = self.player
        else:
            best_score = float('inf')
            player = game.next_player(self.player)
        
        for move in game.gui.allowed_moves():
            
            game.gui.play(player, move)
            
            score = self._minimax(game, depth + 1, not is_maximizing)
            
            game.gui.undo_move(move)
            
            if is_maximizing:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)
        
        return best_score



class ValueIterationPolicy(Strategy):

    def __init__(self, player: tic.Player):
        super(ValueIterationPolicy, self).__init__(player=player)



        
