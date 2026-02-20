#!/usr/bin/env python3

import json
import os
import requests
import sys
import time
from datetime import timedelta
from cli import parser

# URI prefix for the Hacker News v0 API
API_ENDPOINT_PREFIX = "https://hacker-news.firebaseio.com/v0"

ASCII_BANNER = r"""
 _   _ _   _ ____                 _
| | | | \ | |  _ \ ___  __ _  __| | ___ _ __
| |_| |  \| | |_) / _ \/ _` |/ _` |/ _ \ '__|
|  _  | |\  |  _ <  __/ (_| | (_| |  __/ |
|_| |_|_| \_|_| \_\___|\__,_|\__,_|\___|_|
"""

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_CYAN = "\033[36m"
ANSI_BLUE = "\033[34m"
ANSI_WHITE = "\033[97m"
ANSI_YELLOW = "\033[33m"
ANSI_GREEN = "\033[32m"
ANSI_BRIGHT_RED = "\033[91m"
ANSI_UNDERLINE = "\033[4m"
USE_COLORS = sys.stdout.isatty() and os.getenv("TERM", "").lower() != "dumb"


def stylize(text, *styles):
   if not USE_COLORS or len(styles) == 0:
      return text

   return f"{''.join(styles)}{text}{ANSI_RESET}"


def print_header(num_of_stories):
   local_time = time.localtime()

   print(stylize(ASCII_BANNER, ANSI_BOLD, ANSI_BRIGHT_RED))
   print(stylize("******************************************************************", ANSI_CYAN))
   print(stylize("                  Hacker News - Top Stories", ANSI_BOLD, ANSI_WHITE))
   print(stylize(f"                  {time.asctime(local_time)}", ANSI_DIM))
   print(stylize("******************************************************************", ANSI_CYAN))
   print(stylize(f"[fetching the latest top {num_of_stories} stories...]\n", ANSI_GREEN))

   time.sleep(1.0)


def get_elapsed_time(story_timestamp):
   """Returns the elapsed time in hours or minutes from a given timestamp to the
      current time.
   """
   time_value = None
   time_units = None

   current_time = timedelta(seconds=time.time())
   story_time = timedelta(seconds=story_timestamp)
   time_delta = current_time - story_time

   if time_delta.seconds // 3600 > 0:
      time_value = int(time_delta.seconds // 3600)
      time_units = "hours" if time_value > 1 else "hour"
   else:
      time_value = int(time_delta.seconds // 60)
      time_units = "minutes" if time_value > 1 else "minute"

   return time_value, time_units


def get_story_properties(story_id):
   """Returns the properties of a story. If the story is an "Ask HN", it will not
      contain a url property.
   """
   story_endpoint = f"{API_ENDPOINT_PREFIX}/item/{story_id}.json?print=pretty"

   response = requests.get(story_endpoint)
   json_response = json.loads(response.text)

   return json_response


def get_top_stories():
   """Returns the IDs of up to 500 top stories.
   """
   top_stories_endpoint = f"{API_ENDPOINT_PREFIX}/topstories.json?print=pretty"

   response = requests.get(top_stories_endpoint)
   json_response = json.loads(response.text)

   return json_response


def fetch_stories(quantity):
   stories_ids = get_top_stories()
   num_of_stories = max(0, min(quantity, len(stories_ids)))
   stories = []

   for i, story_id in enumerate(stories_ids[:num_of_stories], start=1):
      story = get_story_properties(story_id)
      time_value, time_unit = get_elapsed_time(story["time"])

      stories.append(
         {
            "index": i,
            "title": story["title"],
            "url": story["url"] if "url" in story else "",
            "score": story["score"],
            "time_value": time_value,
            "time_unit": time_unit,
         }
      )

   return stories


def print_stories(stories):
   """Prints the stories details to std output."""
   print_header(len(stories))

   for story in stories:
      print(stylize(f"[{story['index']}]. {story['title']}", ANSI_BOLD, ANSI_WHITE))
      print(stylize(story["url"] if story["url"] else "(no url available)", ANSI_UNDERLINE, ANSI_BLUE))
      print(
         stylize(
            f"{story['score']} points | {story['time_value']} {story['time_unit']} ago",
            ANSI_YELLOW,
         )
      )
      print(stylize("-------------------------\n", ANSI_DIM))


def run_tui(stories):
   from tui import HackerNewsTUI

   app = HackerNewsTUI(stories)
   app.run()


def main():
   args = parser.parse_args()
   stories = fetch_stories(args.quantity)

   if args.tui:
      run_tui(stories)
   else:
      os.system("clear" if os.name != "nt" else "cls")
      print_stories(stories)


if __name__ == "__main__":
   main()
