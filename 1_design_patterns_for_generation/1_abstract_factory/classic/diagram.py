BLANK = " "
CORNER = "+"
HORIZONTAL = "-"
VERTICAL = "|"


class Diagram:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.diagram = _create_rectangle(self.width, self.height, BLANK)

    def add(self, componant):
        for y, row in enumerate(componant.rows):
            for x, char in enumerate(row):
                self.diagram[y + componant.y][x + componant.x] = char

    def save(self, filenameOrFile):
        file = None if isinstance(filenameOrFile, str) else filenameOrFile
        try:
            if file is None:
                file = open(filenameOrFile, "w", encoding="utf-8")
            for row in self.diagram:
                print("".join(row), file=file)
        finally:
            if isinstance(filenameOrFile, str) and file is not None:
                file.close()


def _create_rectangle(width, height, fill):
    rows = [[fill for _ in range(width)] for _ in range(height)]
    for x in range(1, width - 1):
        rows[0][x] = HORIZONTAL
        rows[height - 1][x] = HORIZONTAL
    for y in range(1, height - 1):
        rows[y][0] = VERTICAL
        rows[y][width - 1] = VERTICAL
    for y, x in ((0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)):
        rows[y][x] = CORNER
    return rows


class Rectangle:
    def __init__(self, x, y, width, height, fill, stroke):
        self.x = x
        self.y = y
        self.rows = _create_rectangle(width, height, BLANK if fill == "white" else "%")


class Text:
    def __init__(self, x, y, text, fontsize):
        self.x = x
        self.y = y
        self.rows = [list(text)]
