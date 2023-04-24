from enum import Enum

from requests_oauth2client import BearerAuth
import requests
import time

class Chess_board_pos:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def into_str(self):
        return chr(ord('a') + self.column) + str(self.row + 1)

CHESS_BOARD_MIN_INDEX = 0
CHESS_BOARD_MAX_INDEX = 7

class Color(Enum):
    WHITE = 0
    BLACK = 1

    def next(self):
        if self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE

    def into_fen(self):
        if self == Color.WHITE:
            return "w"
        else:
            return "b"
        
    def into_str(self):
        if self == Color.WHITE:
            return "white"
        else:
            return "black"
        
    @staticmethod
    def from_fen(fen):
        if fen == "w":
            return Color.WHITE
        else:
            return Color.BLACK

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

FEN_BOARD_SEPARATOR = "/"
FEN_MAIN_SEPARATOR = " "

class FEN_split_type(Enum):
    BOARD = 0
    PLAYER = 1
    CASTLING = 2
    EN_PASSANT = 3
    HALF_MOVE_CLOCK = 4
    FULL_MOVE_NUMBER = 5

class FEN_content:

    def __init__(self, fen_str):
        self.split = fen_str.split(FEN_MAIN_SEPARATOR)
        
    def into_str(self):
        return " ".join(self.split)
    
    def get(self, split_type):
        return self.split[split_type.value]
    
    def set(self, split_type, value):
        self.split[split_type.value] = value

    def get_color(self):
        return Color.from_fen(self.get(FEN_split_type.PLAYER))
    
    def set_color(self, color):
        self.set(FEN_split_type.PLAYER, color.into_fen())

    def toggle_player(self):
        self.set_color(self.get_color().next())

    def get_row(self, row):
        return self.get(FEN_split_type.BOARD).split(FEN_BOARD_SEPARATOR)[CHESS_BOARD_MAX_INDEX - row]
    
    def set_row(self, row, fen_row):
        board_split = self.get(FEN_split_type.BOARD).split(FEN_BOARD_SEPARATOR)
        board_split[CHESS_BOARD_MAX_INDEX - row] = fen_row
        self.set(FEN_split_type.BOARD, FEN_BOARD_SEPARATOR.join(board_split))

    def get_position(self, row, column):
        fen_row = self.get_row(row)
        pos_in_row = self.get_pos_in_row_str(fen_row, column)
        return fen_row[pos_in_row]
    
    def set_position(self, row, column, piece):
        fen_row = self.get_row(row)
        pos_in_row = self.get_pos_in_row_str(fen_row, column)

        current_piece = fen_row[pos_in_row]
        could_be_replaced_in_place = not current_piece.isdigit() or int(current_piece) == 1

        if could_be_replaced_in_place:
            replacment = piece
            self.set_row(row, replace_str_index(fen_row, pos_in_row, replacment))
        else:
            columns_before = self.count_columns_before_piece(fen_row, column)
            columns_needed = column - columns_before
            columns_after = int(current_piece) - columns_needed - 1
            into_space = lambda x: str(x) if x > 1 else ""
            replacment = into_space(columns_needed) + piece + into_space(columns_after)
            self.set_row(row, replace_str_index(fen_row, pos_in_row, replacment))


    def get_pos_in_row_str(self, fen_row, column):
        current_column_pos = 0
        pos_in_text = 0
        for c in fen_row:
            if current_column_pos >= column:
                return pos_in_text
            
            if c.isdigit():
                current_column_pos += int(c)
            else:
                current_column_pos += 1

            pos_in_text += 1

        return len(fen_row) - 1
    
    def count_columns_before_piece(self, row_str, column):
        current_column_pos = 0
        for c in row_str:
            current_adding = int(c) if c.isdigit() else 1

            if current_column_pos + current_adding > column:
                return current_column_pos
            
            current_column_pos += current_adding
    
        return current_column_pos
    
    def pop_piece(self, row, column):
        fen_row = self.get_row(row)
        pos_in_row = self.get_pos_in_row_str(fen_row, column)
        piece = fen_row[pos_in_row]

        count = 1
        if column > CHESS_BOARD_MIN_INDEX and fen_row[pos_in_row - 1].isdigit():
            count += int(fen_row[pos_in_row - 1])
            pos_in_row -= 1
            fen_row = replace_str_index(fen_row, pos_in_row, "")
        if column < CHESS_BOARD_MAX_INDEX and fen_row[pos_in_row + 1].isdigit():
            count += int(fen_row[pos_in_row + 1])
            fen_row = replace_str_index(fen_row, pos_in_row + 1, "")

        self.set_row(row, replace_str_index(fen_row, pos_in_row, str(count)))

        return piece


class FEN_constroller:
    @staticmethod
    def get_initial_fen():
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    @staticmethod
    def next_move(fen, move_from, move_to):
        fen = FEN_content(fen)
        fen.toggle_player()
        piece = fen.pop_piece(move_from.row, move_from.column)
        fen.set_position(move_to.row, move_to.column, piece)
        return fen.into_str()
        

class ChessGame:
    def __init__(self, player_color):
        self.current_fen = FEN_constroller.get_initial_fen()
        self.player_color = player_color
        self.current_move_player = Color.WHITE

    def update(self):
        if(self.current_move_player == self.player_color):
            self.update_player_move()
        else:
            self.update_computer_move()

    def update_player_move(self):
        pass

    def update_computer_move(self):
        pass
    
class Single_board_position_controller:
    def __init__(self):
        self.move = Chess_board_pos(0, 0)

    @staticmethod
    def from_str(move_str):
        move = Chess_board_pos(0, 0)
        move.column = ord(move_str[0]) - ord('a')
        move.row = int(move_str[1]) - 1
        return move
    
    def increase_column(self):
        self.move.column += 1

    def increase_row(self):
        self.move.row += 1

    def get(self):
        return self.move
    
class Chess_move:
    def __init__(self, move_from, move_to):
        self.move_from = move_from
        self.move_to = move_to

    def get_UCI(self):
        return self.move_from.into_str() + self.move_to.into_str()
    
class Game_data():
    def __init__(self, player_color, fen =  FEN_constroller.get_initial_fen()):
        self.level = 8
        self.color = Color.into_str(player_color)
        self.variant = "standard"
        self.fen = fen

    def into_payload(self):
        return {
            "level": self.level,
            "color": self.color,
            "variant": self.variant,
            "fen": self.fen,
        }


class Chess_lichess_game_data:
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    @staticmethod
    def from_json(json):
        return Chess_lichess_game_data(json["id"])
        

#TODO after 5 moves resign and create new game with new fen XD
class Lichess_api_controller:
    def __init__(self, token, lichess_game_data):
        self.token = token
        self.lichess_game_data = lichess_game_data

    @staticmethod
    def create_new_bot_game(game_data, token):
        url = "https://lichess.org/api/challenge/ai"

        payload = game_data.into_payload()
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload, auth=BearerAuth(token))
        return Lichess_api_controller(token, Chess_lichess_game_data.from_json(response.json()))
    
    def abandon_game(self):
        url = "https://lichess.org/api/board/game/" + self.lichess_game_data.get_id() + "/abort"
        requests.post(url, auth=BearerAuth(self.token))

    def get_moves(self):
        url = f"https://lichess.org/game/export/{self.lichess_game_data.get_id()}"
        data = requests.get(url, headers={"Accept": "application/json"})
        return data.json()["moves"].split(" ")
    
    def make_move(self, move):
        url = "https://lichess.org/api/board/game/" + self.lichess_game_data.get_id() + "/move/" + move.get_UCI()
        requests.post(url, auth=BearerAuth(self.token))
        pass


class Chess_game_controller:
    def __init__(self, token):
        self.token = token

    def new_start_game(self, color):
        self.player_color = color
        self.enemy_color = color.next()
        self.current_player = color if color == Color.WHITE else color.next()
        self.current_fen = FEN_constroller.get_initial_fen()
        self.calculated_best_move = None 

        self.lichess_controller =  Lichess_api_controller.create_new_bot_game(
            Game_data(self.enemy_color, self.current_fen), self.token
        )

        print(f"Game started - id: {self.lichess_controller.lichess_game_data.get_id()}")

    def abandon_game(self):
        if self.lichess_controller:
            self.lichess_controller.abandon_game()

    def get_current_fen(self):
        pass

    def get_current_player(self):
        pass
    
    def accept_move(self):
        self.current_player = self.current_player.next()

    def get_best_move(self):
        if self.current_player != self.player_color:
            return
        
        if self.calculated_best_move is None:
            last_move = self.lichess_controller.get_moves()[-1]
            last_move = last_move.replace("+", "")
            if not last_move[-1].isdigit():
                raise Exception("TODO")
            move_to = last_move[-2:]
    
            move_from = "a1" #TODO
            self.calculated_best_move = Chess_move(
                Single_board_position_controller.from_str(move_from),
                Single_board_position_controller.from_str(move_to)
            )
        

        return self.calculated_best_move
    
    def make_enemy_move(self, move):
        if self.current_player != self.enemy_color or not self.lichess_controller:
            return

        self.current_fen = FEN_constroller.next_move(self.current_fen, move.move_from, move.move_to)
        self.current_player = self.current_player.next()        
        self.lichess_controller.make_move(move)
        self.calculated_best_move = None

    
        

if __name__ == "__main__":
    TOKEN = 'lip_eMBV2qjns7LExky0LRCs'
    client_secrets = "eei_QPIYlTfWnRnA"

    chess_game_controller = Chess_game_controller(TOKEN)
    chess_game_controller.new_start_game(Color.WHITE)

    time.sleep(4)

    moves = chess_game_controller.lichess_controller.get_moves()
    print(moves)
    print(chess_game_controller.get_best_move().move_to.into_str())
    chess_game_controller.accept_move()

    time.sleep(4)

    move_from = Single_board_position_controller.from_str('e7')
    move_to = Single_board_position_controller.from_str('e5')
    chess_move = Chess_move(move_from, move_to)

    chess_game_controller.make_enemy_move(chess_move)

    time.sleep(4)

    moves = chess_game_controller.lichess_controller.get_moves()
    print(moves)

    print(chess_game_controller.get_best_move().move_to.into_str())
    chess_game_controller.accept_move()


    time.sleep(4)

    move = chess_game_controller.abandon_game() 