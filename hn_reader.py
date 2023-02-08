#!usr/bin/env python3

import argparse
import json
import requests
import time
from datetime import timedelta


# URI prefix for the Hacker News v0 API
API_ENDPOINT_PREFIX = "https://hacker-news.firebaseio.com/v0"

parser = argparse.ArgumentParser(
   prog="hn_reader",
   description="Fetch the latest top stories from Hacker News"
)

parser.add_argument(
   "-q",
   "--quantity",
   default=10,
   help="The number of stories to display (max is 500). If not provided, the default is 10."
)


def print_header():
   local_time = time.localtime()

   print("\n******************************************************************")
   print("                  Hacker News - Top Stories \n")
   print(f"                  {time.asctime(local_time)}")
   print("******************************************************************\n")


def get_elapsed_time(story_timestamp):
   """
      Returns the elapsed time in hours or minutes from a given timestamp to the
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
   """
      Returns the properties of a story. If the story is an "Ask HN", it will not
      contain a url property.
   """
   story_endpoint = f"{API_ENDPOINT_PREFIX}/item/{story_id}.json?print=pretty"

   response = requests.get(story_endpoint)
   json_response = json.loads(response.text)

   return json_response


def print_stories(stories_ids, quantity):
   """
      Prints the stories details to std output.
   """
   print_header()

   for i in range(quantity):
      story = get_story_properties(stories_ids[i])

      title = story["title"]
      url = story["url"] if "url" in story else ""
      score = story["score"]
      time_value, time_unit = get_elapsed_time(story["time"])

      print(f"[{i+1}]. {title}")
      print(f"{url}")
      print(f"{score} points | {time_value} {time_unit} ago")
      print("-------------------------\n")


def get_top_stories():
   """
      Returns the IDs of up to 500 top stories.
   """
   top_stories_endpoint = f"{API_ENDPOINT_PREFIX}/topstories.json?print=pretty"

   response = requests.get(top_stories_endpoint)
   json_response = json.loads(response.text)

   return json_response


def main():
   args = parser.parse_args()
   top_stories = get_top_stories()
   print_stories(top_stories, int(args.quantity))


if __name__ == "__main__":
   main()
