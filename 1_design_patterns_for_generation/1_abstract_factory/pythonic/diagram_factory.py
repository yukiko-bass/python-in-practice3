class DiagramFactory:
    """
    Diagram, Rectangle, Text を nest することにより、
    main.py からはサブクラスのメソッドを呼ばなくて良くなる
    """

    @classmethod
    def make_diagram(cls, width, height):
        return cls.Diagram(width, height)

    @classmethod
    def make_rectangle(cls, x, y, width, height, fill="white", stroke="black"):
        return cls.Rectangle(x, y, width, height, fill, stroke)

    @classmethod
    def make_text(cls, x, y, text, fontsize=12):
        return cls.Text(x, y, text, fontsize)

    BLANK = " "
    CORNER = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"

    @staticmethod
    def _create_rectangle(width, height, fill):
        rows = [[fill for _ in range(width)] for _ in range(height)]
        for x in range(1, width - 1):
            rows[0][x] = DiagramFactory.HORIZONTAL
            rows[height - 1][x] = DiagramFactory.HORIZONTAL
        for y in range(1, height - 1):
            rows[y][0] = DiagramFactory.VERTICAL
            rows[y][width - 1] = DiagramFactory.VERTICAL
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)):
            rows[y][x] = DiagramFactory.CORNER
        return rows

    class Diagram:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.diagram = DiagramFactory._create_rectangle(
                self.width, self.height, DiagramFactory.BLANK
            )

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

    class Rectangle:
        def __init__(self, x, y, width, height, fill, stroke):
            self.x = x
            self.y = y
            self.rows = DiagramFactory._create_rectangle(
                width, height, DiagramFactory.BLANK if fill == "white" else "%"
            )

    class Text:
        def __init__(self, x, y, text, fontsize):
            self.x = x
            self.y = y
            self.rows = [list(text)]
