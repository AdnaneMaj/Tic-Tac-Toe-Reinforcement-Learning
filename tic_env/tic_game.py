from enum import Enum 


class PlayerId(Enum):
    X: int = 1
    O: int = -1 


class State:

    WIN_STATES_LIST = [
            0b000000111, 0b000111000, 0b111000000,  # rows
            0b001001001, 0b010010010, 0b100100100,  # columns
            0b100010001, 0b001010100  # diagonals
        ]

    def __init__(self, state: int):
        self._state: int = state 

    def set(self, state: int):
        self._state = state 

    def get(self) -> int:
        return self._state 
    
    @staticmethod
    def reset():
        return State(state= 0b000000000)
    
    @staticmethod
    def draw_state():
        return State(state=0b111111111)

    @classmethod
    def win_states(cls):
        return list(map(lambda state: State(state=state), cls.WIN_STATES_LIST))

    def __repr__(self):
        return f"<state: id={self._state}>"


class Player:

    def __init__(self, id: PlayerId, state: State):

        self.state: State = state 
        self.id: PlayerId = id

    def move(self, action: int):
        action -= 1
        self.state = State(state= (self.state.get() | (1 << action)))

    def __repr__(self):
        return f"<Player: id={self.id}>"


class BoardState:

    def __init__(self, players: list[Player]):
        
        self.players: list[Player] = players

    def get_state(self, ):
        return State(state= (self.players[0].state.get() | self.players[1].state.get()))

    def allowed_actions(self):

        return [
            (action + 1) for action in range(0, 9) 
            if ((1 << action) & self.get_state().get() == State.reset().get())        
        ]


class TicTacToeGame:

    def __init__(self, cur_player_id: PlayerId = None):
        
        self.cur_player_id: PlayerId = PlayerId.X if cur_player_id == None else cur_player_id

        self.reset()

    def reset(self):

        self.players: list[Player] = [
            Player(
                id= PlayerId.X, state= State.reset()
            ),
            Player(
                id= PlayerId.O, state= State.reset()
            )
        ]

        self.board_state: BoardState = BoardState(players=self.players) 

    @property
    def cur_player(self) -> Player:
        return self.players[(self.cur_player_id.value + 1)//2]

    def change_player(self):
        self.cur_player_id = PlayerId(self.cur_player_id.value * -1)

    def is_winner(self, player: Player):
        for win in State.win_states():
            if (player.state.get() & win.get()) == win.get():
                return True
        return False

    def is_draw(self, board_state: BoardState):
        return board_state.get_state().get() == State.draw_state().get() 

    def get_reward(self):

        if self.is_winner(player=self.players[0]): # X wins
            return 1

        elif self.is_winner(player=self.players[1]): # O wins
            return -1
        
        else: return 0

    def is_done(self):

        return (
            any(self.is_winner(player) for player in self.players) or self.is_draw(self.board_state)
        )

    def get_allowed_actions(self):
        return self.board_state.allowed_actions()


    def render(self):
        # TODO: change this implimentation it's weird.

        board = {}
        for i in range(1, 10):
            if (self.players[0].state.get() & (1 << (i-1))) == (1 << (i-1)):
                board[i] = " X "
            elif (self.players[1].state.get() & (1 << (i-1))) == (1 << (i-1)):
                board[i] = " O "
            else:
                board[i] = f"   "
        
        map_repr = ""
        line = "+---+---+---+\n"
        map_repr += line
        for i in range(3):
            map_repr += f"|{board[3*i+1]}|{board[3*i+2]}|{board[3*i+3]}|\n"
            map_repr += line
        print(map_repr)