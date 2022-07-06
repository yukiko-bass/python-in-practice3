import os
import sys
from diagram_factory import DiagramFactory
from svg_diagram_factory import SvgDiagramFactory


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-P":
        create_diagram(DiagramFactory).save(sys.stdout)
        create_diagram(SvgDiagramFactory).save(sys.stdout)
        return
    textFilename = os.path.join(os.getcwd(), "diagram.txt")
    svgFilename = os.path.join(os.getcwd(), "diagram.svg")

    txtDiagram = create_diagram(DiagramFactory)
    txtDiagram.save(textFilename)
    print("wrote", textFilename)

    svgDiagram = create_diagram(SvgDiagramFactory)
    svgDiagram.save(svgFilename)
    print("wrote", svgFilename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return diagram


if __name__ == "__main__":
    main()
