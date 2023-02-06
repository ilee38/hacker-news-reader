#!usr/bin/env python3

import json
import requests
from datetime import date
import time

# URI prefix for the Hacker News v0 API
API_ENDPOINT_PREFIX = "https://hacker-news.firebaseio.com/v0"

def print_header():
   local_time = time.localtime()

   print("\n**********************************************************")
   print("            Hacker News - Top Stories \n")
   print(f"            {time.asctime(local_time)}")
   print("**********************************************************\n")


def get_story_properties(story_id):
   """
      Returns the properties of a story. If the story is an "Ask HN", it will not
      contain a url property.
   """
   story_endpoint = f"{API_ENDPOINT_PREFIX}/item/{story_id}.json?print=pretty"

   response = requests.get(story_endpoint)
   json_response = json.loads(response.text)

   return json_response


def print_stories(stories_ids):
   """
      Prints the stories details to std output.
   """
   print_header()

   for i in range(10):
      story = get_story_properties(stories_ids[i])

      title = story["title"]
      url = story["url"] if "url" in story else ""
      score = story["score"]

      print(f"[{i+1}]. {title}")
      print(f"{url}")
      print(f"score: {score}")
      print("----------")


def get_top_stories():
   """
      Returns the IDs of up to 500 top stories.
   """
   top_stories_endpoint = f"{API_ENDPOINT_PREFIX}/topstories.json?print=pretty"

   response = requests.get(top_stories_endpoint)
   json_response = json.loads(response.text)

   return json_response


def main():
   top_stories = get_top_stories()
   print_stories(top_stories)


if __name__ == "__main__":
   main()
