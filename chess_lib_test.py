from chess_lib import FEN_constroller, FEN_content, Chess_board_pos, Chess_move
import unittest

INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class Test_FEN_content(unittest.TestCase):
    def test_toggle_player(self):
        test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        expected_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.toggle_player()
        self.assertEqual(fen.into_str(), expected_fen)
    
    def test_get_position(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        self.assertEqual(fen.get_position(0, 1), "R")
        self.assertEqual(fen.get_position(2, 0), "N")
        self.assertEqual(fen.get_position(3, 1), "P")
        self.assertEqual(fen.get_position(3, 3), "P")
        self.assertEqual(fen.get_position(4, 4), "P")

    def test_set_position_replace_piece(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/Q7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(2, 0, "Q")
        self.assertEqual(fen.into_str(), expected_fen)
    
    def test_set_position_replace_single_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/QP1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(3, 0, "Q")
        self.assertEqual(fen.into_str(), expected_fen)
    
    def test_set_position_add_before_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/NQ6/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(2, 1, "Q")
        self.assertEqual(fen.into_str(), expected_fen)

    def test_set_position_add_after_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N6Q/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(2, 7, "Q")
        self.assertEqual(fen.into_str(), expected_fen)

    def test_set_position_split_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N2Q4/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(2, 3, "Q")
        self.assertEqual(fen.into_str(), expected_fen)

    def test_set_position_one_space_after_piece(self):
        test_fen = "r1bqkbnr/ppp1pppp/2n5/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbnr/ppp1pppp/2n5/3p4/3P4/2N1B3/PPP1PPPP/R1BQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.set_position(2, 4, "B")
        self.assertEqual(fen.into_str(), expected_fen)

    def test_pop_piece_surrounded(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1PPP2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.pop_piece(3, 2)
        self.assertEqual(fen.into_str(), expected_fen)

    def test_pop_piece_before_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1PPP2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1PP3PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.pop_piece(3, 3)
        self.assertEqual(fen.into_str(), expected_fen)
    
    def test_pop_piece_after_space(self):
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1PPP2PP/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        expected_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1PPP3P/N7/P1P2P2/1RBQKBNR w KQkq - 0 1"
        fen = FEN_content(test_fen)
        fen.pop_piece(3, 6)
        self.assertEqual(fen.into_str(), expected_fen)


    def test_get_position_piece_beteen_pieces(self):
        test_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"
        row = 0
        col = 2 
        expected_piece = "B"

        piece = FEN_content(test_fen).get_position(row, col)

        self.assertEqual(piece, expected_piece)

    def test_get_position_empty_line(self):
        test_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"
        row = 2
        expected_piece = "8"

        BOARD_SIZE = 8
        for col in range(BOARD_SIZE):
            piece = FEN_content(test_fen).get_position(row, col)
            self.assertEqual(piece, expected_piece)

    def test_get_position_single_piece_middle_of_line(self):
        test_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"
        row = 3
        piece_col = 3
        expected_piece = "P"
        expected_before = "3"
        expected_after = "4"

        BOARD_SIZE = 8
        for col in range(BOARD_SIZE):
            if col == piece_col:
                piece = FEN_content(test_fen).get_position(row, col)
                self.assertEqual(piece, expected_piece)
            elif col < piece_col:   
                piece = FEN_content(test_fen).get_position(row, col)
                self.assertEqual(piece, expected_before)
            else:
                piece = FEN_content(test_fen).get_position(row, col)
                self.assertEqual(piece, expected_after)

        
class Test_FEN_controller(unittest.TestCase):
    def test_get_initial_fen(self):
        self.assertEqual(FEN_constroller.get_initial_fen(), INITIAL_FEN)

    def test_move_to_same_field(self):
        EXPECTED_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        move_from = Chess_board_pos(0, 0)
        move_to = Chess_board_pos(0, 0)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_next_move_surrounded_into_surrounded(self):
        EXPECTED_FEN = "r1bqkbnr/ppp1p1pp/2n5/3pPp2/3P1P2/8/PPP3PP/RNBQKBNR b KQkq - 1 9"
        test_fen     = "r1bqkbnr/ppp1p1pp/2n5/3p1p2/3PPP2/8/PPP3PP/RNBQKBNR w KQkq - 1 9"
        move_from = Chess_board_pos(3, 4)
        move_to = Chess_board_pos(4, 4)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)       
        self.assertEqual(result, EXPECTED_FEN)

    def test_next_move_last_column(self):
        EXPECTED_FEN = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2PP/N7/P1P2P2/1RBQKBNR b KQkq - 1 4"
        test_fen = "r1bqkbr1/pp2p1pp/2n2p1n/2ppP3/1P1P2P1/N7/P1P2P1P/1RBQKBNR w KQkq - 1 4"
        move_from = Chess_board_pos(1, 7)
        move_to = Chess_board_pos(3, 7)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_next_move_first_column(self):
        EXPECTED_FEN = "r2qkbr1/pp2p1pp/5p1n/nPppP3/3P2bP/N7/P1P2P2/1RBQKBNR w KQkq - 0 5"
        test_fen = "r2qkbr1/pp2p1pp/2n2p1n/1PppP3/3P2bP/N7/P1P2P2/1RBQKBNR b KQkq - 0 5"
        move_from = Chess_board_pos(5, 2)
        move_to = Chess_board_pos(4, 0)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_next_move_capture(self):
        test_fen = "r1bqkbnr/ppp1p1pp/2n5/3p1p2/3PPP2/8/PPP3PP/RNBQKBNR w KQkq - 1 9"
        EXPECTED_FEN = "r1bqkbnr/ppp1p1pp/2n5/3P1p2/3P1P2/8/PPP3PP/RNBQKBNR b KQkq - 1 9"
        move_from = Chess_board_pos(3, 4)
        move_to = Chess_board_pos(4, 3)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_next_move_between_spaces_into_middle_of_empty_row(self):
        test_fen = "r1b1kbnr/1pp1p2p/2n1q1p1/p2pPp2/PP2PPPP/8/2P5/RNBQKBNR w KQkq - 1 13"
        EXPECTED_FEN = "r1b1kbnr/1pp1p2p/2n1q1p1/p2pPp2/PP2PPPP/2P5/8/RNBQKBNR b KQkq - 1 13"
        move_from = Chess_board_pos(1, 2)
        move_to = Chess_board_pos(2, 2)
        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_move_one_space_after_piece(self):
        test_fen     = "r1bqkbnr/ppp1pppp/2n5/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq - 0 1"
        EXPECTED_FEN = "r1bqkbnr/ppp1pppp/2n5/3p4/3P4/2N1B3/PPP1PPPP/R2QKBNR b KQkq - 0 1"

        move_from = Chess_board_pos.from_str("c1")
        move_to = Chess_board_pos.from_str("e3")

        result = FEN_constroller.next_move(test_fen, move_from, move_to)
        self.assertEqual(result, EXPECTED_FEN)

    def test_get_diff_move_single_moves(self):
        initial = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        moves = [
            "d2d4",
            "d7d5",
            "b1c3",
            "b8c6",
            "c1f4",
            "g8f6",
            "e2e3",
            "e7e6",
            "f1d3",
            "f8e7",
            "g1f3",
        ]

        last_fen = initial
        for move in moves:
            move_board = Chess_move.from_UCI(move)
            print(move_board.move_from.into_str(), move_board.move_to.into_str())
            next_fen = FEN_constroller.next_move(last_fen, move_board.move_from, move_board.move_to)
            move = FEN_constroller.get_diff_move(last_fen, next_fen)
            print(move, " - ", move_board, "; ", last_fen, " -> ", next_fen)
            self.assertEqual(move, move_board)
            last_fen = next_fen
            

if __name__ == '__main__':
    unittest.main()
        