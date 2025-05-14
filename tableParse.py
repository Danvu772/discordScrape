from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import unquote
import time

print(f'started at {time.strftime('%Y-%m-%d %H:%M:%S')}')

with open('resources/html/tableScrape.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

print(f'finished loading soup at {time.strftime('%Y-%m-%d %H:%M:%S')}')

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
            else:
                with open('invalidH3.html', 'a') as file:
                    file.write(str(user_name_h3))

        image_tag = li.find('a')
        if image_tag and image_tag.has_attr('href'):
            content = image_tag.get('href')
        else:
            contents_div = li.find('div', class_='contents_c19a55')
            if contents_div:
                message_content = contents_div.find('div', class_='messageContent_c19a55')
                content = message_content.text.replace("\n", " ").strip() if message_content else "No content"
                content = re.sub(r'\s+', ' ', content) 
                content = unquote(content)  # Decode any encoded characters

        datetime_tag = li.find('time')
        datetime = datetime_tag.get('datetime') if datetime_tag else None  # Handle missing timestamp

        message['username'] = user_name if user_name else "Unknown User"
        message['content'] = content if content else "No content"
        message['datetime'] = datetime if datetime else "Unknown Timestamp"

        big_messages.append(message)

    except Exception as e:
        print(f"Error processing message: {e}")

print(f'finished processing all messages at {time.strftime('%Y-%m-%d %H:%M:%S')}')

# Convert to DataFrame and process dates safely
df = pd.DataFrame(big_messages)
print(f'finished loading the pandas dataframe at {time.strftime('%Y-%m-%d %H:%M:%S')}')
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')  # Avoid errors from bad timestamps
print(f'finished fixing datetime values at {time.strftime('%Y-%m-%d %H:%M:%S')}')
df_sorted = df.sort_values(by='datetime', ascending=True)
print(f'finished sorting by datetime at {time.strftime('%Y-%m-%d %H:%M:%S')}')
df_sorted.to_json('resources/json/table_messages.json', orient='records', indent=4)
print(f'finished saving to json at {time.strftime('%Y-%m-%d %H:%M:%S')}')
print("Messages successfully extracted and saved to JSON.")