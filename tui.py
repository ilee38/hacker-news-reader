import webbrowser
from datetime import datetime
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, OptionList, Static


class HackerNewsTUI(App):
   BINDINGS = [
      Binding("enter", "open_story", "Open story"),
      Binding("q", "quit", "Quit"),
      Binding("ctrl+c", "quit", "Quit"),
   ]

   CSS = """
   Screen {
      layout: vertical;
   }

   #banner {
      padding: 0 1;
      border: round cyan;
      color: orange;
   }

   #story_list {
      height: 1fr;
      width: 100%;
      border: round cyan;
   }
   """

   def __init__(self, stories):
      super().__init__()
      self.stories = stories

   def compose(self) -> ComposeResult:
      with Vertical():
         yield Static(self._build_banner_text(), id="banner")
         yield OptionList(
            *[
               f"[{story['index']}] {story['title']} "
               f"({story['score']} points | {story['time_value']} {story['time_unit']} ago)\n"
               f"{story['url'] if story['url'] else ''}\n"
               f"-------------------------"
               for story in self.stories
            ],
            id="story_list",
         )
      yield Footer()

   def on_mount(self):
      story_list = self.query_one("#story_list", OptionList)
      story_list.focus()
      if self.stories:
         story_list.highlighted = 0
      else:
         self.notify("No stories available.", severity="warning")

   def action_open_story(self):
      story_list = self.query_one("#story_list", OptionList)
      selected_index = story_list.highlighted

      if selected_index is None:
         return

      self._open_story_by_index(selected_index)

   def on_option_list_option_selected(self, event: OptionList.OptionSelected):
      self._open_story_by_index(event.option_index)

   def _open_story_by_index(self, selected_index):
      if selected_index < 0 or selected_index >= len(self.stories):
         return

      story = self.stories[selected_index]
      story_url = story["url"]
      if not story_url:
         self.notify("This story does not have a URL.", severity="warning")
         return

      try:
         webbrowser.open(story_url, new=2)
         self.notify(f"Opening [{story['index']}] in browser...")
      except webbrowser.Error:
         self.notify("Unable to open browser for selected story.", severity="error")

   def _build_banner_text(self):
      timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
      return (
         " _   _ _   _ ____                 _\n"
         "| | | | \\ | |  _ \\ ___  __ _  __| | ___ _ __\n"
         "| |_| |  \\| | |_) / _ \\/ _` |/ _` |/ _ \\ '__|\n"
         "|  _  | |\\  |  _ <  __/ (_| | (_| |  __/ |\n"
         "|_| |_|_| \\_|_| \\_\\___|\\__,_|\\__,_|\\___|_|\n"
         "******************************************************************\n"
         "                  Hacker News - Top Stories\n"
         f"                  {timestamp}\n"
         "******************************************************************\n"
         f"[top {len(self.stories)} stories loaded | Up/Down navigate | Enter opens URL]"
      )
