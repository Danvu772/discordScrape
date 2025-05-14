from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.common.exceptions import StaleElementReferenceException 
from dotenv import load_dotenv

load_dotenv()
profile_directory = os.getenv('profile_directory')
discord_channel_link = os.getenv('discord_channel_link')

def main():
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
    saveFile(previous_first_message.get_attribute('outerHTML'))
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
            for item in between_elements:
                big_message_list += item.get_attribute('outerHTML') 
            previous_first_message = message_list[0]
            driver.execute_script("arguments[0].scrollIntoView();", previous_first_message)
            driver.execute_script("arguments[0].setAttribute('style', 'background-color:red')", previous_first_message)
            scrolls += 1
            print(f'performing scroll {scrolls}', end='\r')
            saveFile(big_message_list)

        except NoSuchElementException:
            print('no more elements')
            break
        except StaleElementReferenceException:
            time.sleep(0.3)
            continue



def saveFile(htmlContent):
    with open('resources/html/tableScrape.html', 'a') as file:
        file.write(htmlContent)



main()