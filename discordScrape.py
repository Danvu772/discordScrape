from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException 
import time
import os
from dotenv import load_dotenv
from tableParse import parseHtml, finalCleanup, combine_json
import pandas as pd
import argparse
import sys
from bs4 import BeautifulSoup
import re

def discordScrape(last_message_id):
    if last_message_id:
        temp_json_path = 'resources/json/temp.json'
    options = Options()

    options.profile = profile_directory
    options.add_argument('--headless')
    driver = Firefox(options=options)
    driver.get(discord_channel_link)
    print('accessed page')

    message_item_class_xpath =  '//li[@class="messageListItem__5126c"]'
    message_item_class_xpath_text =  '//li[@class="messageListItem__5126c"]//div[contains(@class, "messageContent")]'
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, message_item_class_xpath_text)))
    message_list = driver.find_elements(By.XPATH, message_item_class_xpath)
    previous_first_message = message_list[-1]
    if os.path.exists(json_path) and last_message_id is not None:
        os.remove(json_path)
    if last_message_id is None:
        parseHtml(previous_first_message.get_attribute('outerHTML'), json_path)
    else:
        parseHtml(previous_first_message.get_attribute('outerHTML'), temp_json_path)
    scrolls = 0
    while True:
        try: 
            while True:
                try:
                    message_list = driver.find_elements(By.XPATH, message_item_class_xpath)
                    if any(el.location['y'] < previous_first_message.location['y'] for el in message_list):
                        break
                    time.sleep(0.3)
                except StaleElementReferenceException:
                    time.sleep(0.3)
                    continue

            big_message_list = ''
            between_elements = [el for el in message_list if el.location['y'] < previous_first_message.location['y']]

            matching_id = False
            if last_message_id:
                for item in between_elements:
                    li = BeautifulSoup(item.get_attribute('outerHTML'), 'html.parser')
                    contents_div = li.find('div', class_='contents_c19a55')
                    if not contents_div:
                        continue
                    message_content_div = contents_div.find('div', id=re.compile(r'message-content-\d+'))
                    if not message_content_div:
                        continue
                    match = re.search(r'message-content-(\d+)', message_content_div.get('id'))
                    if not match:
                        continue
                    message_id = match.group(1)
                    if message_id == last_message_id:
                        matching_id = True
                    big_message_list += item.get_attribute('outerHTML')
                if matching_id:
                    parseHtml(big_message_list, temp_json_path)
                    finalCleanup(temp_json_path)
                    combine_json(json_path, temp_json_path)
                    sys.exit()

            for item in between_elements:
                big_message_list += item.get_attribute('outerHTML') 

            previous_first_message = message_list[0]
            driver.execute_script("arguments[0].scrollIntoView();", previous_first_message)
            driver.execute_script("arguments[0].setAttribute('style', 'background-color:red')", previous_first_message)
            scrolls += 1
            print(f'performing scroll {scrolls}', end='\r')
            parseHtml(big_message_list, json_path)
        except NoSuchElementException:
            print('no more elements')
            break
        except StaleElementReferenceException:
            print('stale element.. trying again XD')
            time.sleep(0.3)
            continue
        except KeyboardInterrupt:
            finalCleanup(json_path)

    finalCleanup(json_path)

def syncMessages():
    try:
        df = pd.read_json('resources/json/table_messages.json', orient='records', dtype=False)
    except FileNotFoundError:
        print('file not found..')

    last_message_id = df.iloc[-1]['message_id']
    discordScrape(last_message_id)



if __name__ == '__main__':
    load_dotenv()
    profile_directory = os.getenv('profile_directory')
    discord_channel_link = os.getenv('discord_channel_link')
    json_path = 'resources/json/table_messages.json'

    description = (
        "Discord Channel Scraper\n"
        "Github: https://github.com/Danvu772/discordScrape\n\n"
        "This script scrapes messages from a Discord channel using Selenium.\n"
        "It supports two modes:\n"
        "  - fullScrape: Scrape the entire channel history based on the Discord channel link in your .env file.\n"
        "  - sync: Scrape only new messages since the last saved message in the JSON file.\n\n"
        "Make sure to set the required environment variables in your .env file:\n"
        "  - profile_directory: Path to your Firefox profile for Selenium\n"
        "  - discord_channel_link: URL to the Discord channel to scrape"
    )

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter
)

    parser.add_argument(
    'action',
    choices=['fullScrape', 'sync'],
    help=(
        "Action to perform:\n"
        "  fullScrape     - Scrapes your entire channel history using channel link found in your .env file\n"
        "  sync           - Scrapes your channel history up until the last message found in table_messages.json"
    )
)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.action == 'fullScrape':
        discordScrape(None)
    elif args.action == 'sync':
        syncMessages()

    