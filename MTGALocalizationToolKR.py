import sqlite3
import glob
import os
import sys
import json
import unicodedata
# UI 오역 수정 파트

client_files = glob.glob('Raw_ClientLocalization_*.mtga')

if not client_files:
    print("파일을 찾을 수 없습니다. 게임폴더내 Raw 폴더에서 실행시켜 주세요")
    os.system("pause")
    sys.exit()

client_json_file_path = 'client_data.json'

# JSON 파일에서 데이터를 불러오기
with open(client_json_file_path, 'r', encoding='utf-8') as json_file:
    client_values_to_update = json.load(json_file)

for client_file in client_files:

    print(f"아래 파일에 접근 : {client_file}")
    try:
        client_conn = sqlite3.connect(client_file)
        client_cursor = client_conn.cursor()

        client_table_name = 'Loc'
        client_search_column = 'key'
        client_target_column = 'koKR'

        client_select_query = f"SELECT {client_search_column}, {client_target_column} FROM {client_table_name} WHERE {client_search_column} = ?"
        client_update_query = f"UPDATE {client_table_name} SET {client_target_column} = ? WHERE {client_search_column} = ?"

        for client in client_values_to_update:
            
            search_value = client['Key']
            new_value = client['KoKR']

            client_cursor.execute(client_select_query, (search_value,))
            rows = client_cursor.fetchall()

            if rows:
                # 찾은 행 업데이트
                client_cursor.execute(client_update_query, (new_value, search_value))
                print(f"{search_value}가 {new_value}로 변경되었습니다.")
            else:
                print(f"{client_search_column}에서 {search_value}를 찾지 못하였습니다.")


        client_conn.commit()
    except sqlite3.Error as e:
        print(f"{client_file}에서 에러 발생: {e}")
    finally: 
        if client_conn:
            client_conn.close()

# 카드 오역 수정파트

card_json_file_path = 'card_data.json'

# JSON 파일에서 데이터를 불러오기
with open(card_json_file_path, 'r', encoding='utf-8') as json_file:
    card_values_to_update = json.load(json_file)

def formatting_for_2(text):
    decomposed = ""
    for char in text:
        # 각 문자를 NFD 방식으로 정규화하여 초성, 중성, 종성으로 분리
        decomposed_char = unicodedata.normalize('NFD', char)
        decomposed += decomposed_char
    return decomposed

card_files = glob.glob('Raw_CardDatabase_*.mtga')

for card_file in card_files:

    print(f"아래 파일에 접근 : {card_file}")

    try:
        card_conn = sqlite3.connect(card_file)
        card_cursor = card_conn.cursor()

        card_table_name = 'Localizations'
        card_search_column = 'LocId'
        card_target_column = 'koKR'
        card_formatted_column = 'Formatted'
        card_name_en = 'enUS'
        card_name_kr = 'koKR'

        card_select_query = f"""
                SELECT {card_search_column}, {card_target_column}, {card_name_en}, {card_name_kr}, {card_formatted_column}
                FROM {card_table_name}
                WHERE {card_search_column} = ?
            """

        for card in card_values_to_update:
            search_value = card['LocId']
            value_for_0 = card['Formatted_0']
            value_for_1 = card['Formatted_1']
            value_for_2 = formatting_for_2(card['Formatted_0'])

            # 특정 값을 포함하는 행 찾기
            card_cursor.execute(card_select_query, (search_value,))
            rows = card_cursor.fetchall()

            if rows:
                formatted_values = {row[4] for row in rows}  # Formatted 값의 집합

                for row in rows:
                    formatted_value = row[4]
                    new_value = None
                    
                    if 0 in formatted_values and formatted_value == 0:
                        new_value = value_for_0
                    elif 0 in formatted_values and formatted_value == 1: 
                        if not value_for_1:
                            new_value = value_for_0
                        else:
                            new_value = value_for_1
                    elif 0 not in formatted_values and formatted_value == 1:
                        new_value = value_for_0
                    elif 2 in formatted_values and formatted_value == 2:
                        new_value = value_for_2
                    
                    if new_value:
                        card_cursor.execute(f"""
                            UPDATE {card_table_name}
                            SET {card_target_column} = ?
                            WHERE {card_search_column} = ?
                            AND {card_formatted_column} = ?
                        """, (new_value, search_value, formatted_value))
                        print(f"{row[3]}({row[2]})가 {new_value}로 변경되었습니다.\n")
            else:
                print(f"{search_value}에 해당하는 값을 찾지 못하였습니다.")

        card_conn.commit()

    except sqlite3.Error as e:
        print(f"{card_file}에서 에러 발생: {e}")

    finally: 
        if card_conn:
            card_conn.close()

print("패치가 완료되었습니다. 이용해주셔서 감사합니다.")   
os.system("pause")



