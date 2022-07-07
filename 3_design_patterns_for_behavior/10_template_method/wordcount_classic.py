import html.parser
import os
import re
import sys


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {}".format(os.path.basename(sys.argv[0])))
        sys.exit(1)
    count_words_in_files(sys.argv[1:])


def count_words_in_files(files):
    total = 0
    for filename in files:
        count = count_words(filename)
        if count is not None:
            total += count
            print("{:9,} words in {}".format(count, filename))
    print("total: {:,} words".format(total))


def count_words(filename):
    for wordCounter in (PlaintextWordCounter, HtmlWordCounter):
        if wordCounter.can_count(filename):
            return wordCounter.count(filename)


class AbstractWordCounter:
    @staticmethod
    def can_count(filename):
        raise NotImplementedError()

    @staticmethod
    def count(filename):
        raise NotImplementedError()


class PlaintextWordCounter(AbstractWordCounter):
    @staticmethod
    def can_count(filename):
        return filename.lower().endswith(".txt")

    @staticmethod
    def count(filename):

        if not PlaintextWordCounter.can_count(filename):
            return 0
        regex = re.compile(r"\w+")
        total = 0

        with open(filename, encoding="utf-8") as file:
            for line in file:
                for _ in regex.finditer(line):
                    total += 1

        return total


class HtmlWordCounter(AbstractWordCounter):
    class __HtmlParser(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.regex = re.compile(r"\w+")
            self.inText = True
            self.text = []
            self.count = 0

        def handle_starttag(self, tag, attrs):
            if tag in {"script", "style"}:
                self.inText = False

        def handle_endtag(self, tag):
            if tag in {"script", "style"}:
                self.inText = True
            else:
                for _ in self.regex.finditer(" ".join(self.text)):
                    self.count += 1
                self.text = []

        def handle_data(self, text):
            if self.inText:
                text = text.rstrip()
                if text:
                    self.text.append(text)

    @staticmethod
    def can_count(filename):
        return filename.lower().endwith((".htm", ".html"))

    @staticmethod
    def count(filename):
        if not HtmlWordCounter.can_count(filename):
            return 0
        parser = HtmlWordCounter.__HtmlParser()
        with open(filename, encoding="utf-8") as file:
            parser.feed(file.read())
        return parser.count


if __name__ == "__main__":
    main()
