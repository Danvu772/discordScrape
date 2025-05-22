from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import unquote
from io import StringIO
import os
from tools import jsonClean

def parseHtml(html, json_path):
    
    soup = BeautifulSoup(html, 'html.parser')

    li_messages = soup.select('li')
    big_messages = []
    user_name = None  # None instead of empty string, to avoid carrying incorrect values

    for li in li_messages:
        message = {}
        try:
            user_name_h3 = li.find('h3')
            if user_name_h3:
                user_name_span = user_name_h3.find('span', class_='username_c19a55')
                if user_name_span:
                    user_name = user_name_span.get('data-text', user_name) 

            user_id_div = li.find('div', class_='message__5126c')
            if user_id_div:
                match = re.search(r'message-username-(\d+)', user_id_div.get('aria-labelledby'))
                user_id = match.group(1) if match else None

            if user_id is None and user_name_h3:
                message_username_span = user_name_h3.find('span', class_='headerText_c19a55')
                if message_username_span:
                    match = re.search(r'message-username-(\d+)', message_username_span.get('id'))
                    user_id = match.group(1) if match else None

            image_tag = li.find('a')
            contents_div = li.find('div', class_='contents_c19a55')
            if contents_div:
                message_content_div = contents_div.find('div', id=re.compile(r'message-content-\d+'))

            reply_id = None
            replied_text_div = li.find('div', class_='repliedTextPreview_c19a55')
            if replied_text_div:
                replied_content_div = replied_text_div.find('div', id=re.compile(r'message-content-\d+'))
                if replied_content_div:
                    match = re.search(r'message-content-(\d+)', replied_content_div.get('id'))
                    reply_id = match.group(1) if match else None

            if message_content_div:
                match = re.search(r'message-content-(\d+)', message_content_div.get('id'))
                message_id = match.group(1) if match else None
            else:
                print('fuck you')

            if image_tag and image_tag.has_attr('href'):
                content = image_tag.get('href')
            else:
                if contents_div:
                    message_content = contents_div.find('div', class_='messageContent_c19a55')
                    content = message_content.text.replace('\n', ' ').strip() if message_content else 'No content'
                    content = re.sub(r'\s+', ' ', content) 
                    content = unquote(content)  # Decode any encoded characters

            datetime_tag = li.find('time')
            datetime = datetime_tag.get('datetime') if datetime_tag else None  # Handle missing timestamp


            message['username'] = user_name if user_name else None 
            message['user_id'] = user_id if user_id else None
            message['message_id'] = message_id if message_id else None
            message['content'] = content if content else None 
            message['datetime'] = datetime if datetime else None
            message['reply_id'] = reply_id if reply_id else None

            big_messages.append(message)

        except Exception as e:
            print(f'Error processing message: {e}')


    # Convert to DataFrame and process dates safely
    df = pd.DataFrame(big_messages)
    df.to_json(json_path, mode='a', orient='records', lines=True, indent=4)
    
def finalCleanup(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        cleaned_json = file.read()

    cleaned_json = '[' + cleaned_json.replace('}\n', '},')[:-1] + ']'
    cleaned_json = cleaned_json.replace(',]', '\n]') 

    df = pd.read_json(StringIO(cleaned_json), orient='records', dtype=False)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df_sorted = df.sort_values(by='datetime', ascending=True)
    df_sorted.to_json(json_path, orient='records', indent=4)

    jsonClean.replaceName(json_path)
    jsonClean.postClean(json_path)

    print('finished cleanup')

def combine_json(json_path, temp_json):

        df1 = pd.read_json(json_path, orient='records', dtype=False)
        df2 = pd.read_json(temp_json, orient='records', dtype=False)

        combined = pd.concat([df1, df2], ignore_index=True)
        combined = combined.drop_duplicates(subset='message_id')

        combined.to_json(json_path, orient='records', indent=4)
        
        os.remove(temp_json)



def main():
    json_path = 'resources/json/table_messages.json'
    df = pd.read_json(json_path, orient='records', dtype=False)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df_sorted = df.sort_values(by='datetime', ascending=True)
    df_sorted.to_json(json_path, orient='records', indent=4)

    jsonClean.replaceName(json_path)
    jsonClean.postClean(json_path)



if __name__ == '__main__':
    json_path = 'resources/json/table_messages.json'
    df = pd.read_json(json_path, orient='records', dtype=False)

    print(len(df))