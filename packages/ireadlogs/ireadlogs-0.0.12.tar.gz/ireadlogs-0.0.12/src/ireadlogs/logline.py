import re


class LogLine:
    """Captures an analysed log line"""

    # static - compiled once
    MATCHER = re.compile(r'(.*)\s-\s-\s\[(.*)\]\s"(.*)"\s(.*)')

    # ctor
    def __init__(self, line):
        """
        constructor parses a string line into a LogLine object.
        Code follows https://docs.python.org/3.5/glossary.html#term-eafp design
        philosophy.
        """
        try:
            # match line against reg exp
            m = self.MATCHER.match(line)
            self.host = m.group(1)
            self.time = m.group(2)
            self.version = None
            verb_page_version = m.group(3).split()
            if len(verb_page_version) < 2 or len(verb_page_version) > 3:
                raise ValueError("Malformed line")
            if len(verb_page_version) == 3:
                self.verb, self.page, self.version = verb_page_version
            else:
                self.verb, self.page = verb_page_version
            status_nbytes = m.group(4).split()
            if len(status_nbytes) == 2:
                self.status, self.nbytes = status_nbytes
            else:
                self.status = status_nbytes[0]
                self.nbytes = "0"
            self.status = int(self.status)
            # treat garbage in nbytes
            for c in self.nbytes:
                if not c.isdigit():
                    self.nbytes = 0
                    return
            self.nbytes = int(self.nbytes)
        except Exception:
            raise
