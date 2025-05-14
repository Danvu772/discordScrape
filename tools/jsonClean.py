import pandas as pd

df = pd.read_json('../resources/json/table_messages.json', orient='records')

'''
badRowCondition = (df['content'] == 'No content') & (df['datetime'].isna())

filtered = df[~badRowCondition]

filtered.to_json('table_messages.json', orient='records', indent=4)

df_filtered = df.drop_duplicates()


df_filtered.to_json('table_messages.json', orient='records', indent=4)
null_datetime_rows = df[df['datetime'].isna()]

duplicate_content = df[df['datetime'].notna()]['content']

filtered_df = df[~(df['datetime'].isna() & df['content'].isin(duplicate_content))]

filtered_df.to_json('table_messages.json', orient='records', indent=4)
'''

charlieM_rows = df[df['username'] == 'Charlie M']
charlieM_duplicated_content = charlieM_rows['content']

print(charlieM_duplicated_content)
print(len(charlieM_duplicated_content))

deletedRowBool = (df['username'] == 'Charlie M') & (df['content'].isin(charlieM_duplicated_content))

df_new = df[~deletedRowBool]


charlieM_rows = df_new[df_new['username'] == 'Charlie M']
charlieM_duplicated_content = charlieM_rows['content']

print(charlieM_duplicated_content)
print(len(charlieM_duplicated_content))
df_new.to_json('table_messages.json', orient='records', indent=4)