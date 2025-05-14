# Welcome to the Discord Web Scraper

This python tool will scrape all of your messages and can process your data into JSON.

The tool requires two steps, running discordScrape.py, and running tableParse.py after discordScrape.py finishes. 

As of now, the tool works <i>very</i> slowly. In my experience, scraping approximately 201,873 messages took more than an hour, and it took another hour to parse the table after the html was found.

## Setup

### Firefox Profile

To authenticate, this tool makes use of Firefox profiles to automatically log in to Discord.

1. Download [Firefox](https://www.mozilla.org/en-US/firefox/new/?xv=refresh-new&v=b)
2. Open Firefox and type 'about:profiles' in the top url bar
3. Click on 'create a new profile' and follow the steps in creating a new profile
4. While still on the profile page, scroll down to the section with the profile you just created
5. Copy the 'Root Directory' link

### Discord channel url
* You will need to find the url of the channel you wish you scrape. Simply access discord on the web and copy the url from the url bar

This tool makes use of dotenv to store the Firefox profile directory and the Discord channel url. In the root of the project folder, create a file called `.env` and write `profile_directory=`, and `discord_channel_link=`, writing your Firefox profile directory url and your discord channel url, respectively, to the .env file

```python
profile_directory='/path/to/your/firefox/profile/directory'
discord_channel_link='https://discord.com/channels/random_numbers/more_random_numbers'

```