# Hacker News Reader

Fetch Hacker News top stories right from your terminal.

## Pre-requisites

1. Install the Firebase CLI for your OS (Windows, macOS, or Linux)
     - Follow the installation instructions here: [Firebase CLI reference](https://firebase.google.com/docs/cli#install-cli-mac-linux)
     - Make sure to login to Firebase with the command below (you can use your Google credentials to login).

 ```bash
   $ firebase login
 ```

2. Verify you have Python 3 installed:

```bash
   $ python --version
```
   - If not installed, download Python [here](https://www.python.org/downloads/)

3. Install Python's `request` library:

```bash
   $ pip install requests
```

## Running the program

1. Download the code from this repository.
2. Open your terminal window and navigate to the directory where the `hnreader.py` module is located.
3. Execute the program:

```bash
   $ python3 hnreader.py
```
This will fetch the latest top 10 stories.

4. You can specify the number of stories to fetch with the `-q` or `--quantity` flag:

```bash
   $ python3 hnreader.py -q 25
```
This will fetch the latest top 25 stories

5. Depending on your terminal: Ctr+click, Cmd+click, or just click on the link in the story to open it in a browser.
   -  If using zsh on macOS, you can preview the story without opening a browser:
      -  Ctrl+click on the url, then select Quick Look:
![zsh](./img/hnreader-on-zsh.png)


*Note*: The max number of stories is 500 per the Hacker News API limit.

6. Alternatively, you can run the file directly:

```bash
   $ ./hnreader.py
```

## Screen views

### Usage

```
$ python3 hnreader.py -h
usage: hnreader [-h] [-q]

Fetch the latest top stories from Hacker News

optional arguments:
  -h, --help        show this help message and exit
  -q , --quantity   The number of stories to display (max is 500). If not provided, the default is 10.
```

### Fetching stories

```
$ python3 hnreader.py -q 5

******************************************************************
                  Hacker News - Top Stories

                  Fri Feb 10 10:47:44 2023

******************************************************************
[fetching the latest top 5 stories...]

[1]. “Open Source” Seeds Loosen Big Ag’s Grip on Farmers
https://worldsensorium.com/open-source-seeds-loosen-big-ags-grip-on-farmers/
207 points | 2 hours ago
-------------------------

[2]. Is Seattle a 15-minute city? It depends on where you want to walk
https://nathenry.com/writing/2023-02-07-seattle-walkability.html
102 points | 1 hour ago
-------------------------

[3]. Show HN: Spaghettify – A VSCode Extension to make your code worse with AI
https://www.spaghettify.dev/
74 points | 1 hour ago
-------------------------

[4]. Manticore 6.0.0 – a faster alternative to Elasticsearch in C++
https://manticoresearch.com/blog/manticore-search-6-0-0/
47 points | 1 hour ago
-------------------------

[5]. Show HN: Dslcad a programming language and interpreter for building 3D models
https://github.com/DSchroer/dslcad
53 points | 1 hour ago
-------------------------

```