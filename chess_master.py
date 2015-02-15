import sys

BLANK_SQUARE = ''


class ChessMasterException(Exception):
    def __init__(self, message):
        super(ChessMasterException, self).__init__()
        self.message = message

    def __str__(self):
        return repr(self.message)

class ChessMaster(object):
    def __init__(self, board_string):
        self.board = self.from_string(board_string)

    def from_string(self, board_string):
        board_rows = [
            row.replace('=', '').split('|')[1:-1] 
            for row in board_string.split("\\n")]
        board_rows = [map(lambda l: l.strip(), row) for row in board_rows]
        return board_rows

    def _get_piece_position(self, piece):
        position = [(row_pos, row.index(piece))
                    for row_pos, row in enumerate(self.board) if piece in row]
        return position

    def black_is_in_checkmate(self):
        try:
            black_king_pos = self._get_piece_position('kd')[0]
        except IndexError:
            raise ChessMasterException("No black king present, "
                                       "hence checkmate is not valid.")
        white_piece_pos = self._get_piece_position('nl')
        if any([abs(wpos[0] - black_king_pos[0]) == 0 and 
                abs(wpos[1] - black_king_pos[1]) == 0
                for wpos in white_piece_pos]):
            return True
        else:
            return False

    def white_can_mate_in_one_move(self):
        result = self.make_white_mate_move()
        if len(result) == 2 and result[1]:
            return True
        else:
            return False

    def _get_knight_pos_by_index(self, pos_mov_map, select_pos, 
                                white_knight_pos_map):
        for white_kn_pos, closest_pos, in pos_mov_map.items():
            if closest_pos == select_pos:
                return white_knight_pos_map[white_kn_pos]

    def board_update(self, initial, final):
        piece = self.board[initial[0]][initial[1]]
        self.board[final[0]][final[1]] = piece
        self.board[initial[0]][initial[1]] = BLANK_SQUARE

    def make_white_mate_move(self):
        white_knight_position = self._get_piece_position('nl')
        if not white_knight_position:
            return "No Move"
        black_king_position = self._get_piece_position('kd')
        if not black_king_position:
            return "No Move"
        if len(black_king_position) > 1:
            raise ChessMasterException("More than 1 black king is not "
                                       "possible.")
        try:
            row_bk = black_king_position[0][0]
            col_bk = black_king_position[0][1]
        except IndexError:
            print "No black king"
            return
        for white_knight_pos in white_knight_position:
            row_wk = white_knight_pos[0]
            col_wk = white_knight_pos[1]
            if (row_wk + 2 == row_bk) or (row_wk - 2 == row_bk) and \
               (col_wk + 1 == col_bk or col_wk - 1 == col_bk):
                white_knight_final_row = row_wk + 2
                white_knight_final_col = col_wk + 1
                if row_bk - row_wk < 0:
                    white_knight_final_row = row_wk - 2
                if col_bk - col_wk < 0:
                    white_knight_final_col = col_wk - 1
                self.board_update(white_knight_pos,
                                  (white_knight_final_row,
                                   white_knight_final_col))
                return (white_knight_pos, "checkmate")

        possible_moves_map = {}
        possible_moves_map = {
            i: (abs(wk[0] - row_bk), abs(wk[1] - col_bk)) 
            for i, wk in enumerate(white_knight_position)
        }
        possible_moves_by_wk = possible_moves_map.values()

        even_moves = sorted(
            sorted([move_pos for move_pos in possible_moves_by_wk 
                    if move_pos[0] % 2 == 0]), key=lambda l: l[1])

        if even_moves:
            next_move_piece_pos = self._get_knight_pos_by_index(
                possible_moves_map, even_moves[0], white_knight_position)
        else:
            odd_moves = sorted(
                sorted([move_pos for move_pos in possible_moves_by_wk 
                        if move_pos[0] % 2 != 0]), key=lambda l: l[1])
                
            next_move_piece_pos = self._get_knight_pos_by_index(
                    possible_moves_map, odd_moves[0], white_knight_position)
        next_move_row = next_move_piece_pos[0] + 2
        next_move_col = next_move_piece_pos[1] + 1
        if row_bk - next_move_piece_pos[0] < 0:
            next_move_row = next_move_piece_pos[0] - 2
        if col_bk - next_move_piece_pos[1] < 0:
            next_move_row = next_move_piece_pos[0] - 1

        self.board_update(next_move_piece_pos, (next_move_row, next_move_col))
        return ((next_move_row, next_move_col), )

    def to_string(self):
        board_string = ""
        for row in self.board:
            board_string += "|" + "|".join(row) + "|=\n"
        return board_string


def main():
    if len(sys.argv) < 2:
        return "Feed board string"
    board_string = sys.argv[1]
    cm = ChessMaster(board_string)
    print "White Can mate in one move"
    print cm.white_can_mate_in_one_move()
    print "Board after white move"
    print cm.to_string()

if __name__ == "__main__":
    main()
