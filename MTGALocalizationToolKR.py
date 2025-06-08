import sqlite3
import glob
import os
import sys
import unicodedata
import requests 



# UI 오역 수정 파트

client_files = glob.glob('Raw_ClientLocalization_*.mtga')

if not client_files:
    print("파일을 찾을 수 없습니다. 게임폴더내 Raw 폴더에서 실행시켜 주세요")
    os.system("pause")
    sys.exit()

def get_resource_path(relative_path):
    try:
        # PyInstaller로 패키징된 경우
        base_path = sys._MEIPASS
    except AttributeError:
        # 일반적인 실행 환경일 경우
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 있는지 확인
        return response.json()  # JSON 데이터를 파싱하여 반환
    except requests.exceptions.RequestException as e:
        print(f"웹에서 데이터를 가져오는 중 오류 발생: {e}")
        sys.exit()

# JSON 데이터를 웹에서 가져오기
print("데이터 불러오는중...")
client_json_url = "https://docs.google.com/uc?export=download&id=1oOqAmmoyJ9FJZsrWccMoLjMchAatWtou&confirm=t" 
client_values_to_update = fetch_json_from_url(client_json_url)
card_json_url = "https://docs.google.com/uc?export=download&id=1pSF_YCV0NPuy240Rtt0bzOmr1GyE5HMd&confirm=t"
card_values_to_update = fetch_json_from_url(card_json_url)


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

    card_table_name = 'Localizations'
    card_search_column = 'LocId'
    card_target_column = 'koKR'
    card_formatted_column = 'Formatted'
    card_name_en = 'enUS'
    card_name_kr = 'koKR'

    try:
        card_conn = sqlite3.connect(card_file)
        card_cursor = card_conn.cursor()

        # 사전 로딩
        card_cursor.execute("SELECT Id, TextId FROM abilities")
        textid_to_abilityid = {
            str(text_id).strip(): str(ability_id).strip()
            for ability_id, text_id in card_cursor.fetchall()
        }

        card_cursor.execute("SELECT HiddenAbilityIds, AbilityIds FROM cards")
        ability_to_b_ids = {}
        for hid_ids, main_ids in card_cursor.fetchall():
            for raw in (hid_ids, main_ids):
                if not raw:
                    continue
                for pair in raw.split(','):
                    if ':' not in pair:
                        continue
                    A, B = pair.split(':', 1)
                    A = str(A).strip()
                    B = str(B).strip()
                    ability_to_b_ids.setdefault(A, []).append(B)

        card_cursor.execute("SELECT LocId, Loc FROM Localizations_koKR")
        ko_loc_map = {str(row[0]).strip(): row[1] for row in card_cursor.fetchall()}

        card_cursor.execute("SELECT LocId, Loc FROM Localizations_enUS")
        en_loc_map = {str(row[0]).strip(): row[1] for row in card_cursor.fetchall()}

        card_cursor.execute("""
            SELECT LocId FROM Localizations_koKR 
            WHERE Loc IN ('#NoTranslationNeeded', '#NoTransNeeded')
        """)
        no_trans_ids = [str(row[0]).strip() for row in card_cursor.fetchall()]

        for no_trans_id in no_trans_ids:
            ability_id = textid_to_abilityid.get(no_trans_id)

            if not ability_id:
                en_loc = en_loc_map.get(no_trans_id)
                if en_loc and ko_loc_map.get(no_trans_id) in ['#NoTranslationNeeded', '#NoTransNeeded']:
                    card_cursor.execute("""
                        UPDATE Localizations_koKR
                        SET Loc = ?
                        WHERE LocId = ?
                    """, (en_loc, no_trans_id))
                continue

            translated = False
            for b_id in ability_to_b_ids.get(ability_id, []):
                new_loc = ko_loc_map.get(b_id)
                if new_loc and new_loc not in ['#NoTranslationNeeded', '#NoTransNeeded']:
                    card_cursor.execute("""
                        UPDATE Localizations_koKR
                        SET Loc = ?
                        WHERE LocId = ?
                    """, (new_loc, no_trans_id))
                    translated = True
                    break

            if not translated:
                en_loc = en_loc_map.get(no_trans_id)
                if en_loc and ko_loc_map.get(no_trans_id) in ['#NoTranslationNeeded', '#NoTransNeeded']:
                    card_cursor.execute("""
                        UPDATE Localizations_koKR
                        SET Loc = ?
                        WHERE LocId = ?
                    """, (en_loc, no_trans_id))


    # HTML 태그 치환
        card_cursor.execute("""
            SELECT LocId, Loc
            FROM Localizations_koKR
            WHERE Loc LIKE '%&lt;%' OR Loc LIKE '%&gt;%'
        """)

        rows_to_update = card_cursor.fetchall()

        print(f"치환 대상 행 개수: {len(rows_to_update)}")

        # 2. 한 행씩 치환하고 업데이트 수행
        for loc_id, loc_text in rows_to_update:
            new_loc_text = loc_text.replace('&lt;', '<').replace('&gt;', '>')
            if new_loc_text != loc_text:
                card_cursor.execute("""
                    UPDATE Localizations_koKR
                    SET Loc = ?
                    WHERE LocId = ?
                """, (new_loc_text, loc_id))


#직접 입력한 오역 수정파트 
        for card in card_values_to_update:
            search_value = card['LocId']
            value_for_0 = card['Formatted_0']
            value_for_1 = card['Formatted_1']
            value_for_2 = formatting_for_2(card['Formatted_0'])

            card_cursor.execute("""
                SELECT LocId, Loc, Formatted
                FROM Localizations_koKR
                WHERE LocId = ?
            """, (search_value,))
            rows = card_cursor.fetchall()

            if rows:
                formatted_values = {row[2] for row in rows}  # Formatted column
                for row in rows:
                    formatted_value = row[2]
                    new_value = None

                    if 0 in formatted_values and formatted_value == 0:
                        new_value = value_for_0
                    elif 0 in formatted_values and formatted_value == 1:
                        new_value = value_for_1 if value_for_1 else value_for_0
                    elif 0 not in formatted_values and formatted_value == 1:
                        new_value = value_for_0
                    elif 2 in formatted_values and formatted_value == 2:
                        new_value = value_for_2

                    if new_value and row[1] != new_value:
                        card_cursor.execute("""
                            UPDATE Localizations_koKR
                            SET Loc = ?
                            WHERE LocId = ? AND Formatted = ?
                        """, (new_value, search_value, formatted_value))
                
                    if formatted_value != 2 :
                        print(f"{row[1]}가 {new_value}로 변경되었습니다.\n")

        card_conn.commit()

    except sqlite3.Error as e:
        print(f"{card_file}에서 에러 발생: {e}")

    finally: 
        if card_conn:
            card_conn.close()

print("패치가 완료되었습니다. 이용해주셔서 감사합니다.")   
os.system("pause")



