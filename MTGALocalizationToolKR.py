import sqlite3
import glob

# UI 오역 수정 파트

client_files = glob.glob('Raw_ClientLocalization_*.mtga')

for client_file in client_files:

    print(f"아래 파일에 접근 : {client_file}")
    try:
        client_conn = sqlite3.connect(client_file)
        client_cursor = client_conn.cursor()

        client_table_name = 'Loc'
        client_search_column = 'key'
        client_target_column = 'koKR'

        client_values_to_update = [
            ('AbilityHanger/Keyword/Perpetual_Body', '영구 효과는 영역이 변경되더라도 카드로부터 제거되지 않는다.'),
            ('AbilityHanger/LayeredEffect/PerpetualPowerToughness_Title', '영구적인 공격력 및 방어력 변경'),
            ('AbilityHanger/Keyword/Perpetual_Title', '영구'),
            ('DuelScene/ClientPrompt/ExaminePerpetual', '영구 카드 보기'),
            ('DuelScene/FaceHanger/Conjure', '부르기'),
            ('AbilityHanger/Keyword/Conjure_Title', '부르기'),
            ('AbilityHanger/Keyword/Conjure_Body', '부르기한 카드가 게임에 추가됩니다.'),
            ('AbilityHanger/Keyword/Discover10_Body', '마나 비용이 10 이하인 대지가 아닌 카드를 추방할 때까지 서고 맨 위의 카드를 추방한다. 당신은 해당 카드를 마나 비용 없이 발동하거나 손으로 가져갈 수 있다. 나머지 카드는 서고 맨 밑에 무작위 순서로 추가한다.'),
            ('AbilityHanger/Keyword/Discover3_Body', '마나 비용이 3 이하인 대지가 아닌 카드를 추방할 때까지 서고 맨 위의 카드를 추방한다. 당신은 해당 카드를 마나 비용 없이 발동하거나 손으로 가져갈 수 있다. 나머지 카드는 서고 맨 밑에 무작위 순서로 추가한다.'),
            ('AbilityHanger/Keyword/Discover4_Body', '마나 비용이 4 이하인 대지가 아닌 카드를 추방할 때까지 서고 맨 위의 카드를 추방한다. 당신은 해당 카드를 마나 비용 없이 발동하거나 손으로 가져갈 수 있다. 나머지 카드는 서고 맨 밑에 무작위 순서로 추가한다.'),
            ('AbilityHanger/Keyword/Discover5_Body', '마나 비용이 5 이하인 대지가 아닌 카드를 추방할 때까지 서고 맨 위의 카드를 추방한다. 당신은 해당 카드를 마나 비용 없이 발동하거나 손으로 가져갈 수 있다. 나머지 카드는 서고 맨 밑에 무작위 순서로 추가한다.'),
            ('AbilityHanger/Keyword/DiscoverX_Body', '마나 비용이 X 이하인 대지가 아닌 카드를 추방할 때까지 서고 맨 위의 카드를 추방한다. 당신은 해당 카드를 마나 비용 없이 발동하거나 손으로 가져갈 수 있다. 나머지 카드는 서고 맨 밑에 무작위 순서로 추가한다.'),
            ('AbilityHanger/PhyrexianMana_Title', '피렉시아 마나'),
        ]

        client_select_query = f"SELECT {client_search_column}, {client_target_column} FROM {client_table_name} WHERE {client_search_column} = ?"
        client_update_query = f"UPDATE {client_table_name} SET {client_target_column} = ? WHERE {client_search_column} = ?"

        for search_value, new_value in client_values_to_update:
            # 특정 값을 포함하는 행 찾기
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

        # LocId, Value, Formatted Value 
        card_values_to_update = [
            # v1.1
            ('811472', '당신의 턴 전투 시작에, 당신이 조종하는 생쥐를 목표로 정한다. 그 생물은 턴종료까지 이단공격 또는 돌진 중 당신이 선택한 능력을 얻는다.', ''),
            ('811169', '문턱 — 당신의 무덤에 카드가 일곱 장 이상 있는 한, 밤소용돌이 은둔자는 +1/+0을 받고 방어될 수 없다.', '<i>문턱</i><nobr> —</nobr> 당신의 무덤에 카드가 일곱 장 이상 있는 한, 밤소용돌이 은둔자는 <nobr>+1/+0</nobr>을 받고 방어될 수 없다.'),
            ('811168', '문턱 — 당신의 무덤에 카드가 일곱 장 이상 있는 한, CARDNAME는 +1/+0을 받고 방어될 수 없다.', '<i>문턱</i><nobr> —</nobr> 당신의 무덤에 카드가 일곱 장 이상 있는 한, CARDNAME는 <nobr>+1/+0</nobr>을 받고 방어될 수 없다.'),
            ('90919', '대지가 아닌 지속물을 최대 두 개까지 목표로 정한다. 그 목표들을 소유자의 손으로 되돌린다.', ''),
            ('810878', '당신의 전투후 본단계 시작에, 당신이 이 턴에 생명 4점 이상을 얻었다면, 이름이 목스 진주인 카드를 당신의 손으로 부른다. 이 능력은 한 번만 격발한다.', ''),
            ('810886', '당신의 전투후 본단계 시작에, 당신의 무덤에 카드가 네 장 이상 있다면, 이름이 목스 흑옥인 카드를 당신의 손으로 부른다. 이 능력은 한 번만 격발한다.', ''),
            ('748889', '장착된 생물은 +1/+2를 받고 대공을 가지며, 생물 한개에게만 방어될 수 있다.', '장착된 생물은 <nobr>+1/+2</nobr>를 받고 대공을 가지며, 생물 한개에게만 방어될 수 있다.'),
            ('748904', '돌진을 가진 0/0 녹색 점액괴물 생물 토큰 한 개를 만든다. 그 생물에 +1/+1 카운터 X개를 올려놓는다. X는 2에 더해 추방 영역에서 당신이 소유한 카드 및 당신의 무덤에 있는 카드들 중 점액괴물이거나 이름이 반인륜적인 슬라임인 카드의 수다.', '돌진을 가진 0/0 녹색 점액괴물 생물 토큰 한 개를 만든다. 그 생물에 <nobr>+1/+1</nobr> 카운터 X개를 올려놓는다. X는 2에 더해 추방 영역에서 당신이 소유한 카드 및 당신의 무덤에 있는 카드들 중 점액괴물이거나 이름이 반인륜적인 슬라임인 카드의 수다.'),
            ('748696', '생물이 피해를 입을 때마다, 그 생물의 조종자는 자신의 서고 맨 위에서 그만큼 카드를 추방할 수 있다. 그 플레이어는 자신의 다음 턴 턴종료까지 그 카드들을 플레이할 수 있다.', ''),
            ('749115', '당신의 종료단 시작에, 이 턴에 생명점을 잃은 각 상대에 대해 조사한다.', ''),
            ('748863', '우리들 중의 살인자를 희생한다, 당신이 선택한 생물 유형을 공개한다: 공격 중인 생물 토큰을 목표로 정한다. 그 생물이 선택된 유형이면, 그 생물에 +1/+1 카운터 세 개를 올려놓고 그 생물은 턴종료까지 치명타를 얻는다.', '우리들 중의 살인자를 희생한다, 당신이 선택한 생물 유형을 공개한다: 공격 중인 생물 토큰을 목표로 정한다. 그 생물이 선택된 유형이면, 그 생물에 <nobr>+1/+1</nobr> 카운터 세 개를 올려놓고 그 생물은 턴종료까지 치명타를 얻는다.'),
            ('748862', 'CARDNAME를 희생한다, 당신이 선택한 생물 유형을 공개한다: 공격 중인 생물 토큰을 목표로 정한다. 그 생물이 선택된 유형이면, 그 생물에 +1/+1 카운터 세 개를 올려놓고 그 생물은 턴종료까지 치명타를 얻는다.', 'CARDNAME를 희생한다, 당신이 선택한 생물 유형을 공개한다: 공격 중인 생물 토큰을 목표로 정한다. 그 생물이 선택된 유형이면, 그 생물에 <nobr>+1/+1</nobr> 카운터 세 개를 올려놓고 그 생물은 턴종료까지 치명타를 얻는다.'),
            ('749036', '인간 페어리 탐정', ''),
            ('866789', '당신은 메아리치는 심해가 무덤에 있는 대지 카드의 복사본이지만 자신의 다른 유형에 더불어 동굴인 대지로 탭된 채로 들어오게 할 수 있다.', ''),
            ('866788', '당신은 CARDNAME가 무덤에 있는 대지 카드의 복사본이지만 자신의 다른 유형에 더불어 동굴인 대지로 탭된 채로 들어오게 할 수 있다.', ''),
            ('866018', '연글라이더 절도범이 들어올 때, 각 플레이어에 대해, 그 플레이어가 조종하는 다른 마법물체 또는 생물을 최대 한 개까지 선택한다. 연글라이더 절도범이 전장에 남아있는 한, 선택된 지속물들은 "{oT}, 이 마법물체를 희생한다: 원하는 색의 마나 한 개를 추가한다."를 가진 보물 마법물체가 되며 다른 모든 능력을 잃는다.', ''),
            ('866017', 'CARDNAME이 들어올 때, 각 플레이어에 대해, 그 플레이어가 조종하는 다른 마법물체 또는 생물을 최대 한 개까지 선택한다. CARDNAME이 전장에 남아있는 한, 선택된 지속물들은 "{oT}, 이 마법물체를 희생한다: 원하는 색의 마나 한 개를 추가한다."를 가진 보물 마법물체가 되며 다른 모든 능력을 잃는다.', ''),
            ('738033', '한 개 이상을 사용한 제작 {o5}', ''),
            ('737111', '당신의 조종하에 한 개 이상의 생물 토큰이 만들어지려 한다면, 대신 그 세 배만큼의 토큰이 만들어진다.', ''),
            ('737222', '당신이 조종하는 토큰이 아닌 인어가 한 개 이상 탭될 때마다, 방호를 가진 1/1 청색 인어 생물 토큰 한 개를 만든다.', ''),
            ('865927', '불안정한 상형문자다리가 들어올 때, 당신이 불안정한 상형문자다리를 발동했다면, 각 플레이어에 대해, 그 플레이어가 조종하며 공격력이 2 이하인 생물 한 개를 선택한다. 그 후 이런 식으로 선택된 생물들을 제외한 모든 생물을 파괴한다.', ''),
            ('865926', 'CARDNAME가 들어올 때, 당신이 CARDNAME를 발동했다면, 각 플레이어에 대해, 그 플레이어가 조종하며 공격력이 2 이하인 생물 한 개를 선택한다. 그 후 이런 식으로 선택된 생물들을 제외한 모든 생물을 파괴한다.', ''),
            ('865892', '유혈 전도사가 들어오거나 죽을 때, 비행을 가진 1/1 흑색 박쥐 생물 토큰 한 개를 만든다.', ''),
            ('865891', 'CARDNAME가 들어오거나 죽을 때, 비행을 가진 1/1 흑색 박쥐 생물 토큰 한 개를 만든다.', ''),
            ('755565', '당신의 종료단 시작에, 당신은 당신이 조종하는 다른 마법물체 또는 당신의 무덤에 있는 마법물체 카드 한 장을 추방할 수 있다. 그렇게 한다면, 마법물체 카드 한 장을 탐색한다. 그 카드는 영구적으로 기본 공격력 및 방어력이 1/1이 되며 자신의 다른 유형에 더불어 놈 생물이 된다.', ''),
            ('731412', '플레이어를 목표로 정한다. 그 플레이어는 자신의 서고 맨 위 X장을 추방한다. X는 추방 영역에 있는 카드들 중 당신이 소유한 카드들이 가진 마나 값의 총합이다.', ''),
            ('875165', '이번 게임에서 당신의 첫 세 턴 동안, 당신이 시작플레이어 였다면 매혹적인 교차로는 탭된 채로 들어온다.', ''),
            ('875164', '이번 게임에서 당신의 첫 세 턴 동안, 당신이 시작플레이어 였다면 CARDNAME는 탭된 채로 들어온다.', ''),
            ('703263', '상대가 조종하는 주문 또는 대지가 아닌 지속물을 목표로 정한다. 그 목표를 소유자의 손으로 되돌린다. 당신은 당신의 손에서 마나 값이 목표의 마나 값 이하인 순간마법 또는 집중마법 주문 한 개를 그 주문의 마나 비용을 지불하지 않고 발동할 수 있다.', ''),
            ('704233', '지리나를 희생한다: 당신이 조종하는 인간들은 턴종료까지 방호 및 무적을 얻는다.', ''),
            ('683792', '{o3o(W/P)}: 독성 1과 "이 생물은 방어할 수 없다."를 가진 1/1 무색 피렉시아 진드기 마법물체 생물 토큰 한 개를 만든다.', ''),
            ('729545', '흉포한 육식생물, 교스', ''),
            ('701484', '대사막 헬리온이 전장을 떠날 때, 당신은 손을 버릴 수 있다. 그렇게 한다면, 대사막 헬리온의 강도만큼 카드를 뽑는다.', ''),
            ('701483', 'CARDNAME이 전장을 떠날 때, 당신은 손을 버릴 수 있다. 그렇게 한다면, CARDNAME의 강도만큼 카드를 뽑는다.', ''),
            ('604724', '폭풍의 복사, 클레멘트가 피해를 입을 때마다, 원하는 목표를 정한다. 클레멘트는 그 목표에게 그만큼 피해를 입힌다.', ''),
            ('233577', 'CARDNAME가 피해를 입을 때마다, 원하는 목표를 정한다. CARDNAME는 그 목표에게 그만큼 피해를 입힌다.', ''),
            ('854997', '산업의 카미가 들어올 때, 당신의 무덤에 있는 마나 값이 3 이하인 마법물체 카드를 목표로 정한다. 그 카드를 전장으로 되돌린다. 그 마법물체는 신속을 얻는다. 다음 종료단 시작에 그 마법물체를 희생한다.', ''),
            ('854996', 'CARDNAME가 들어올 때, 당신의 무덤에 있는 마나 값이 3 이하인 마법물체 카드를 목표로 정한다. 그 카드를 전장으로 되돌린다. 그 마법물체는 신속을 얻는다. 다음 종료단 시작에 그 마법물체를 희생한다.', ''),
            ('546078', '각 종료단 시작에, 당신이 조종하지 않는 각 생물에 점액 카운터를 한 개씩 올려놓는다.', ''),
            ('545949', '눈알 괴수', ''),
            ('529670', '당신이 공격할 때마다, 각 상대에 대해, 탭되어 그 플레이어 또는 그 플레이어가 조종하는 플레인즈워커를 공격 중인 1/1 백색 인간 생물 토큰 한 개를 만든다.', ''),
            ('566461', '{o1o(B/G)}, 당신의 무덤에서 카드 두 장을 추방한다: 무리어미, 이쉬카나의 주문서에서 카드 한 장을 드래프트한다.', ''),
            ('487830', '{o3oB}: 당신이 조종하는 다람쥐들은 턴종료까지 +1/+0을 받고 호전적을 얻는다.', '{o3oB}: 당신이 조종하는 다람쥐들은 턴종료까지 <nobr>+1/+0</nobr>을 받고 호전적을 얻는다.'),
            ('488728', '헌신적인 상형문자 방직공을 추방한다: 당신이 조종하는 생물들은 턴종료까지 무적을 얻는다.', ''),
            ('488727', 'CARDNAME을 추방한다: 당신이 조종하는 생물들은 턴종료까지 무적을 얻는다.', ''),
            ('477799', '상대가 조종하는 지속물이 전장에서 무덤에 놓일 때마다, 세계 포식자, 사룰프에 +1/+1 카운터 한 개를 올려놓는다.', '상대가 조종하는 지속물이 전장에서 무덤에 놓일 때마다, 세계 포식자, 사룰프에 <nobr>+1/+1</nobr> 카운터 한 개를 올려놓는다.'),
            ('477798', '상대가 조종하는 지속물이 전장에서 무덤에 놓일 때마다, CARDNAME에 +1/+1 카운터 한 개를 올려놓는다.', '상대가 조종하는 지속물이 전장에서 무덤에 놓일 때마다, CARDNAME에 <nobr>+1/+1</nobr> 카운터 한 개를 올려놓는다.'),
            ('477389', '부여된 생물은 기본 공격력이 0이 되고 "당신의 유지단 시작에, 당신은 이 생물을 희생하지 않는 한 생명 1점을 잃는다."를 가진다.', ''),
            ('477849', '당신의 유지단 시작에, 복제하는 반지에 밤 카운터 한 개를 올려놓는다. 그 후 복제하는 반지에 밤 카운터가 여덟 개 이상 놓여 있다면, 그 카운터들을 모두 제거하고 "{oT}: 원하는 색의 마나 한 개를 추가한다."를 가졌으며 이름이 복제된 반지인 무색 눈 마법물체 토큰 여덟 개를 만든다.', ''),
            ('477848', '당신의 유지단 시작에, CARDNAME에 밤 카운터 한 개를 올려놓는다. 그 후 CARDNAME에 밤 카운터가 여덟 개 이상 놓여 있다면, 그 카운터들을 모두 제거하고 "{oT}: 원하는 색의 마나 한 개를 추가한다."를 가졌으며 이름이 복제된 반지인 무색 눈 마법물체 토큰 여덟 개를 만든다.', ''),
            ('478037', '복제된 반지', ''),
            ('483854', '처녀림 트롤이 죽을 때, 처녀림 트롤이 생물이었다면, 처녀림 트롤을 전장으로 되돌린다. 처녀림 트롤은 당신이 조종하는 숲에 부여 및 "부여된 숲은 \'{oT}: {oGoG}를 추가한다.\' 및 \'{o1}, {oT}, 이 대지를 희생한다: 돌진을 가진 탭된 4/4 녹색 트롤 전사 생물 토큰 한 개를 만든다.\'를 가진다."를 가진 마법진 부여마법이다.', ''),
            ('483853', 'CARDNAME이 죽을 때, CARDNAME이 생물이었다면, CARDNAME을 전장으로 되돌린다. CARDNAME은 당신이 조종하는 숲에 부여 및 "부여된 숲은 \'{oT}: {oGoG}를 추가한다.\' 및 \'{o1}, {oT}, 이 대지를 희생한다: 돌진을 가진 탭된 4/4 녹색 트롤 전사 생물 토큰 한 개를 만든다.\'를 가진다."를 가진 마법진 부여마법이다.', ''),
            ('477515', '장착된 생물은 "{o1oR}, {oT}, 토랄프의 망치를 분리한다: 원하는 목표를 정한다. 토랄프의 망치는 그 목표에게 피해 3점을 입힌다. 토랄프의 망치를 소유자의 손으로 되돌린다."를 가진다.', ''),
            ('477514', '{o1oR}, {oT}, 토랄프의 망치를 분리한다: 원하는 목표를 정한다. 토랄프의 망치는 그 목표에게 피해 3점을 입힌다. 토랄프의 망치를 소유자의 손으로 되돌린다.', ''),
            ('477516', '장착된 생물은 전설적인 한 +3/+0을 받는다.', '장착된 생물은 전설적인 한 <nobr>+3/+0</nobr>을 받는다.'),
            ('562047', '{oT}, 토모드의 묘소를 희생한다: 플레이어를 목표로 정한다. 그 플레이어의 무덤을 추방한다.', ''),
            ('562046', '{oT}, CARDNAME를 희생한다: 플레이어를 목표로 정한다. 그 플레이어의 무덤을 추방한다.', ''),
            ('441358', '무리 대장이 공격할 때마다, 이번 턴에 당신이 조종하는 개들에게 입혀질 모든 전투피해를 방지한다.', ''),
            ('441357', 'CARDNAME이 공격할 때마다, 이번 턴에 당신이 조종하는 개들에게 입혀질 모든 전투피해를 방지한다.', ''),
            ('43274', '부여마법, 순간마법 또는 집중마법 주문을 목표로 정한다. 그 주문을 무효화한다. 그 주문의 조종자는 비행을 가진 2/2 청색 조류 생물 토큰 한 개를 만든다.', ''),
            ('234538', '정의의 집정관이 죽을 때, 지속물을 목표로 정한다. 그 지속물을 추방한다.', ''),
            ('56220', 'CARDNAME이 죽을 때, 지속물을 목표로 정한다. 그 지속물을 추방한다.', ''),
            ('428543', '돌연변이화 {o3o(G/U)o(G/U)}', ''),
            ('17799', '당신이 인어 주문을 발동할 때마다, 지속물을 목표로 정한다. 당신은 그 지속물을 탭 또는 언탭할 수 있다.', ''),
            ('414585', '당신이 조종하는 장착된 생물이 공격할 때마다, 당신은 카드 한 장을 뽑고 생명 1점을 잃는다.', ''),
            ('336947', '"이 생물이 플레인즈워커에게 피해를 입힐 때마다, 그 플레인즈워커를 파괴한다." 및 치명타를 가진 1/1 흑색 암살자 생물 토큰 한 개를 만든다.', ''),
            ('336946', '이 생물이 플레인즈워커에게 피해를 입힐 때마다, 그 플레인즈워커를 파괴한다.', ''),
            ('835509', '억류 대리인이 들어올 때, 상대가 조종하는 대지가 아닌 지속물을 목표로 정한다. 그 지속물 및 그 지속물을 조종하는 플레이어의 지속물 중 그 지속물과 이름이 같은 모든 대지가 아닌 지속물을 억류 대리인이 전장을 떠날 때까지 추방한다.', ''),
            ('835508', 'CARDNAME이 들어올 때, 상대가 조종하는 대지가 아닌 지속물을 목표로 정한다. 그 지속물 및 그 지속물을 조종하는 플레이어의 지속물 중 그 지속물과 이름이 같은 모든 대지가 아닌 지속물을 CARDNAME이 전장을 떠날 때까지 추방한다.', ''),
            # 탐색 파트
            ('810826', '{oT}, 룬이 새겨진 오벨리스크를 희생한다: 당신의 서고에서 마나 값이 X 이하인 카드들 중 가장 높은 마나 값을 가진 카드 한 장을 탐색한다. X는 룬이 새겨진 오벨리스크에 놓인 충전 카운터의 수다.', ''),
            ('810825', '{oT}, CARDNAME를 희생한다: 당신의 서고에서 마나 값이 X 이하인 카드들 중 가장 높은 마나 값을 가진 카드 한 장을 탐색한다. X는 CARDNAME에 놓인 충전 카운터의 수다.', ''),
            ('810898', '주문을 목표로 정한다. 그 주문의 조종자가 {o2}을(를) 지불하지 않는 한 그 주문을 무효화한다. 문턱 — 당신의 무덤에 카드가 일곱 장 있다면, 선택된 주문과 마나 값이 같은 생물 카드 한 장을 탐색한다.', '주문을 목표로 정한다. 그 주문의 조종자가 {o2}을(를) 지불하지 않는 한 그 주문을 무효화한다. <i>문턱</i><nobr> —</nobr> 당신의 무덤에 카드가 일곱 장 있다면, 선택된 주문과 마나 값이 같은 생물 카드 한 장을 탐색한다.'),
            ('875325', '당신이 조종하는 다른 생물이 들어올 때마다, 그 생물의 공격력이 4 이상이라면 그 생물은 영구적으로 신속을 얻는다. 그 생물의 방어력이 4 이상이라면, 당신은 생명 4점을 얻는다. 그 생물의 마나 값이 4 이상이라면, 생물 카드 한 장을 탐색한다.', ''),
            ('810843', '당신의 무덤에 있는 생물 카드를 최대 두 장까지 목표로 정한다. 그 카드들을 당신의 손으로 되돌린 후, 생물이 아니고 대지가 아닌 카드 두 장을 탐색한다.', ''),
            ('810840', '당신이 조종하는 생물이 공격할 때마다, 대지가 아닌 카드 두 장을 탐색한 후, 카드 한 장을 버린다.', ''),
            ('793426', '낄낄대는 관찰자가 전장을 떠날 때, 추방된 카드의 소유자는 추방된 카드보다 적은 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.', ''),
            ('793425', 'CARDNAME가 전장을 떠날 때, 추방된 카드의 소유자는 추방된 카드보다 적은 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.', ''),
            ('793411', '{o1}, 단서 한 개를 희생한다: 순간마법 또는 집중마법 카드 한 장을 탐색한다.', ''),
            ('793398', '탐정 강사 또는 당신이 조종하는 다른 지속물이 앞면으로 뒤집힐 때마다, 마나 값이 3 이하이며 코끼리가 아닌 생물 카드 한 장을 탐색하고 그 카드를 비닉한다. 이 능력은 한 번만 격발한다.', ''),
            ('793397', 'CARDNAME 또는 당신이 조종하는 다른 지속물이 앞면으로 뒤집힐 때마다, 마나 값이 3 이하이며 코끼리가 아닌 생물 카드 한 장을 탐색하고 그 카드를 비닉한다. 이 능력은 한 번만 격발한다.', ''),
            ('755621', '카드 한 장을 뽑는다. 이 주문을 발동하는 데 보물에서 생성된 마나가 지불되었다면, 대신 해적 카드 한 장을 탐색한다.', ''),
            ('755597', '카드 한 장을 뽑는다. 이 턴에 상대가 생명점을 잃었고 당신이 생명점을 얻었다면, 대신 흡혈귀 카드 두 장을 탐색한다.', ''),
            ('755591', '마나 값이 X 이하이며 대지가 아닌 마법물체 카드 한 장을 탐색해 그 카드를 전장에 놓는다. 마나 값이 X 미만인 카드가 이런 식으로 전장에 놓였다면, 이 주문은 영구적으로 "이 주문은 발동하는 데 {o1}이(가) 더 든다."를 얻은 후 이 주문을 소유자의 손으로 되돌린다.', ''),
            ('755582', '카드 한 장을 뽑는다. 당신이 조종한 지속물이 이 턴에 탐험했다면, 대신 인어 카드 한 장을 탐색한다.', ''),
            ('751536', '당신의 서고 맨 위 열 장 중에서 생물 카드 두 장을 탐색한 후, 서고를 섞는다. 당신의 손에 있는 생물 카드들은 영구적으로 +1/+1을 받는다.', ''),
            ('751462', '당신의 손에 있는 카드의 수보다 적은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('751463', '당신의 손에 있는 카드의 수보다 큰 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('751455', '당신의 턴 전투후 본단계 시작에, 당신이 이 턴에 생명점을 얻었다면, 마나 값이 당신이 이 턴에 얻은 생명점 이하인 카드들 중에서 마나 값이 가장 높은 카드 한 장을 탐색한다.', ''),
            ('729576', '당신이 카드를 한 장 이상 탐색할 때마다, 3/3 무색 피렉시아 골렘 마법물체 생물 토큰 한 개를 만든다.', ''),
            ('729556', '당신이 조종하는 마법물체 생물 한 개 이상이 플레이어에게 전투피해를 입힐 때마다, 마나 값이 2 이하이며 대지가 아닌 카드 한 장을 탐색한다.', ''),
            ('729630', '당신의 유지단 시작에, 번들거리는 추출기에 기름 카운터가 한 개 이상 놓여있다면, 마나 값이 번들거리는 추출기에 놓인 기름 카운터의 수와 같은 카드 한 장을 탐색한 후, 번들거리는 추출기에서 기름 카운터 한 개를 제거한다.', ''),
            ('729629', '당신의 유지단 시작에, CARDNAME에 기름 카운터가 한 개 이상 놓여있다면, 마나 값이 CARDNAME에 놓인 기름 카운터의 수와 같은 카드 한 장을 탐색한 후, CARDNAME에서 기름 카운터 한 개를 제거한다.', ''),
            ('729523', '{o1}, {oT}, 생물 한 개를 희생한다: 희생된 생물의 마나 값에 1을 더한 수와 같은 마나 값을 가진 생물 카드 한 장을 탐색하고 그 카드를 전장에 놓는다. 그 생물은 자신의 다른 유형에 더불어 피렉시아다. 집중마법 시기에만 활성화할 수 있다.', ''),
            ('729511', '피렉시아 수확자가 피해를 입을 때마다, 그만큼 대지가 아닌 카드를 탐색한다. 당신의 다음 종료단 시작에, 그 카드들을 버린다.', ''),
            ('729510', 'CARDNAME가 피해를 입을 때마다, 그만큼 대지가 아닌 카드를 탐색한다. 당신의 다음 종료단 시작에, 그 카드들을 버린다.', ''),
            ('729491', '역병날개 새끼용이 플레이어에게 전투피해를 입힐 때마다, 그 플레이어가 가진 독 카운터의 수와 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('729490', 'CARDNAME이 플레이어에게 전투피해를 입힐 때마다, 그 플레이어가 가진 독 카운터의 수와 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('864440', '타락 — 노른의 하인이 들어올 때, 이름이 들인 카드 한 장을 당신의 손으로 부른다. 독 카운터를 세 개 이상 가진 상대가 있다면, 당신은 대신 대지가 아닌 카드 한 장을 탐색할 수 있다.', '<i>타락</i><nobr> —</nobr> 노른의 하인이 들어올 때, 이름이 들인 카드 한 장을 당신의 손으로 부른다. 독 카운터를 세 개 이상 가진 상대가 있다면, 당신은 대신 대지가 아닌 카드 한 장을 탐색할 수 있다.'),
            ('864439', '타락 — CARDNAME이 들어올 때, 이름이 들인 카드 한 장을 당신의 손으로 부른다. 독 카운터를 세 개 이상 가진 상대가 있다면, 당신은 대신 대지가 아닌 카드 한 장을 탐색할 수 있다.', '<i>타락</i><nobr> —</nobr> CARDNAME이 들어올 때, 이름이 들인 카드 한 장을 당신의 손으로 부른다. 독 카운터를 세 개 이상 가진 상대가 있다면, 당신은 대신 대지가 아닌 카드 한 장을 탐색할 수 있다.'),
            ('701519', '우르자의 건설 드론이 공격하거나 죽을 때마다, 우르자의 대지 카드 한 장을 탐색한다.', ''),
            ('701518', 'CARDNAME이 공격하거나 죽을 때마다, 우르자의 대지 카드 한 장을 탐색한다.', ''),
            ('763501', '요티아 전령이 공격할 때마다, 지난 전투에서 선택되지 않은 한 개를 선택한다 — • 탭된 마법석 토큰 한 개를 만든다. • 당신이 조종하는 마법석의 수와 동일한 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.', '요티아 전령이 공격할 때마다, 지난 전투에서 선택되지 않은 한 개를 선택한다<nobr> —</nobr> • 탭된 마법석 토큰 한 개를 만든다. • 당신이 조종하는 마법석의 수와 동일한 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.'),
            ('763500', 'CARDNAME이 공격할 때마다, 지난 전투에서 선택되지 않은 한 개를 선택한다 — • 탭된 마법석 토큰 한 개를 만든다. • 당신이 조종하는 마법석의 수와 동일한 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.', 'CARDNAME이 공격할 때마다, 지난 전투에서 선택되지 않은 한 개를 선택한다<nobr> —</nobr> • 탭된 마법석 토큰 한 개를 만든다. • 당신이 조종하는 마법석의 수와 동일한 마나 값을 가진 대지가 아닌 카드 한 장을 탐색한다.'),
            ('701490', '마나 값이 2 이하인 카드 한 장 및 마나 값이 3 이상인 카드 한 장을 탐색한다. 당신의 다음 턴 종료단 시작에, 그 카드들을 버린다.', ''),
            ('701479', '당신의 종료단 시작에, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 보물 토큰 한 개를 만들고 야망 또는 편법을 선택한다. 야망을 선택한다면, 버려진 카드보다 높은 마나 값을 가진 카드 한 장을 탐색한다. 편법을 선택한다면, 버려진 카드보다 낮은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('701418', '{o1oW}, 역사적 지속물 한 개를 희생한다: 역사적 카드 한 장을 탐색한다.', ''),
            ('676035', '영토 — {o7oG}: 생물 카드 한 장을 탐색한다. 이 능력은 당신이 조종하는 대지들이 가진 각 기본 대지 유형마다 활성화하는 데{o1} 이(가) 덜 든다.', '<i>영토</i><nobr> —</nobr> {o7oG}: 생물 카드 한 장을 탐색한다. 이 능력은 당신이 조종하는 대지들이 가진 각 기본 대지 유형마다 활성화하는 데{o1} 이(가) 덜 든다.'),
            ('676015', '당신의 전투전 본단계 시작에, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 그보다 더 큰 마나 값을 가진 카드 한 장을 탐색하고 그 카드를 추방한다. 당신의 다음 턴 턴종료까지, 당신은 추방된 카드를 플레이할 수 있다.', ''),
            ('860375', '다리가즈의 새끼용이 들어올 때, 키커 비용이 지불되었다면, 용 카드 한 장을 탐색한다. 다리가즈의 새끼용 및 그 용 카드는 각각 영구적으로 +1/+1을 받는다.', '다리가즈의 새끼용이 들어올 때, 키커 비용이 지불되었다면, 용 카드 한 장을 탐색한다. 다리가즈의 새끼용 및 그 용 카드는 각각 영구적으로 <nobr>+1/+1</nobr>을 받는다.'),
            ('860374', 'CARDNAME이 들어올 때, 키커 비용이 지불되었다면, 용 카드 한 장을 탐색한다. CARDNAME 및 그 용 카드는 각각 영구적으로 +1/+1을 받는다.', 'CARDNAME이 들어올 때, 키커 비용이 지불되었다면, 용 카드 한 장을 탐색한다. CARDNAME 및 그 용 카드는 각각 영구적으로 <nobr>+1/+1</nobr>을 받는다.'),
            ('860369', '보물창고 마도사가 들어올 때, 당신의 서고 맨 위 카드 열 장에서 마법물체 카드 한 장을 탐색한 뒤, 서고를 섞는다.', ''),
            ('860368', 'CARDNAME가 들어올 때, 당신의 서고 맨 위 카드 열 장에서 마법물체 카드 한 장을 탐색한 뒤, 서고를 섞는다.', ''),
            ('604265', '{o3oB}, {oT}: 대지가 아닌 카드 한 장을 탐색한다. 한 번만 활성화할 수 있다.', ''),
            ('604270', '{o3oG}, {oT}: 대지가 아닌 카드 한 장을 탐색한다. 한 번만 활성화할 수 있다.', ''),
            ('604275', '{o3oU}, {oT}: 대지가 아닌 카드 한 장을 탐색한다. 한 번만 활성화할 수 있다.', ''),
            ('604280', '{o3oW}, {oT}: 대지가 아닌 카드 한 장을 탐색한다. 한 번만 활성화할 수 있다.', ''),
            ('604285', '{o3oR}, {oT}: 대지가 아닌 카드 한 장을 탐색한다. 한 번만 활성화할 수 있다.', ''),
            ('604228', '이 턴에 마나 값이 3 이하인 주문을 발동한 상대가 있다면 생물 카드 한 장을 탐색한다.', ''),
            ('604230', '생물, 부여마법 및/또는 플레인즈워커 카드 X장을 탐색한다. X는 당신이 조종하는 생물들이 가진 마나 값 중 가장 높은 마나 값이다. 그 카드들을 전장에 놓는다.', ''),
            ('604193', '불길의 수호자, 카르둠이 공격할 때마다, 카르둠에 불길 카운터 한 개를 올려놓은 후, 카르둠에 놓인 불길 카운터의 수와 마나 값이 같은 카드 한 장을 탐색하고 그 카드를 뒷면 상태로 추방한다.', ''),
            ('604192', 'CARDNAME이 공격할 때마다, 카르둠에 불길 카운터 한 개를 올려놓은 후, 카르둠에 놓인 불길 카운터의 수와 마나 값이 같은 카드 한 장을 탐색하고 그 카드를 뒷면 상태로 추방한다.', ''),
            ('604187', '고블린 함정탐색꾼이 죽을 때, 마나 비용이 3 이하인 생물 카드 한 장을 탐색한다. 그 카드는 영구적으로 신속, "이 주문은 발동하는 데 {o1}가 덜 든다." 및 "당신의 종료단 시작에, 이 생물을 희생한다."를 얻는다.', ''),
            ('604186', 'CARDNAME이 죽을 때, 마나 비용이 3 이하인 생물 카드 한 장을 탐색한다. 그 카드는 영구적으로 신속, "이 주문은 발동하는 데 {o1}가 덜 든다." 및 "당신의 종료단 시작에, 이 생물을 희생한다."를 얻는다.', ''),
            ('610786', '혼돈 발로르가 공격하거나 죽을 때마다, 두 개를 선택한다. 각 모드는 반드시 서로 다른 플레이어를 목표로 정해야 한다. • 플레이어를 목표로 정한다. 그 플레이어는 자신의 손에 있는 모든 카드를 버린 후, 그만큼 대지가 아닌 카드를 탐색한다. • 플레이어를 목표로 정한다. 혼돈 발로르는 그 플레이어에게 피해 2점을 입히고 그 플레이어는 보물 토큰 두 개를 만든다. • 플레이어를 목표로 정한다. 혼돈 발로르는 그 플레이어가 조종하는 각 생물에게 피해 2점씩을 입힌다. 그 생물들은 영구적으로 +2/+0을 받는다.', '혼돈 발로르가 공격하거나 죽을 때마다, 두 개를 선택한다. 각 모드는 반드시 서로 다른 플레이어를 목표로 정해야 한다. • 플레이어를 목표로 정한다. 그 플레이어는 자신의 손에 있는 모든 카드를 버린 후, 그만큼 대지가 아닌 카드를 탐색한다. • 플레이어를 목표로 정한다. 혼돈 발로르는 그 플레이어에게 피해 2점을 입히고 그 플레이어는 보물 토큰 두 개를 만든다. • 플레이어를 목표로 정한다. 혼돈 발로르는 그 플레이어가 조종하는 각 생물에게 피해 2점씩을 입힌다. 그 생물들은 영구적으로 <nobr>+2/+0</nobr>을 받는다.'),
            ('610785', 'CARDNAME가 공격하거나 죽을 때마다, 두 개를 선택한다. 각 모드는 반드시 서로 다른 플레이어를 목표로 정해야 한다. • 플레이어를 목표로 정한다. 그 플레이어는 자신의 손에 있는 모든 카드를 버린 후, 그만큼 대지가 아닌 카드를 탐색한다. • 플레이어를 목표로 정한다. CARDNAME는 그 플레이어에게 피해 2점을 입히고 그 플레이어는 보물 토큰 두 개를 만든다. • 플레이어를 목표로 정한다. CARDNAME는 그 플레이어가 조종하는 각 생물에게 피해 2점씩을 입힌다. 그 생물들은 영구적으로 +2/+0을 받는다.', 'CARDNAME가 공격하거나 죽을 때마다, 두 개를 선택한다. 각 모드는 반드시 서로 다른 플레이어를 목표로 정해야 한다. • 플레이어를 목표로 정한다. 그 플레이어는 자신의 손에 있는 모든 카드를 버린 후, 그만큼 대지가 아닌 카드를 탐색한다. • 플레이어를 목표로 정한다. CARDNAME는 그 플레이어에게 피해 2점을 입히고 그 플레이어는 보물 토큰 두 개를 만든다. • 플레이어를 목표로 정한다. CARDNAME는 그 플레이어가 조종하는 각 생물에게 피해 2점씩을 입힌다. 그 생물들은 영구적으로 <nobr>+2/+0</nobr>을 받는다.'),
            ('604158', '플레이어를 목표로 정한다. 그 플레이어는 자신의 손에 있는 모든 카드를 버린 후, 그만큼 대지가 아닌 카드를 탐색한다.', ''),
            ('856936', '대표 주문이 들어올 때, 마나 값이 3인 순간마법 및/또는 집중마법 카드 두 장을 탐색한 후 그 카드들을 추방한다.', ''),
            ('856935', 'CARDNAME이 들어올 때, 마나 값이 3인 순간마법 및/또는 집중마법 카드 두 장을 탐색한 후 그 카드들을 추방한다.', ''),
            ('604111', '대지가 아닌 카드 두 장을 탐색한 후, 당신의 손에 있는 카드 한 장을 당신의 서고 맨 밑에 놓는다.', ''),
            ('604093', '하나 이상을 선택한다 — • 2/2 백색 기사 생물 토큰 두 개를 만든다. • 마나 값이 3 이하이며 대지가 아닌 지속물 카드 한 장을 탐색한다. • 마법물체를 목표로 정한다. 그 마법물체를 파괴한다. • 부여마법을 목표로 정한다. 그 부여마법을 파괴한다. • 플레이어를 목표로 정한다. 그 플레이어는 생명 3점을 얻는다.', '하나 이상을 선택한다<nobr> —</nobr> • 2/2 백색 기사 생물 토큰 두 개를 만든다. • 마나 값이 3 이하이며 대지가 아닌 지속물 카드 한 장을 탐색한다. • 마법물체를 목표로 정한다. 그 마법물체를 파괴한다. • 부여마법을 목표로 정한다. 그 부여마법을 파괴한다. • 플레이어를 목표로 정한다. 그 플레이어는 생명 3점을 얻는다.'),
            ('604092', '마나 값이 3 이하이며 대지가 아닌 지속물 카드 한 장을 탐색한다.', ''),
            ('604720', '이 생물이 전문화할 때, 대지가 아닌 지속물 카드 세 장을 탐색한다. 그 카드들 중 하나를 선택하고 나머지를 당신의 서고에 섞어넣는다.', ''),
            ('604851', '이 생물이 전문화할 때, 생물 카드 한 장을 탐색해 그 카드를 당신의 무덤에 넣은 후, 그 카드의 복제본 두 장을 당신의 무덤으로 부른다.', ''),
            ('610816', '이 생물이 전문화할 때, 이 생물에서 학습 카운터를 모두 제거한다. 마나 값이 이런 식으로 제거된 학습 카운터의 수 이하인 생물 카드 두 장을 탐색한다. 그중 한 장을 전장에 놓고 다른 한 장은 당신의 서고에 섞어넣는다.', ''),
            ('619014', '이 카드가 어떤 영역에서든 전문화할 때, 마나 값이 3 이하인 순간마법 또는 집중마법 카드 한 장을 탐색한다. 턴종료까지, 당신은 마나 비용을 지불하지 않고 그 카드를 발동할 수 있다.', ''),
            ('874738', '이 생물이 들어오거나 전문화할 때, 마나 값이 3 이하이며 대지가 아닌 지속물 카드 한 장을 탐색한다.', ''),
            ('857452', '달 드루이드, 루카미나가 들어올 때, 당신이 루카미나를 발동했다면, 기본 대지 유형을 가진 대지 카드 한 장을 탐색한다.', ''),
            ('857451', 'CARDNAME가 들어올 때, 당신이 루카미나를 발동했다면, 기본 대지 유형을 가진 대지 카드 한 장을 탐색한다.', ''),
            ('856857', '옵스큐라 변환술사가 들어올 때, 생물을 최대 한 개까지 목표로 정한다. 그 생물을 추방한다. 그 생물의 조종자는 생물 카드 한 장을 탐색한다.', ''),
            ('856856', 'CARDNAME가 들어올 때, 생물을 최대 한 개까지 목표로 정한다. 그 생물을 추방한다. 그 생물의 조종자는 생물 카드 한 장을 탐색한다.', ''),
            ('614542', '당신이 카드를 한 장 이상 버릴 때마다, 버려진 카드들 중 하나와 카드 유형을 공유하는 카드 한 장을 탐색한다. 이 능력은 한 턴에 한 번만 격발한다.', ''),
            ('614492', '당신이 생물 주문을 발동할 때마다, 더 적은 마나 값을 가진 생물 카드를 탐색한 후, 그 카드를 전장에 놓는다.', ''),
            ('875746', '연대 — 당신이 조종하는 다른 생물이 한 개 이상 들어올 때마다, 대지 카드 한 장을 탐색한 후, 그 카드를 탭된 채로 전장에 놓는다. 이 능력은 한 턴에 한 번만 격발한다.', '<i>연대</i><nobr> —</nobr> 당신이 조종하는 다른 생물이 한 개 이상 들어올 때마다, 대지 카드 한 장을 탐색한 후, 그 카드를 탭된 채로 전장에 놓는다. 이 능력은 한 턴에 한 번만 격발한다.'),
            ('614444', '카드 두 장을 탐색한다. 당신은 그 카드들을 당신의 서고에 섞어넣을 수 있다. 그렇게 한다면, 카드 두 장을 탐색한다.', ''),
            ('598825', '주카이 해방자가 플레이어에게 전투피해를 입힐 때마다, 대지 또는 비대지를 선택한다. 선택된 유형을 가진 지속물 카드 한 장을 탐색한다.', ''),
            ('598824', 'CARDNAME가 플레이어에게 전투피해를 입힐 때마다, 대지 또는 비대지를 선택한다. 선택된 유형을 가진 지속물 카드 한 장을 탐색한다.', ''),
            ('855653', '대포 맹신자가 들어올 때, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 그 카드의 마나 값과 마나 값이 동일한 카드 한 장을 탐색한다.', ''),
            ('855652', 'CARDNAME가 들어올 때, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 그 카드의 마나 값과 마나 값이 동일한 카드 한 장을 탐색한다.', ''),
            ('566794', '장착된 생물이 플레이어에게 전투피해를 입힐 때마다, 그 피해와 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('603573', '매 전투 시작에, 자바의 공포, 기트로그가 언탭되어 있다면, 어느 상대든 토큰이 아닌 생물 한 개를 희생할 수 있다. 그 플레이어가 그렇게 한다면, 자바의 공포, 기트로그를 탭한 후, 대지 카드 한 장을 탐색해 탭된 채로 전장에 놓는다.', ''),
            ('603572', '매 전투 시작에, CARDNAME가 언탭되어 있다면, 어느 상대든 토큰이 아닌 생물 한 개를 희생할 수 있다. 그 플레이어가 그렇게 한다면, CARDNAME를 탭한 후, 대지 카드 한 장을 탐색해 탭된 채로 전장에 놓는다.', ''),
            ('566469', '기본 대지 카드 한 장을 탐색해 탭된 채로 전장에 놓는다. 그 후 당신이 조종하는 대지의 수와 동일한 마나 값을 가진 지속물 카드 한 장을 탐색한다.', ''),
            ('853148', '돌기둥공터 조련사가 들어올 때, 대지 카드 한 장을 탐색한다.', ''),
            ('853147', 'CARDNAME가 들어올 때, 대지 카드 한 장을 탐색한다.', ''),
            ('566446', '심령무리 우두머리가 죽을 때, 당신이 조종하는 대지의 수와 동일한 마나 값을 가진 지속물 카드 한 장을 탐색한다.', ''),
            ('566445', 'CARDNAME가 죽을 때, 당신이 조종하는 대지의 수와 동일한 마나 값을 가진 지속물 카드 한 장을 탐색한다.', ''),
            ('853107', '광란한 심령폭파자가 들어올 때, 당신의 무덤, 손, 및 서고에 순간마법 및/또는 집중마법 카드가 20장 이상 있다면, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 순간마법 또는 집중마법 카드 한 장을 탐색한다.', ''),
            ('853106', 'CARDNAME가 들어올 때, 당신의 무덤, 손, 및 서고에 순간마법 및/또는 집중마법 카드가 20장 이상 있다면, 당신은 카드 한 장을 버릴 수 있다. 그렇게 한다면, 순간마법 또는 집중마법 카드 한 장을 탐색한다.', ''),
            ('566778', '당신의 종료단 시작에, 당신의 무덤에 있는 생물 카드를 최대 한 장까지 목표로 정한다. 그 카드를 추방한다. 그렇게 한다면, 그 카드의 마나 값에 1을 더한 수와 같은 마나 값을 가지는 생물 카드 한 장을 탐색한다. 그 카드는 영구적으로 호전적을 얻는다.', ''),
            ('566349', '강박적인 수집가가 플레이어에게 전투피해를 입힐 때마다, 당신의 손에 있는 카드의 수와 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('566348', 'CARDNAME가 플레이어에게 전투피해를 입힐 때마다, 당신의 손에 있는 카드의 수와 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('566346', '주문을 목표로 정한다. 그 주문을 무효화한다. 그 주문과 같은 마나 값을 가진 카드 한 장을 탐색한다.', ''),
            ('566336', '대지가 아닌 카드 세 장을 탐색한 후, 당신의 손에 있는 대지가 아닌 카드들은 영구적으로 "이 주문은 발동하는 데 {o1}이 덜 든다."를 가진다.', ''),
            ('566766', '카드 두 장을 뽑는다. 그 후 당신은 당신의 손에서 순간마법 또는 집중마법 카드 한 장을 추방할 수 있다. 그렇게 한다면, 당신의 손 및 서고에서 같은 이름을 가진 카드를 원하는 수만큼 찾아, 그 카드들을 추방하고, 서고를 섞는다. 당신의 손에서 이런 식으로 추방된 각 카드마다 순간마법 또는 집중마법 카드 한 장을 탐색한다.', ''),
            ('852999', '심문관 대장이 들어올 때, 당신이 심문관 대장을 발동했고 당신의 무덤, 손, 그리고 서고에 마나 값이 3 이하인 생물 카드가 20장 이상 있다면, 마나 값이 3 이하인 생물 카드 두 장을 탐색한다. 그중 한 장을 전장에 놓고 다른 한 장은 당신의 서고에 섞어넣는다.', ''),
            ('852998', 'CARDNAME이 들어올 때, 당신이 CARDNAME을 발동했고 당신의 무덤, 손, 그리고 서고에 마나 값이 3 이하인 생물 카드가 20장 이상 있다면, 마나 값이 3 이하인 생물 카드 두 장을 탐색한다. 그중 한 장을 전장에 놓고 다른 한 장은 당신의 서고에 섞어넣는다.', ''),
            ('851834', '스카이슈라우드 파수꾼이 들어올 때, 엘프 카드 한 장을 탐색한다.', ''),
            ('851833', 'CARDNAME이 들어올 때, 엘프 카드 한 장을 탐색한다.', ''),
            ('548260', '엘프 카드 한 개를 탐색한다.', ''),
            ('548281', '엘프 카드를 탐색하십시오.', ''),
            ('547412', '저택 수호자가 죽을 때, 각 플레이어는 마나 값이 2 이하인 대지가 아닌 카드 한 장을 탐색한다.', ''),
            ('547411', 'CARDNAME가 죽을 때, 각 플레이어는 마나 값이 2 이하인 대지가 아닌 카드 한 장을 탐색한다.', ''),
            ('548199', '당신의 손애 대지 카드가 없다면, 대지 카드 한 장 및 대지가 아닌 카드 한 장을 탐색한다. 그렇지 않다면, 대지가 아닌 카드 두 장을 탐색한다.', ''),
            ('851728', '얼굴 없는 요원이 들어올 때, 당신의 서고에 가장 많이 포함된 생물 유형을 가진 생물 카드 한 장을 탐색한다.', ''),
            ('851727', 'CARDNAME이 들어올 때, 당신의 서고에 가장 많이 포함된 생물 유형을 가진 생물 카드 한 장을 탐색한다.', ''),
            ('566499', '당신의 손에 있는 카드의 수와 동일한 마나 값을 가진 카드 한 장을 탐색하십시오.', ''),
            ('566506', '당신이 조종하는 대지의 수와 동일한 마나 값을 가진 지속물 카드 한 장을 탐색하십시오.', ''),
            ('566507', '대지 카드 한 장을 탐색하십시오.', ''),
            ('566511', '대지가 아닌 카드 세 장을 탐색하십시오.', ''),
            ('566513', '그 피해량과 마나 값이 동일한 카드 한 장을 탐색하십시오.', ''),
            ('566514', '기본 대지 카드를 탐색하십시오.', ''),
            ('566802', '그 카드의 마나 값에 1을 더한 수와 같은 마나 값을 가지는 생물 카드 한 장을 탐색하십시오.', ''),
            ('566805', '마나 값이 3 이하인 생물 카드 두 장을 탐색하십시오.', ''),
            ('567008', '순간마법 또는 집중마법 카드 한 장을 탐색하십시오.', ''),
            ('567969', '{2, plural, =1 {순간마법 또는 집중마법 카드 {2, Number}장} other {순간마법 또는 집중마법 카드 {2, Number}장}}을 탐색하십시오.', ''),
            ('568053', '그 주문과 같은 마나 값을 가진 카드 한 장을 탐색하십시오.', ''),
            ('595505', '그 카드의 마나 값과 마나 값이 동일한 카드 한 장을 탐색하십시오.', ''),
            ('620556', '자신의 손을 버리게 할 플레이어를 목표로 정하십시오. 그 플레이어는 그 후 대지가 아닌 카드들을 그만큼 탐색합니다.', ''),
            ('729590', '대지가 아닌 카드를 탐색하시겠습니까?', ''),
            ('793461', '추방된 카드보다 적은 마나 값을 가진 대지가 아닌 카드 한 장을 탐색하십시오.', ''),
            ('810806', '마나 값이 3 이하이며 코끼리가 아닌 생물 카드 한 장을 탐색하십시오.', ''),
            # v1.1.1
            ('236486', '{o5}, {oT}, 문양을 그리는 추를 희생한다: 카드 한 장을 뽑는다.', ''),
            ('851426', '그을린 습지는 당신이 기본 대지를 두 개 이상 조종하지 않는 한 탭된 채로 들어온다.', ''),
            ('851429', '침몰된 골짜기는 당신이 기본 대지를 두 개 이상 조종하지 않는 한 탭된 채로 들어온다.', ''),
            # v1.1.2
            ('752156', '당신이 각 턴에 처음으로 생명점을 잃을 때마다, 복수심에 불타는 전쟁족장에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', ''),
            ('351913', '당신이 각 턴에 처음으로 생명점을 잃을 때마다, CARDNAME에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', '당신이 각 턴에 처음으로 생명점을 잃을 때마다, CARDNAME에 <nobr>+1/+1</nobr> 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>'),
            ('751916', '당신이 생명점을 잃을 때마다, 그만큼 카드를 뽑는다. <i>(피해는 생명점을 잃게 한다.)</i>', ''),
            ('751897', '당신의 종료단 시작에, 플레이어가 이번 턴에 생명점을 4점 이상 잃었다면, 검은 군단의 기사에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', ''),
            ('351877', '당신의 종료단 시작에, 플레이어가 이번 턴에 생명점을 4점 이상 잃었다면, CARDNAME에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', '당신의 종료단 시작에, 플레이어가 이번 턴에 생명점을 4점 이상 잃었다면, CARDNAME에 <nobr>+1/+1</nobr> 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>'),
            ('751743', '당신의 종료단 시작에, 상대가 이번 턴에 생명점을 잃었다면, 난폭한 포식자에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', ''),
            ('352289', '당신의 종료단 시작에, 상대가 이번 턴에 생명점을 잃었다면, CARDNAME에 +1/+1 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>', '당신의 종료단 시작에, 상대가 이번 턴에 생명점을 잃었다면, CARDNAME에 <nobr>+1/+1</nobr> 카운터 한 개를 올려놓는다. <i>(피해는 생명점을 잃게 한다.)</i>'),
            ('752312', '주문, 활성화능력 또는 격발능력을 목표로 정한다. 그 목표를 무효화한다. <i>(마나 능력은 목표로 정해질 수 없다.)</i>', ''),
            ('751823', '활성화능력 또는 격발능력을 목표로 정한다. 그 목표를 무효화한다. <i>(마나 능력은 목표로 정해질 수 없다.)</i>', ''),
            ('753170', '{oG}, {oT}: 당신이 조종하며 부여마법이 원천인 활성화능력 또는 격발능력을 목표로 정한다. 그 목표를 복사한다. 당신은 그 복사본의 목표를 새로 정할 수 있다. <i>(마나 능력은 목표로 정해질 수 없다.)</i>', ''),
            ('413722', '{oT}: 당신의 무덤에 있는 마법물체 카드를 목표로 정한다. 당신은 이 턴에 그 카드를 발동할 수 있다. <i>(여전히 발동 비용은 지불해야 한다. 발동 시기 규칙도 여전히 적용된다.)</i>', ''),
            # v1.1.3
            ('558066', '뱀 드루이드', ''),
            # v.1.1.4
            ('281000', '봉기',''),
            # v.1.2.0
            ('877473', '문턱 — {oT}: 이 턴에 당신이 당신의 무덤에서 발동하는 주문들은 발동하는 데 {o2}이(가) 덜 든다. 당신의 무덤에 카드가 일곱 장 이상 있는 경우에만 활성화할 수 있다.','<i>문턱</i><nobr> —</nobr> {oT}: 이 턴에 당신이 당신의 무덤에서 발동하는 주문들은 발동하는 데 {o2}이(가) 덜 든다. 당신의 무덤에 카드가 일곱 장 이상 있는 경우에만 활성화할 수 있다.'),
            ('878570', '상대를 목표로 정한다. 그 플레이어는 자신의 손에서 대지가 아닌 각 카드를 공개한다. 당신은 그 카드 중 한 장을 선택한다. 그 카드를 추방한다. \n문턱 — 당신의 무덤에 카드가 일곱 장 이상 있다면, 쥐 카드 한 장을 탐색한다. 그 카드는 영구적으로 "이 주문은 발동하는 데 {o1}이(가) 덜 든다."를 얻는다.','상대를 목표로 정한다. 그 플레이어는 자신의 손에서 대지가 아닌 각 카드를 공개한다. 당신은 그 카드 중 한 장을 선택한다. 그 카드를 추방한다. \n<i>문턱</i><nobr> —</nobr> 당신의 무덤에 카드가 일곱 장 이상 있다면, 쥐 카드 한 장을 탐색한다. 그 카드는 영구적으로 "이 주문은 발동하는 데 {o1}이(가) 덜 든다."를 얻는다.'),
            ('877476', '카드 두 장을 뽑는다. 선물이 약속되었다면, 대신 대지가 아닌 카드 두 장을 탐색한다.',''),
            ('877495', 'CARDNAME가 전장을 떠날 때, 추방된 카드의 소유자는 추방된 카드와 카드 유형을 공유하는 카드 한 장을 탐색한다.',''),
            ('877496', '검은별 추방자가 전장을 떠날 때, 추방된 카드의 소유자는 추방된 카드와 카드 유형을 공유하는 카드 한 장을 탐색한다.',''),
            ('877537', '당신의 종료단 시작에, 당신이 탭된 생물을 조종한다면, 마나 비용이 X 이하이고 대지가 아닌 지속물 카드 한 장을 탐색한다. X는 당신이 조종하는 탭된 생물의 수다. 그 카드를 전장에 놓는다.',''),
            ('878558', '당신이 지속물을 한 개 이상 희생할 때마다, 대지가 아닌 카드 한 장을 탐색한다.',''),
            ('878559', '당신은 "당신이 지속물을 한 개 이상 희생할 때마다, 대지가 아닌 카드 한 장을 탐색한다."를 가진 2회성 축복을 받는다.',''),
            ('878565', '기본이 아닌 대지 카드 한 장을 탐색한다. 키커 비용이 지불되었다면, 그 카드를 탭된 채로 전장에 놓는다.',''),
        ]

        card_select_query = f"SELECT {card_search_column}, {card_target_column}, {card_name_en}, {card_name_kr} FROM {card_table_name} WHERE {card_search_column} = ?"
        card_update_query = f"UPDATE {card_table_name} SET {card_target_column} = ? WHERE {card_search_column} = ?"
        card_update_query_formatted = f"UPDATE {card_table_name} SET {card_target_column} = ? WHERE {card_search_column} = ? AND {card_formatted_column} = 1"


        for search_value, new_value_not_formatted, new_value_formatted in card_values_to_update:
            # 특정 값을 포함하는 행 찾기
            card_cursor.execute(card_select_query, (search_value,))
            rows = card_cursor.fetchall()

            if rows:
                # 기본 업데이트 쿼리 실행
                card_cursor.execute(card_update_query, (new_value_not_formatted, search_value))
                print(f"{rows[0][3]}({rows[0][2]})가 {new_value_not_formatted}로 변경되었습니다.\n")
                
                # formatted 열이 1인 경우의 값이 제공된 경우
                if new_value_formatted != '':
                    card_cursor.execute(card_update_query_formatted, (new_value_formatted, search_value))
                    print(f"{rows[0][3]}({rows[0][2]})가 {new_value_formatted}로 변경되었습니다.\n")
            else:
                print(f"{search_value}에 해당하는 값을 찾지 못하였습니다.")

        card_conn.commit()

    except sqlite3.Error as e:
        print(f"{card_file}에서 에러 발생: {e}")

    finally: 
        if card_conn:
            card_conn.close()
        

