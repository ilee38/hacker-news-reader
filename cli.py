import argparse

parser = argparse.ArgumentParser(
   prog="hnreader",
   description="Fetch the latest top stories from Hacker News"
)

parser.add_argument(
   "-q",
   "--quantity",
   default=10,
   help="The number of stories to display (max is 500). If not provided, the default is 10.",
   required=False,
   type=int,
   metavar=""
)

parser.add_argument(
   "-t",
   "--tui",
   action="store_true",
   help="Launch interactive TUI mode.",
   required=False
)
