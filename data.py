from dataclasses import dataclass

# 땅 데이터
@dataclass(frozen=True)
class Land_Info():
    name:str
    land:int
    house1:int
    house2:int
    house3:int
    building:int
    hotel:int
    landmark:int

if True:
    Pyongyang = Land_Info("평양 (북한)", 50000, 15000, 20000, 30000, 50000, 70000, 90000)
    Mogadishu = Land_Info("모가디슈 (소말리아)", 80000, 20000, 25000, 40000, 60000, 80000, 100000)
    Kabul = Land_Info("카불 (아프가니스탄)", 80000, 20000, 25000, 40000, 60000, 80000, 100000)
    Damascus = Land_Info("다마스커스 (시리아)", 100000, 25000, 30000, 45000, 75000, 100000, 125000)
    Harare = Land_Info("하라레 (짐바브웨)", 120000, 30000, 35000, 50000, 80000, 110000, 140000)
    Caracas = Land_Info("카라카스 (베네수엘라)", 130000, 35000, 40000, 55000, 90000, 120000, 150000)
    red_info = (Pyongyang, Mogadishu, Kabul, Damascus, Harare, Caracas)

    Nairobi = Land_Info("나이로비 (케냐)", 200000, 50000, 60000, 85000, 150000, 200000, 250000)
    Budapest = Land_Info("부다페스트 (헝가리)", 220000, 60000, 70000, 95000, 160000, 220000, 275000)
    Kyiv = Land_Info("키이우 (우크라이나)", 240000, 65000, 75000, 90000, 170000, 240000, 300000)
    Athens = Land_Info("아테네 (그리스)", 260000, 70000, 80000, 100000, 180000, 260000, 320000)
    Islamabad = Land_Info("이슬라마바드 (파키스탄)", 280000, 80000, 90000, 110000, 190000, 280000, 350000)
    Riyadh = Land_Info("리야드 (사우디아라비아)", 800000, 90000, 100000, 120000, 200000, 300000, 500000)
    green_info = (Nairobi, Budapest, Kyiv, Athens, Islamabad, Riyadh)

    Sydney = Land_Info("시드니 (호주)", 350000, 70000, 850000, 100000, 200000, 300000, 400000)
    Seoul = Land_Info("서울 (한국)", 380000, 75000, 90000, 110000, 220000, 330000, 440000)
    Roma = Land_Info("로마 (이탈리아)", 380000, 75000, 90000, 110000, 220000, 330000, 440000)
    NewDelhi = Land_Info("뉴델리 (인도)", 400000, 80000, 950000, 125000, 240000, 350000, 460000)
    Moscow = Land_Info("모스크바 (러시아)", 400000, 80000, 950000, 125000, 240000, 350000, 460000)
    Beijing = Land_Info("베이징 (중국)", 430000, 85000, 100000, 130000, 250000, 360000, 470000)
    blue_info = (Sydney, Seoul, Roma, NewDelhi, Moscow, Beijing)

    Ottawa = Land_Info("오타와 (케나다)", 500000, 100000, 115000, 140000, 290000, 400000, 500000)
    Paris = Land_Info("파리 (프랑스)", 550000, 110000, 130000, 160000, 320000, 440000, 550000)
    London = Land_Info("런던 (영국)", 600000, 120000, 140000, 175000, 350000, 480000, 600000)
    Berlin = Land_Info("베를린 (독일)", 650000, 130000, 150000, 190000, 380000, 520000, 650000)
    Tokyo = Land_Info("도쿄 (일본)", 700000, 140000, 170000, 220000, 410000, 550000, 700000)
    NewYork = Land_Info("뉴욕 (미국)", 1000000, 200000, 250000, 350000, 500000, 750000, 1000000)
    black_info = (Ottawa, Paris, London, Berlin, Tokyo, NewYork)

lands_info = (red_info, green_info, blue_info, black_info)

# 황금망치 데이터
@dataclass(kw_only=True)
class Golden_Hammer():
    title:str
    content:str
    effect:str

golden_txt = {
    1:Golden_Hammer(
        title="동네 양아치", 
        content="당신은 골목에서 양아치를 만났습니다.\n\"야, 너 돈 좀 있냐?\"", 
        effect="5000원 지불"
    ), 
    2:Golden_Hammer(
        title="알바 대타", 
        content="당신의 친구가 사정이 생겨 알바를 대신 해달라고 합니다.\n당신은 친구를 위해 하루 동안 알바를 뛰고 시급을 받았습니다.", 
        effect="한 턴 쉬고 1만원 지급"
    ), 
    3:Golden_Hammer(
        title="신나는 생일 파티", 
        content="생일 축하드립니다.\n친구들에게 선물로 5천원을 받습니다.", 
        effect="모두에게서 5천원 받기"
    ), 
    4:Golden_Hammer(
        title="지진 발생", 
        content="거짓말처럼 당신이 소유하고 있는 땅에만 지진이 발생했습니다.\n무너진 건물들을 수리해야 합니다.", 
        effect="자신의 모든 건물 가격의 10% 지불"
    ), 
    5:Golden_Hammer(
        title="복권 당첨", 
        content="당신은 5천원을 주고 복권을 구매했습니다.", 
        effect="5천원 지불 및 "
    ), 
    6:Golden_Hammer(
        title="건설회사 친구", 
        content="당신의 친구가 건물을 지어준다고 합니다.\n다음 건물을 지을 때 10% 할인받습니다.", 
        effect="1회 건물 건설 비용 10% 할인"
    ), 
    7:Golden_Hammer(
        title="헬기 이용권", 
        content="당신은 헬기 무료 이용권을 주웠습니다.\n이런 게 왜 길에 떨어져 있는 거죠?", 
        effect="1회 무인도 즉시 탈출 가능"
    ), 
    8:Golden_Hammer(
        title="검사 친구", 
        content="당신은 유능한 검사를 친구로 두었습니다.\n친구는 한 번만 도와주겠다고 합니다.", 
        effect="다음 통행료 1회 면제 및 해당 토지의 주인 1턴 쉬기"
    ), 
    9:Golden_Hammer(
        title="강도 친구", 
        content="당신은 강도를 친구로 두었습니다.\n당신은 한 사람의 돈을 빼앗을 수 있습니다.", 
        effect="플레이어를 지목해 1만원 받기"
    ), 
    10:Golden_Hammer(
        title="코로나 확진", 
        content="당신은 코로나에 확진되어 자가격리를 해야 합니다.\n괜히 돌아다니다가 전염시키지 말아요.", 
        effect="2턴 쉬기"
    ), 
    11:Golden_Hammer(
        title="허모씨 당선", 
        content="허모 씨가 당선이 되었습니다.\n오히려 좋을지도?", 
        effect="전원 10만원 지급"
    ), 
    12:Golden_Hammer(
        title="독제정치", 
        content="독제정치로 통금이 생겼습니다.\n제 이웃은 이 밤에 왜 밖으로 나서는 걸까요?", 
        effect="다음 플레이어 1턴 쉬기"
    ), 
    13:Golden_Hammer(
        title="교통사고", 
        content="당신은 교통사고를 당했습니다.\n의사가 입원을 권합니다.", 
        effect="5만원 지불 및 1턴 쉬기"
    ), 
    14:Golden_Hammer(
        title="우주여행 티켓", 
        content="당신은 길에서 우주여행 티켓을 주웠습니다.\n길에는 없는 게 뭐죠?", 
        effect="우주여행 1회 무료"
    ), 
    15:Golden_Hammer(
        title="유명 유튜브 출연", 
        content="당신은 우연히 야외 방송을 진행하는 유명 유튜버를 만났습니다.\n시청자들이 당신을 좋아하는 것 같군요.", 
        effect="모두의 박수 받기"
    ), 
    16:Golden_Hammer(
        title="중고거래 사기", 
        content="물건을 받고 상자를 열어보니 벽돌이 있습니다.\n잠깐, 얼마에 거래했었죠?", 
        effect="5천원 ~ 1만원 중 랜덤한 금액 지불"
    ), 
    17:Golden_Hammer(
        title="가상화폐", 
        content="가상화폐의 가치가 상승하고 있다고 합니다.\n도전해볼 만 할 것 같습니다.", 
        effect="10만원 지급 및 3턴 뒤 20만원 지불"
    ), 
    18:Golden_Hammer(
        title="유적지 발견", 
        content="당신이 보유한 땅에서 유적지가 발견되었습니다.\n박물관이 세워지면 좋겠네요.", 
        effect="보유한 땅 중 랜덤한 1개의 통행료 50% 상승"
    ), 
    19:Golden_Hammer(
        title="누추한 곳에 귀한 분이", 
        content="빨간색 혹은 초록색의 땅 중 하나에\n디즈니랜드가 들어옵니다.\n이유가 뭐든 좋은 게 좋은 거죠.", 
        effect="해당 땅의 통행료 50% 상승"
    ), 
    20:Golden_Hammer(
        title="소개팅 성공", 
        content="당신은 소개팅을 성공적으로 마쳤고 주선자에게 감사의 술을 건넵니다.", 
        effect="2만원 지불"
    ), 
    21:Golden_Hammer(
        title="소개팅 실패", 
        content="당신은 소개팅 비용까지 지불했지만 결국 실패했습니다.\n친구와 술을 마시며 한탄합니다.", 
        effect="2만원 지불"
    ), 
    22:Golden_Hammer(
        title="대학 입학", 
        content="당신은 꿈에 그리던 대학에 입학했습니다.\n입학금이라니 이 돈이 좋은 곳에 쓰이길..", 
        effect="5만원 지불"
    ), 
    23:Golden_Hammer(
        title="외환 위기", 
        content="외환 위기가 닥처왔습니다.\n모두 3번만 힘들면 될 겁니다.", 
        effect="전원 3턴간 통행료 50% 감소"
    ), 
    24:Golden_Hammer(
        title="모범 시민", 
        content="당신은 모범시민상을 받았습니다.\n제가 다 뿌듯하네요.", 
        effect="모두의 박수 받기"
    ), 
    25:Golden_Hammer(
        title="화재 발생", 
        content="당신의 땅 하나에 큰 화재가 발생했습니다.\n보기 좋지는 않네요.", 
        effect="3턴간 해당 땅의 통행료 50% 감소"
    ), 
    26:Golden_Hammer(
        title="보험 사기", 
        content="당신은 보험 사기를 쳤습니다.\n감옥 정도야 금방이죠.", 
        effect="지목한 플레이어에게 10만원 받고 2턴 쉬기"
    ), 
    27:Golden_Hammer(
        title="플라스틱 망치", 
        content="진짜 망치인 줄 알고 휘둘렀지만 플라스틱 망치였네요.\n오히려 망치가 부서집니다.", 
        effect=""
    ), 
    28:Golden_Hammer(
        title="도박 중독", 
        content="당신은 최근 도박에 중독되었습니다.\n저절로 몸이 카지노로 향합니다.", 
        effect="카지노로 이동"
    ), 
    29:Golden_Hammer(
        title="문모씨 3주년", 
        content="3주년 기념행사라고 합니다.\n정말 행사 맞죠..?", 
        effect="3턴간 모든 땅의 매입 가격 및 통행료 50% 증가"
    ), 
    30:Golden_Hammer(
        title="불우이웃 돕기", 
        content="당신은 돈이 없는 사람을 보니 돕고 싶어집니다.\n얼마가 적당할까요?", 
        effect="돈이 가장 적은 플레이어에게 15만원 주기"
    ), 
    31:Golden_Hammer(
        title="신용불량", 
        content="당신의 신용등급이 매우 낮습니다.\n경제활동이 일부 제한됩니다.", 
        effect="2턴간 모든 구입 활동 불가"
    ), 
    32:Golden_Hammer(
        title="아 @발 꿈", 
        content="당신은 땅을 구매하는 꿈을 꾸었습니다.\n꿈은 꿈일 뿐 현실은 다르죠.", 
        effect="랜덤한 땅 1개 구매비용 돌려받기"
    ), 
    33:Golden_Hammer(
        title="공금 횡령", 
        content="당신은 횡령을 하기로 마음먹습니다.\n저런, 들키고 말았군요.", 
        effect="사회복지기금 획득 및 2턴 쉬기"
    ), 
    34:Golden_Hammer(
        title="즐거운 여행", 
        content="당신은 하와이로 여행을 떠납니다.\n그런데 이런, 비행기가 추락합니다.", 
        effect="무인도로 이동"
    ), 
    35:Golden_Hammer(
        title="씁.. 후..", 
        content="인생이 너무 무료한 당신, 결국 손에 대고 말았군요.\n하지만 그건 불법입니다.", 
        effect="재산의 10% 지불"
    ), 
}
