import pandas as pd

def replaceName(json_path):
    df = pd.read_json(json_path, dtype=False)
    df_chungus_replaced = df
    df_chungus_replaced['username'] = df_chungus_replaced['username'].str.replace('Chungus v2', 'Chungus')
    df_chungus_replaced['content'] = df_chungus_replaced['content'].str.replace('Chungus v2', 'Chungus')

    df_chungus_replaced['username'] = df_chungus_replaced['username'].str.replace('Vũ Thái huy', 'Dan')
    df_chungus_replaced['content'] = df_chungus_replaced['content'].str.replace('@Vũ Thái huy', '@Dan')

    df_chungus_replaced.to_json(json_path, orient='records', indent=4)

def postClean(json_path):
    df_sorted = pd.read_json(json_path, dtype=False)
    df_sorted = df_sorted[~(df_sorted['datetime'].isnull() & df_sorted['content'].isnull())]
    df = df_sorted
    duplicate_content = df[df['datetime'].notna()]['content']
    df_sorted = df[~(df['datetime'].isna() & df['content'].isin(duplicate_content))]

    df_sorted = df_sorted.drop_duplicates(keep=False)
    df_sorted.to_json(json_path, orient='records', indent=4)

if __name__ == '__main__':
    replaceName('../resources/json/table_messages.json')

