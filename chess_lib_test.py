from chess_lib import FEN_constroller, FEN_content, Chess_board_pos
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

if __name__ == '__main__':
    unittest.main()
        