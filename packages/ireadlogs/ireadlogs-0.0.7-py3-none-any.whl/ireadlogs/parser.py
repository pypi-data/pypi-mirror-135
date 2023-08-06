import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("logfile")
        self.parser.add_argument(
            "--pages",
            default=10,
            type=int,
            help="limits the top pages shown (default is 10)",
        )
        self.parser.add_argument(
            "--hosts",
            default=10,
            type=int,
            help="limits the top hosts shown (default is 10)",
        )
        self.parser.add_argument(
            "--hosts-breakdown",
            default=5,
            type=int,
            help="limits the top pages per host breakdown (default is 5)",
        )
        self.parser.add_argument(
            "--show-errors",
            default=False,
            const=True,
            action="store_const",
            help="if present show malformed line numbers ",
        )
