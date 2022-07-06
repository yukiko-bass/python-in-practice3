import io
import os
import sys


BLACK, WHITE = ("BLACK", "WHITE")


def main():
    checkers = CheckersBoard()
    print(checkers)

    chess = ChessBoard()
    print(chess)

    if sys.platform.startswith("win"):
        sys.stdout = io.StringIO()
        filename = os.path.join(os.getcwd(), "gameboard.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(io.StringIO().getvalue())
        print("wrote '{}'".format(filename), file=sys.__stdout__)


# 微妙に違う気がするけど、win環境じゃないからいいか・・・
def console(char, background):
    if sys.platform.startswith("win"):
        return char or " "

    else:
        return "\x1B[{}m{}\x1B[0m".format(
            43 if background == BLACK else 47, char or " "
        )


class AbstractBoard:
    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()

    def populate_board(self):
        raise NotImplementedError()

    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y + x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):
    def __init__(self):
        super().__init__(10, 10)

    def populate_board(self):
        for x in range(0, 9, 2):
            for row in range(4):
                column = x + ((row + 1) % 2)
                self.board[row][column] = BlackDraught()
                self.board[row + 6][column] = WhiteDraught()


class ChessBoard(AbstractBoard):
    def __init__(self):
        super().__init__(8, 8)

    def populate_board(self):
        self.board[0][0] = BlackChessRook()
        self.board[0][1] = BlackChessKnight()
        self.board[0][2] = BlackChessBishop()
        self.board[0][3] = BlackChessQueen()
        self.board[0][4] = BlackChessKing()
        self.board[0][5] = BlackChessBishop()
        self.board[0][6] = BlackChessKnight()
        self.board[0][7] = BlackChessRook()
        self.board[7][0] = WhiteChessRook()
        self.board[7][1] = WhiteChessKnight()
        self.board[7][2] = WhiteChessBishop()
        self.board[7][3] = WhiteChessQueen()
        self.board[7][4] = WhiteChessKing()
        self.board[7][5] = WhiteChessBishop()
        self.board[7][6] = WhiteChessKnight()
        self.board[7][7] = WhiteChessRook()
        for column in range(8):
            self.board[1][column] = BlackChessPawn()
            self.board[6][column] = WhiteChessPawn()


class Piece(str):

    __slots__ = ()


class BlackDraught(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black draughts man}")


class WhiteDraught(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white draughts man}")


class BlackChessKing(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess king}")


class WhiteChessKing(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess king}")


class BlackChessQueen(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess queen}")


class WhiteChessQueen(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess queen}")


class BlackChessRook(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess rook}")


class WhiteChessRook(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess rook}")


class BlackChessBishop(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess bishop}")


class WhiteChessBishop(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess bishop}")


class BlackChessKnight(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess knight}")


class WhiteChessKnight(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess knight}")


class BlackChessPawn(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{black chess pawn}")


class WhiteChessPawn(Piece):

    __slots__ = ()

    def __new__(cls):
        return super().__new__(cls, "\N{white chess pawn}")


if __name__ == "__main__":
    main()
