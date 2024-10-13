import tictacteo as tic
import tictacteo.strategies as st


game = tic.TicTacTeoGame()

done = False

# p = input("Choose Player: ")

# if p.lower() == "x":
#     player = tic.Player.X 
# elif p.lower() == "o":
#     player = tic.Player.O
# else: 
#     raise ValueError("Ligal players: 'x' 'o' ") 

player = tic.Player(1)

x_strategy = st.ValueIterationPolicy(player= tic.Player.X)
o_strategy = st.RandomStrategy(player= tic.Player.O)

while not done:

    if player == x_strategy.player: 
        pos = x_strategy.best_move(game=game)
    else: 
        pos = o_strategy.best_move(game=game)

    done = game.step(player, pos)

    game.render()

    if done: 
        game.gui.game_over(player=player)

    player = game.next_player(player= player)