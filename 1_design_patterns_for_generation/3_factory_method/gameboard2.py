import io
import itertools
import os
import sys
import unicodedata


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
            for y in range(4):
                column = x + ((y + 1) % 2)
                # サブクラスをやめた
                for row, color in ((y, "black"), (y + 6, "white")):
                    self.board[row][column] = create_piece("draught", color)


class ChessBoard(AbstractBoard):
    def __init__(self):
        super().__init__(8, 8)

    def populate_board(self):
        for row, color in ((0, "black"), (7, "white")):
            for columns, kind in (
                ((0, 7), "rook"),
                ((1, 6), "knight"),
                ((2, 5), "bishop"),
                ((3,), "queen"),
                ((4,), "king"),
            ):
                for column in columns:
                    self.board[row][column] = create_piece(kind, color)
        for column in range(8):
            for row, color in ((1, "black"), (6, "white")):
                self.board[row][column] = create_piece("pawn", color)


# factory method
def create_piece(kind, color):
    if kind == "draught":
        return eval("{}{}()".format(color.title(), kind.title()))
    return eval("{}Chess{}()".format(color.title(), kind.title()))
    # どんなコードが来ても実行されてしまうのでリスキー


class Piece(str):

    __slots__ = ()


# 必要なPieceのサブクラスを作っている
for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    exec(
        """\
class {}(Piece):

    __slots__ = ()

    def __new__(Class):
        return super().__new__(Class, "{}")""".format(
            name, char
        )
    )
    # Using exec() is risky


if __name__ == "__main__":
    main()
