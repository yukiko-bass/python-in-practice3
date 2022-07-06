SVG_START = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
    width="{pxwidth}px" height="{pxheight}px">"""

SVG_END = "</svg>\n"

SVG_RECTANGLE = """<rect x="{x}" y="{y}" width="{width}" \
height="{height}" fill="{fill}" stroke="{stroke}"/>"""

SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" \
font-family="sans-serif" font-size="{fontsize}">{text}</text>"""

SVG_SCALE = 20


class SvgDiagram:
    def __init__(self, width, height):
        pxwidth = width * SVG_SCALE
        pxheight = height * SVG_SCALE
        self.diagram = [SVG_START.format(**locals())]
        outline = SvgRectangle(0, 0, width, height, "lightgreen", "black")
        self.diagram.append(outline.svg)

    def add(self, component):
        self.diagram.append(component.svg)

    def save(self, filenameOrFile):
        file = None if isinstance(filenameOrFile, str) else filenameOrFile
        try:
            if file is None:
                file = open(filenameOrFile, "w", encoding="utf-8")
            file.write("\n".join(self.diagram))
            file.write("\n" + SVG_END)
        finally:
            if isinstance(filenameOrFile, str) and file is not None:
                file.close()


class SvgRectangle:
    def __init__(self, x, y, width, height, fill, stroke):
        x *= SVG_SCALE
        y *= SVG_SCALE
        width *= SVG_SCALE
        height *= SVG_SCALE
        self.svg = SVG_RECTANGLE.format(**locals())


class SvgText:
    def __init__(self, x, y, text, fontsize):
        x *= SVG_SCALE
        y *= SVG_SCALE
        fontsize *= SVG_SCALE // 10
        self.svg = SVG_TEXT.format(**locals())
