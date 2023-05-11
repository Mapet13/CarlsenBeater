import requests
import time
import json

class Chess_board_pos:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def into_str(self):
        return chr(ord('a') + self.column) + str(self.row + 1)
    
    def __eq__(self, __value: object) -> bool:
        return self.row == __value.row and self.column == __value.column
    
    def __str__(self) -> str:
        return self.into_str()
    
    def __repr__(self) -> str:
        return self.into_str()
    
    @staticmethod
    def from_str(str):
        return Chess_board_pos(int(str[1]) - 1, ord(str[0]) - ord('a'))

CHESS_BOARD_MIN_INDEX = 0
CHESS_BOARD_MAX_INDEX = 7

class Color:
    WHITE = 0
    BLACK = 1

    @staticmethod
    def next(color):
        if color == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE

    @staticmethod
    def into_fen(color):
        if color == Color.WHITE:
            return "w"
        else:
            return "b"
        
    @staticmethod
    def into_str(color):
        if color == Color.WHITE:
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

class FEN_split_type:
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
        return self.split[split_type]
    
    def set(self, split_type, value):
        self.split[split_type] = value

    def get_rows(self):
        return self.get(FEN_split_type.BOARD).split(FEN_BOARD_SEPARATOR)       
    
    def get_color(self):
        return Color.from_fen(self.get(FEN_split_type.PLAYER))
    
    def set_color(self, color):
        self.set(FEN_split_type.PLAYER, Color.into_fen(color))

    def toggle_player(self):
        self.set_color(Color.next(self.get_color()))

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
            into_space = lambda x: str(x) if x >= 1 else ""
            replacment = into_space(columns_needed) + piece + into_space(columns_after)
            self.set_row(row, replace_str_index(fen_row, pos_in_row, replacment))


    def get_pos_in_row_str(self, fen_row, column):
        pos = CHESS_BOARD_MIN_INDEX

        for id, c in enumerate(fen_row):
            pos += int(c) if c.isdigit() else 1

            if pos > column:
                return id

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
    
    @staticmethod
    def get_diff_move(prev_fen, next_fen): 
        prev_fen = FEN_content(prev_fen)
        next_fen = FEN_content(next_fen)

        diffs = []
        for row in range(CHESS_BOARD_MAX_INDEX + 1):
            for column in range(CHESS_BOARD_MAX_INDEX + 1):
                pos_prev = prev_fen.get_position(row, column)
                pos_next = next_fen.get_position(row, column)
                if pos_prev != pos_next and not (pos_prev.isdigit() and pos_next.isdigit()):
                    diffs.append((Chess_board_pos(row, column), pos_prev, pos_next))

        SIMPLE_MOVE_DIFFS_COUNT = 2
        CATLING_MOVE_DIFFS_COUNT = 4
        EN_PASSANT_MOVE_DIFFS_COUNT = 3

        color_in_move = prev_fen.get_color()

        if len(diffs) == SIMPLE_MOVE_DIFFS_COUNT:
            first_pos, first_prev, first_next = diffs[0]
            second_pos, second_prev, second_next = diffs[1]

            if first_prev.isdigit():
                return Chess_move(second_pos, first_pos)
            if first_prev == second_next and first_next == second_prev or second_prev.isdigit():
                return Chess_move(first_pos, second_pos)
            else:
                if color_in_move == Color.WHITE and first_prev.isupper() or color_in_move == Color.BLACK and first_prev.islower():
                    return Chess_move(first_pos, second_pos)
                else:
                    return Chess_move(second_pos, first_pos)
        elif len(diffs) == CATLING_MOVE_DIFFS_COUNT:
            KING_SIGN = "K"
            first_pos = None
            second_pos = None
            for pos, prev, next in diffs:
                if prev.upper() == KING_SIGN:
                    first_pos = pos
                elif next.upper() == KING_SIGN:
                    second_pos = pos
            return Chess_move(first_pos, second_pos)
        elif len(diffs) == EN_PASSANT_MOVE_DIFFS_COUNT:
            captured = "p" if color_in_move == Color.WHITE else "P"
            first_pos = None
            second_pos = None
            for pos, prev, next in diffs:
                if prev.isdigit():
                    second_pos = pos
                elif prev != captured:
                    first_pos = pos
            return Chess_move(first_pos, second_pos)
        else:
            raise Exception("Unhandeled move: ", diffs)

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
    
    def __eq__(self, __value: object) -> bool:
        return self.move_from == __value.move_from and self.move_to == __value.move_to
    
    def __str__(self) -> str:
        return self.get_UCI()
    
    def __repr__(self) -> str:
        return self.get_UCI()

    @staticmethod
    def from_UCI(UCI):
        return Chess_move(Chess_board_pos.from_str(UCI[:2]), Chess_board_pos.from_str(UCI[2:]))

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
    def __init__(self, id, creation_time):
        self.id = id
        self.creation_time = creation_time

    def get_id(self):
        return self.id

    def get_creation_time(self):
        return self.creation_time

    @staticmethod
    def from_json(json):
        return Chess_lichess_game_data(json["id"], json["createdAt"])
        

def get_auth(token):
    return {"Authorization": 'Bearer {}'.format(token)}

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
        headers.update(get_auth(token))

        response = requests.post(url, headers=headers, json=payload)
        return Lichess_api_controller(token, Chess_lichess_game_data.from_json(response.json()))
    
    def abandon_game(self):
        url = "https://lichess.org/api/board/game/" + self.lichess_game_data.get_id() + "/abort"
        requests.post(url, headers=get_auth(self.token))

    def get_moves(self):
        url = f"https://lichess.org/game/export/{self.lichess_game_data.get_id()}"
        data = requests.get(url, headers={"Accept": "application/json"})
        return data.json()["moves"].split(" ")
    
    def make_move(self, move):
        url = "https://lichess.org/api/board/game/" + self.lichess_game_data.get_id() + "/move/" + move.get_UCI()
        requests.post(url, headers=get_auth(self.token))
        pass

    def get_game_fen(self):
        url = f'https://lichess.org/api/stream/game/{self.lichess_game_data.get_id()}'
        
        with requests.get(url, headers=None, stream=True) as resp:
            for line in resp.iter_lines():
                line_str = line.decode("utf-8")
                line_json = json.loads(line_str)
                fen = line_json["fen"]
                if fen:
                    return FEN_content(fen)
        return None 
               



class Chess_game_controller:
    def __init__(self, token):
        self.token = token

    def new_start_game(self, color):
        self.player_color = color
        self.enemy_color = Color.next(color)
        self.current_player = color if color == Color.WHITE else Color.next(color)
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
        return self.current_player
    
    def accept_move(self):
        self.current_player = Color.next(self.current_player)

    def reject_move(self, move):
        pass
        
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
        self.current_player = Color.next(self.current_player)        
        self.lichess_controller.make_move(move)
        self.calculated_best_move = None

    
        

if __name__ == "__main__":
    # TOKEN = 'lip_eMBV2qjns7LExky0LRCs'
    # client_secrets = "eei_QPIYlTfWnRnA"

    # chess_game_controller = Chess_game_controller(TOKEN)
    # chess_game_controller.new_start_game(Color.WHITE)

    # time.sleep(4)

    # moves = chess_game_controller.lichess_controller.get_moves()
    # print(moves)
    # print(chess_game_controller.get_best_move().move_to.into_str())
    # chess_game_controller.accept_move()

    # chess_game_controller.lichess_controller.get_games()

    # # time.sleep(4)

    # # move_from = Single_board_position_controller.from_str('e7')
    # # move_to = Single_board_position_controller.from_str('e5')
    # # chess_move = Chess_move(move_from, move_to)

    # # chess_game_controller.make_enemy_move(chess_move)

    # # time.sleep(4)

    # # moves = chess_game_controller.lichess_controller.get_moves()
    # # print(moves)

    # # print(chess_game_controller.get_best_move().move_to.into_str())
    # # chess_game_controller.accept_move()


    # # time.sleep(4)

    # chess_game_controller.abandon_game() 


    prev_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    next_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"

    FEN_constroller.get_diff_move(prev_fen, next_fen)