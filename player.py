import random

# Game Class
class Game:
    WINNING_POSITIONS = [
        0b111000000, 0b000111000, 0b000000111,  # Rows
        0b100100100, 0b010010010, 0b001001001,  # Columns
        0b100010001, 0b001010100               # Diagonals
    ]
    
    def __init__(self):
        self.player1_board = 0  # Bitboard for player 1 (X)
        self.player2_board = 0  # Bitboard for player 2 (O)
        self.current_turn = 1   # Player 1 starts
    
    def is_winner(self, board):
        """Check if the given bitboard is a winning state."""
        for win in self.WINNING_POSITIONS:
            if (board & win) == win:
                return True
        return False
    
    def is_draw(self):
        """Check if the game is a draw (all spaces filled)."""
        return (self.player1_board | self.player2_board) == 0b111111111
    
    def make_move(self, position):
        """Make a move at the given position if it's valid."""
        if not self.is_valid_move(position):
            return False
        
        if self.current_turn == 1:
            self.player1_board |= (1 << position)
            if self.is_winner(self.player1_board):
                return "Player 1 wins!"
            self.current_turn = 2
        else:
            self.player2_board |= (1 << position)
            if self.is_winner(self.player2_board):
                return "Player 2 wins!"
            self.current_turn = 1
        
        if self.is_draw():
            return "It's a draw!"
        return True
    
    def is_valid_move(self, position):
        """Check if a move is valid (position is empty)."""
        return not ((self.player1_board | self.player2_board) & (1 << position))
    
    def print_board(self):
        """Print the current state of the game board."""
        board = [' ' for _ in range(9)]
        for i in range(9):
            if self.player1_board & (1 << i):
                board[i] = 'X'
            elif self.player2_board & (1 << i):
                board[i] = 'O'
        
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("--+---+--")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("--+---+--")
        print(f"{board[6]} | {board[7]} | {board[8]}")
    
    def reset(self):
        """Reset the game for a new round."""
        self.player1_board = 0
        self.player2_board = 0
        self.current_turn = 1


# Player Class
class Player:
    def __init__(self, strategy, name="Player"):
        self.strategy = strategy  # A function that decides moves
        self.name = name
    
    def make_move(self, game):
        """Select and make a move based on the player's strategy."""
        move = self.strategy(game)
        result = game.make_move(move)
        print(f"{self.name} chose position {move}")
        return result


# Strategies

# Random Strategy
def random_strategy(game):
    available_moves = [i for i in range(9) if game.is_valid_move(i)]
    return random.choice(available_moves)

# Minimax Strategy
def minimax_strategy(game):
    def minimax(is_maximizing):
        if game.is_winner(game.player1_board):
            return -1
        if game.is_winner(game.player2_board):
            return 1
        if game.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            best_moves = []
            for move in range(9):
                if game.is_valid_move(move):
                    game.player2_board |= (1 << move)  # Simulate move for maximizing player
                    score = minimax(False)
                    game.player2_board &= ~(1 << move)  # Undo move
                    if score > best_score:
                        best_score = score
                        best_moves = [move]
                    elif score == best_score:
                        best_moves.append(move)  # Add to possible best moves
            return best_moves[random.randint(0, len(best_moves) - 1)] if best_moves else None
        else:
            best_score = float('inf')
            best_moves = []
            for move in range(9):
                if game.is_valid_move(move):
                    game.player1_board |= (1 << move)  # Simulate move for minimizing player
                    score = minimax(True)
                    game.player1_board &= ~(1 << move)  # Undo move
                    if score < best_score:
                        best_score = score
                        best_moves = [move]
                    elif score == best_score:
                        best_moves.append(move)  # Add to possible best moves
            return best_moves[random.randint(0, len(best_moves) - 1)] if best_moves else None

    return minimax(True)  # Start with Player 2 (maximizing player)


# Exhaustive Search Strategy (basic)
def exhaustive_search_strategy(game):
    available_moves = [i for i in range(9) if game.is_valid_move(i)]
    return available_moves[0]  # Pick the first available move (or simulate all possibilities)

# Main Function to play the game
def play_game(player1, player2):
    game = Game()
    game.print_board()
    while True:
        if game.current_turn == 1:
            result = player1.make_move(game)
        else:
            result = player2.make_move(game)
        
        game.print_board()
        if result not in (True, None):
            print(result)
            break
def value_iteration(game, epsilon=0.01, discount_factor=0.9):
    """
    Perform value iteration for the Tic-Tac-Toe game.
    
    Parameters:
        game (Game): The Tic-Tac-Toe game instance.
        epsilon (float): Convergence threshold.
        discount_factor (float): Discount factor for future rewards.

    Returns:
        dict: A policy mapping state keys to actions.
    """
    values = {}  # State values
    # Initialize the value function for all possible states (binary representation)
    for i in range(2 ** 18):  # 18 bits: 9 for each player
        values[(i >> 9, i & 0b111111111)] = 0  # Initialize all states

    while True:
        max_change = 0  # Track the maximum change in value
        for state_key in values:
            current_value = values[state_key]
            game.player1_board, game.player2_board = state_key  # Set the game state
            
            actions = [i for i in range(9) if game.is_valid_move(i)]
            if not actions:  # If no actions are available (shouldn't happen)
                continue
            
            new_value = max(get_expected_value(game, action, values, discount_factor) for action in actions)
            values[state_key] = new_value
            max_change = max(max_change, abs(new_value - current_value))

        if max_change < epsilon:
            break  # Convergence

    # Extract the policy based on the value function
    policy = {}
    for state_key in values:
        game.player1_board, game.player2_board = state_key
        actions = [i for i in range(9) if game.is_valid_move(i)]
        if actions:
            best_action = max(actions, key=lambda action: get_expected_value(game, action, values, discount_factor))
            policy[state_key] = best_action

    return policy

def get_expected_value(game, action, values, discount_factor):
    """Calculate the expected value for a given action."""
    original_state = (game.player1_board, game.player2_board)
    
    # Simulate taking the action
    if game.current_turn == 1:
        game.player1_board |= (1 << action)  # Player 1 makes a move
    else:
        game.player2_board |= (1 << action)  # Player 2 makes a move

    reward = get_reward(game)
    next_state = (game.player1_board, game.player2_board)

    # Undo the action
    game.player1_board, game.player2_board = original_state

    return reward + discount_factor * values.get(next_state, 0)

def get_reward(game):
    """Return the reward for the current state."""
    if game.is_winner(game.player1_board):
        return -1  # Player 1 loses
    elif game.is_winner(game.player2_board):
        return 1   # Player 2 wins
    elif game.is_draw():
        return 0   # Draw
    return 0

# Test the Game
def value_iteration(game, epsilon=0.01, discount_factor=0.9):
    """
    Perform value iteration for the Tic-Tac-Toe game.
    
    Parameters:
        game (Game): The Tic-Tac-Toe game instance.
        epsilon (float): Convergence threshold.
        discount_factor (float): Discount factor for future rewards.

    Returns:
        dict: A policy mapping state keys to actions.
    """
    values = {}  # State values
    # Initialize the value function for all possible states (binary representation)
    for i in range(2 ** 18):  # 18 bits: 9 for each player
        values[(i >> 9, i & 0b111111111)] = 0  # Initialize all states

    while True:
        max_change = 0  # Track the maximum change in value
        for state_key in values:
            current_value = values[state_key]
            game.player1_board, game.player2_board = state_key  # Set the game state
            
            actions = [i for i in range(9) if game.is_valid_move(i)]
            if not actions:  # If no actions are available (shouldn't happen)
                continue
            
            new_value = max(get_expected_value(game, action, values, discount_factor) for action in actions)
            values[state_key] = new_value
            max_change = max(max_change, abs(new_value - current_value))

        if max_change < epsilon:
            break  # Convergence

    # Extract the policy based on the value function
    policy = {}
    for state_key in values:
        game.player1_board, game.player2_board = state_key
        actions = [i for i in range(9) if game.is_valid_move(i)]
        if actions:
            best_action = max(actions, key=lambda action: get_expected_value(game, action, values, discount_factor))
            policy[state_key] = best_action

    return policy

def get_expected_value(game, action, values, discount_factor):
    """Calculate the expected value for a given action."""
    original_state = (game.player1_board, game.player2_board)
    
    # Simulate taking the action
    if game.current_turn == 1:
        game.player1_board |= (1 << action)  # Player 1 makes a move
    else:
        game.player2_board |= (1 << action)  # Player 2 makes a move

    reward = get_reward(game)
    next_state = (game.player1_board, game.player2_board)

    # Undo the action
    game.player1_board, game.player2_board = original_state

    return reward + discount_factor * values.get(next_state, 0)

def get_reward(game):
    """Return the reward for the current state."""
    if game.is_winner(game.player1_board):
        return -1  # Player 1 loses
    elif game.is_winner(game.player2_board):
        return 1   # Player 2 wins
    elif game.is_draw():
        return 0   # Draw
    return 0

def test_value_iteration(policy, game):
    """Test the trained policy in a game of Tic-Tac-Toe."""
    game.reset()
    while True:
        if game.current_turn == 1:
            # Player 1's move (can be random or minimax, depending on how you want to test)
            move = random_strategy(game)
            result = game.make_move(move)
        else:
            # Player 2 uses the policy learned from value iteration
            state = (game.player1_board, game.player2_board)
            move = policy.get(state, random_strategy(game))  # Fall back to random if no policy
            result = game.make_move(move)

        game.print_board()
        if result not in (True, None):
            print(result)
            break
def policy_iteration(game, epsilon=0.01, discount_factor=0.9):
    """
    Perform policy iteration for the Tic-Tac-Toe game.
    
    Parameters:
        game (Game): The Tic-Tac-Toe game instance.
        epsilon (float): Convergence threshold for policy evaluation.
        discount_factor (float): Discount factor for future rewards.
    
    Returns:
        dict: The optimal policy mapping state keys to actions.
    """
    # Initialize a random policy and value function for each state
    policy = {}
    values = {}
    for i in range(2 ** 18):  # 18 bits: 9 for each player
        state = (i >> 9, i & 0b111111111)
        values[state] = 0  # Start with value 0 for all states
        policy[state] = random.choice([i for i in range(9)])  # Random initial policy (random move)

    # Policy iteration loop
    while True:
        # Step 1: Policy Evaluation
        while True:
            max_change = 0
            for state_key in values:
                game.player1_board, game.player2_board = state_key  # Set the game state
                action = policy[state_key]
                if not game.is_valid_move(action):  # If the policy is invalid for some reason, continue
                    continue

                current_value = values[state_key]
                new_value = get_expected_value(game, action, values, discount_factor)
                values[state_key] = new_value
                max_change = max(max_change, abs(new_value - current_value))

            if max_change < epsilon:
                break  # Policy evaluation has converged

        # Step 2: Policy Improvement
        policy_stable = True
        for state_key in values:
            game.player1_board, game.player2_board = state_key
            actions = [i for i in range(9) if game.is_valid_move(i)]
            if actions:
                best_action = max(actions, key=lambda action: get_expected_value(game, action, values, discount_factor))
                if policy[state_key] != best_action:
                    policy[state_key] = best_action
                    policy_stable = False

        if policy_stable:
            break  # If policy is stable, we have found the optimal policy

    return policy

def get_expected_value(game, action, values, discount_factor):
    """Calculate the expected value for a given action."""
    original_state = (game.player1_board, game.player2_board)
    
    # Simulate taking the action
    if game.current_turn == 1:
        game.player1_board |= (1 << action)  # Player 1 makes a move
    else:
        game.player2_board |= (1 << action)  # Player 2 makes a move

    reward = get_reward(game)
    next_state = (game.player1_board, game.player2_board)

    # Undo the action
    game.player1_board, game.player2_board = original_state

    return reward + discount_factor * values.get(next_state, 0)

def get_reward(game):
    """Return the reward for the current state."""
    if game.is_winner(game.player1_board):
        return -100  # Player 1 loses
    elif game.is_winner(game.player2_board):
        return 100  # Player 2 wins
    elif game.is_draw():
        return 0   # Draw
    return 0
def test_policy_iteration(policy, game):
    """Test the trained policy in a game of Tic-Tac-Toe."""
    game.reset()
    while True:
        if game.current_turn != 1:
            # Player 1's move (can be random or minimax, depending on how you want to test)
            move = minimax_strategy(game)
            result = game.make_move(move)
        else:
            # Player 2 uses the policy learned from policy iteration
            state = (game.player1_board, game.player2_board)
            move = policy.get(state, random_strategy(game))  # Fall back to random if no policy
            result = game.make_move(move)

        game.print_board()
        if result not in (True, None):
            print(result)
            break
def monte_carlo_strategy(game, num_simulations=1000):
    """
    Monte Carlo strategy for Tic-Tac-Toe. Simulates random games and picks the best move.
    
    Parameters:
        game (Game): The current game instance.
        num_simulations (int): The number of simulations to run for each possible move.
    
    Returns:
        int: The best move based on simulation results.
    """
    available_moves = [i for i in range(9) if game.is_valid_move(i)]
    if not available_moves:
        return None

    move_wins = {move: 0 for move in available_moves}  # To keep track of wins for each move

    # Simulate games for each available move
    for move in available_moves:
        for _ in range(num_simulations):
            sim_game = Game()
            sim_game.player1_board = game.player1_board
            sim_game.player2_board = game.player2_board
            sim_game.current_turn = game.current_turn

            # Make the current move
            sim_game.make_move(move)

            # Simulate the rest of the game randomly
            while not sim_game.is_winner(sim_game.player1_board) and not sim_game.is_winner(sim_game.player2_board) and not sim_game.is_draw():
                next_move = random_strategy(sim_game)
                sim_game.make_move(next_move)

            # If the current player wins, count it as a win for this move
            if (game.current_turn == 1 and sim_game.is_winner(sim_game.player1_board)) or (game.current_turn == 2 and sim_game.is_winner(sim_game.player2_board)):
                move_wins[move] += 1

    # Choose the move with the most wins
    best_move = max(move_wins, key=move_wins.get)
    return best_move

if __name__ == "__main__":
    game = Game()
    player1 = Player(monte_carlo_strategy, name="Player 1 (Monte Carlo)")
    player2 = Player(random_strategy, name="Player 2 (Random)")

    # Play the game
    play_game(player1, player2)
    
    # # Train the policy using policy iteration
    # print("Training policy using Policy Iteration...")
    # policy = policy_iteration(game)

    # # Test the learned policy
    # print("Testing Policy Iteration Policy...")
    # test_policy_iteration(policy, game)
 
