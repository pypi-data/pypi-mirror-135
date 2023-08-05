from argparse import ArgumentParser, Namespace


class Config:
    tab_width : int  = 4
    color     : bool = False

    def make_argparser(self, parser: ArgumentParser = None) -> ArgumentParser:
        if parser is None:
            parser = ArgumentParser()

        parser_config = parser.add_argument_group("config")

        parser_config.add_argument("--tab-width", type=int, default=self.tab_width,
            help="Which tab width to use when calculating the column position for \\t.")

        parser_config.add_argument("--color-output", action="store_true",
            help="Force colored output.")

        return parser

    def parse_args(self, args: Namespace):
        self.tab_width = args.tab_width
        self.color     = args.color_output


# singleton
CONFIG = Config()
del Config

# This enables all who import CONFIG to make changes, visible to all as they
# share the same reference
