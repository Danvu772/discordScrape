# Welcome to the Discord Web Scraper

This python tool will scrape all of your messages and processes your data into JSON.

As of now, the tool works <i>very</i> slowly. In my experience, scraping approximately 201,873 messages took more than an hour, and it took another hour to parse the table after the html was found. not good numbers :(

## Setup

### Python Stuff
1. Use a virtual environment within the project root directory. Use `python -m venv .venv` to create a virtual environment
2. Use the virtual environment by running `source .venv/bin/activate`
3. To set up all packages, use `pip install -r requirements.txt` 

### Firefox Profile

To authenticate, this tool makes use of Firefox profiles to automatically log in to Discord.

1. Download [Firefox](https://www.mozilla.org/en-US/firefox/new/?xv=refresh-new&v=b)
2. Open Firefox and type 'about:profiles' in the top url bar
3. Click on 'create a new profile' and follow the steps in creating a new profile
4. While still on the profile page, scroll down to the section with the profile you just created
5. Copy the 'Root Directory' link

### Discord channel url
1. You will need to find the url of the channel you wish you scrape. Simply access discord on the web and copy the url from the url bar

This tool makes use of dotenv to store the Firefox profile directory and the Discord channel url. In the root of the project folder, create a file called `.env` and write `profile_directory=`, and `discord_channel_link=`, writing your Firefox profile directory url and your discord channel url, respectively, to the .env file

```python
profile_directory='/path/to/your/firefox/profile/directory'
discord_channel_link='https://discord.com/channels/random_numbers/more_random_numbers'

```

## Actually using this
After your setup, run `python discordScrape.py` in the terminal in your project root directory

It supports two modes:
  - fullScrape: Scrape the entire channel history based on the Discord channel link in your .env file.
  - sync: Scrape only new messages since the last saved message in the JSON file.

Make sure to set the required environment variables in your .env file:
  - profile_directory: Path to your Firefox profile for Selenium
  - discord_channel_link: URL to the Discord channel to scrape

#### Example
```
$ python discordScrape.py fullScrape    # Scrape your entire chat history

$ python discordScrape.py sync          # Scrape up to last saved message 
```

To get the help message, you can simply use `python discordScrape.py` or `python discordScrape.py -h`

# Todos
- Fix variable names
- ~~Implement sync - implemented, time to test it~~
- Fix reply id - it seems to be getting the message content instead
- Fix end of chat scraping