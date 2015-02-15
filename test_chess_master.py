import unittest
from chess_master import ChessMaster


class TestChessMaster(unittest.TestCase):
    def setUp(self):
        self.board_string1 = """|kd|  |  |  |  |rd|  |nd|=\\n|  |  |  |  |  |  |  | |=\\n|  |nl|nl|  |  |  |  |  |=\\n|  |  |  |nl|  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |nl|  |  |  |"""
        self.chess_master1 = ChessMaster(self.board_string1)

        self.board_string2 = """|rd|  |  |  |  |rd|  |nd|=\\n|  |  |kd|  |  |  |  | |=\\n|  |nl|nl|  |  |  |  |  |=\\n|  |  |  |nl|  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |  |  |  |  |=\\n|  |  |  |  |nl|  |  | nl |"""
        self.chess_master2 = ChessMaster(self.board_string2)


    def test_white_can_mate_in_one_move(self):
        self.assertTrue(self.chess_master1.white_can_mate_in_one_move())
        self.assertTrue(self.chess_master2.white_can_mate_in_one_move())

    def test_board_position_update_after_move(self):
        self.chess_master1.white_can_mate_in_one_move()
        board_string_after_move = self.chess_master1.to_string()
        self.assertNotEquals(self.board_string1, board_string_after_move)

    def test_black_is_in_checkmate(self):
        self.assertEquals(self.chess_master1.black_is_in_checkmate(), False)


if __name__ == "__main__":
    unittest.main()

