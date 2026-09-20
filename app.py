import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. 커스텀 CSS (다크 모드 및 스타일 반영)
# =========================================================
st.markdown("""
<style>
/* 글로벌 다크 배경 및 기본 폰트 설정 */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #121212 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #e0e0e0 !important;
}

/* 상단 패딩 확보 및 반응형 너비 설정 */
.main .block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
}

/* 사이드바 다크 스타일링 */
section[data-testid="stSidebar"] {
    background-color: #1e1e1e !important;
    border-right: 1px solid #2d2d2d !important;
}

/* 메인 타이틀 헤더 */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}
.header-title-box {
    display: flex;
    align-items: center;
    gap: 10px;
}
.header-icon {
    font-size: 28px;
    color: #ff6b6b;
}
.header-title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.3 !important;
    margin: 0;
}
.header-subtitle {
    font-size: 14px;
    color: #a0a0a0;
    margin-top: 4px;
}
.fav-btn {
    background-color: #2b2b2b;
    border: 1px solid #3d3d3d;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    color: #ff6b6b;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}

/* 대시보드 지표 카드 */
.metric-card {
    background: #1e1e1e;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #2d2d2d;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.metric-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.metric-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}
.metric-label {
    font-size: 12px;
    color: #a0a0a0;
    font-weight: 600;
}
.metric-value {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
}
.metric-sub {
    font-size: 11px;
    color: #707070;
    margin-top: 2px;
}

/* 지도 범례 */
.legend-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-top: 10px;
    margin-bottom: 25px;
    font-size: 12px;
    color: #b0b0b0;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}
.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

/* 상세 정보 섹션 */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 메인 지역 정보 카드 */
.main-region-card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #2d2d2d;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    height: 100%;
    position: relative;
}
.main-region-img {
    width: 100%;
    height: 160px;
    object-fit: cover;
}
.badge-score {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #ff6b6b;
    color: white;
    font-weight: 700;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 20px;
}
.main-region-body {
    padding: 16px;
}
.main-region-desc {
    font-size: 13px;
    color: #cccccc;
    line-height: 1.5;
    margin-bottom: 15px;
}
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    border-top: 1px solid #2d2d2d;
    padding-top: 12px;
    text-align: center;
}
.stat-item-label {
    font-size: 11px;
    color: #a0a0a0;
}
.stat-item-val {
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
}

/* 서브 아이템 카드 */
.sub-info-card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #2d2d2d;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    height: 100%;
}
.sub-info-title {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
}
.sub-info-img {
    width: 100%;
    height: 110px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
}
.sub-info-name {
    font-size: 15px;
    font-weight: 700;
    color: #ffffff;
}
.sub-info-desc {
    font-size: 12px;
    color: #a0a0a0;
    line-height: 1.4;
    margin-top: 4px;
    margin-bottom: 12px;
}
.btn-more {
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 6px 0;
    background: #2b2b2b;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    font-size: 12px;
    color: #e0e0e0;
    font-weight: 600;
    text-decoration: none;
}

/* 추천 맛집 카드 */
.place-card {
    background: #1e1e1e;
    border-radius: 10px;
    border: 1px solid #2d2d2d;
    padding: 12px;
    display: flex;
    gap: 12px;
    align-items: center;
}
.place-img {
    width: 80px;
    height: 80px;
    border-radius: 8px;
    object-fit: cover;
}
.place-name {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
}
.place-star {
    font-size: 12px;
    color: #fcc419;
    font-weight: 700;
    margin: 2px 0;
}
.place-addr {
    font-size: 11px;
    color: #a0a0a0;
}

/* 리뷰 카드 */
.review-card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #2d2d2d;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.review-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.review-user {
    display: flex;
    align-items: center;
    gap: 10px;
}
.review-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #2b2b2b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.review-username {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
}
.review-date {
    font-size: 11px;
    color: #707070;
}
.review-text {
    font-size: 12px;
    color: #cccccc;
    line-height: 1.5;
    margin-bottom: 12px;
}
.review-imgs {
    display: flex;
    gap: 6px;
}
.review-img {
    width: 48%;
    height: 70px;
    border-radius: 6px;
    object-fit: cover;
}

/* 길찾기 커스텀 버튼 스타일 */
.navi-btn-container {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}
.navi-btn-naver {
    flex: 1;
    background-color: #03C75A;
    color: white !important;
    text-align: center;
    padding: 8px 0;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
}
.navi-btn-kakao {
    flex: 1;
    background-color: #FEE500;
    color: #191919 !important;
    text-align: center;
    padding: 8px 0;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. 데이터 로드 (추천 지역 10곳)
# =========================================================
@st.cache_data
def load_data():
    return [
        {
            "id": 1, "지역": "강원도 정선군", "위도": 37.3806, "경도": 128.6608, "점수": 88.7,
            "인구": "34,419명", "면적": "1,444.00㎢", "음식점수": "46개", "관광지수": "91개",
            "소개": "아리랑의 고향 정선은 아름다운 자연경관과 전통문화, 그리고 건강한 먹거리가 가득한 보석 같은 지역입니다.",
            "대표음식": "곤드레밥", "대표음식_설명": "정선의 대표 향토 음식으로, 건강에 좋은 곤드레나물을 넣어 지은 밥.",
            "대표음식_img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80",
            "특산품": "곤드레", "특산품_설명": "해발 700m 고산지대에서 자란 향긋한 곤드레.",
            "특산품_img": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=600&q=80",
            "축제": "정선 아리랑제", "축제_설명": "정선아리랑을 주제로 한 전통 문화 축제.",
            "축제_img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [
                {"이름": "정선곤드레본가", "평점": "★ 4.6 (126)", "주소": "정선읍 5일장길 31", "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=300&q=80"},
                {"이름": "함백산식당", "평점": "★ 4.4 (98)", "주소": "고한읍 고한로 123", "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=300&q=80"},
                {"이름": "정선아리랑시장 맛집", "평점": "★ 4.3 (87)", "주소": "정선읍 봉양3길 322", "img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 2, "지역": "전라남도 구례군", "위도": 35.2025, "경도": 127.4628, "점수": 87.3,
            "인구": "24,800명", "면적": "429.80㎢", "음식점수": "38개", "관광지수": "75개",
            "소개": "지리산 자락 청정 자연 속에서 산수유와 산채 요리를 만나볼 수 있는 구례입니다.",
            "대표음식": "산채정식", "대표음식_설명": "지리산에서 채취한 다양한 나물과 정갈한 반찬으로 차려낸 한상.",
            "대표음식_img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
            "특산품": "산수유", "특산품_설명": "봄을 알리는 붉은 보석, 영양 가득한 구례 산수유.",
            "특산품_img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
            "축제": "구례 산수유꽃축제", "축제_설명": "노란 산수유 꽃물결을 감상하는 대표 봄축제.",
            "축제_img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [
                {"이름": "지리산산채식당", "평점": "★ 4.8 (210)", "주소": "구례군 마산면 88", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 3, "지역": "경상남도 의령군", "위도": 35.3222, "경도": 128.2617, "점수": 86.1,
            "인구": "26,100명", "면적": "482.90㎢", "음식점수": "32개", "관광지수": "58개",
            "소개": "소바와 의령망개떡이 유명하며 맑은 남강이 흐르는 정겨운 로컬 도시입니다.",
            "대표음식": "의령소바", "대표음식_설명": "진한 메밀향과 메밀면의 쫄깃함이 일품인 대표 별미.",
            "대표음식_img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=600&q=80",
            "특산품": "망개떡", "특산품_설명": "청망개잎으로 감싸 향긋함이 더해진 찹쌀떡.",
            "특산품_img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
            "축제": "의령 의병제전", "축제_설명": "임진왜란 의병들의 숭고한 호국정신을 기리는 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [
                {"이름": "의령소바 본점", "평점": "★ 4.5 (320)", "주소": "의령읍 의병로 18", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 4, "지역": "전라북도 무주군", "위도": 35.9861, "경도": 127.6606, "점수": 84.9,
            "인구": "23,500명", "면적": "631.80㎢", "음식점수": "41개", "관광지수": "82개",
            "소개": "덕유산의 웅장함과 청정 반딧불이가 숨쉬는 힐링 여행지입니다.",
            "대표음식": "어죽", "대표음식_설명": "금강 상류의 민물고기로 푹 끓여낸 얼큰하고 담백한 별미.",
            "대표음식_img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
            "특산품": "머루와인", "특산품_설명": "덕유산 자락에서 재배된 산머루로 만든 깊은 풍미의 와인.",
            "특산품_img": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80",
            "축제": "무주 반딧불축제", "축제_설명": "천연기념물 반딧불이와 함께하는 생태 환경 축제.",
            "축제_img": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [
                {"이름": "금강식당 어죽", "평점": "★ 4.7 (180)", "주소": "무주읍 단산리 12", "img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 5, "지역": "충청북도 단양군", "위도": 36.9845, "경도": 128.3657, "점수": 84.2,
            "인구": "28,105명", "면적": "780.10㎢", "음식점수": "52개", "관광지수": "88개",
            "소개": "단양팔경의 수려한 자연경관과 마늘 특산 요리가 어우러진 휴양 도시입니다.",
            "대표음식": "마늘떡갈비", "대표음식_설명": "단양 특산물인 육쪽마늘을 더해 깊은 풍미를 자랑하는 떡갈비.",
            "대표음식_img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80",
            "특산품": "단양 마늘", "특산품_설명": "단단하고 향이 강해 전국 최고의 품질을 자랑하는 마늘.",
            "특산품_img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80",
            "축제": "단양 마늘축제", "축제_설명": "단양 마늘과 로컬 먹거리를 만끽하는 여름 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [
                {"이름": "단양마늘원조집", "평점": "★ 4.7 (150)", "주소": "단양읍 중앙로 15", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 6, "지역": "경상북도 영양군", "위도": 36.6667, "경도": 129.1118, "점수": 83.5,
            "인구": "16,000명", "면적": "815.10㎢", "음식점수": "25개", "관광지수": "45개",
            "소개": "아시아 최초 밤하늘 보호공원이 위치한 별빛 가득한 오지 로컬 명소.",
            "대표음식": "산나물비빔밥", "대표음식_설명": "영양의 깨끗한 고산지대에서 채취한 산나물 뷔페식 비빔밥.",
            "대표음식_img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
            "특산품": "영양 고추", "특산품_설명": "빛깔이 곱고 매운맛이 적당하며 당도가 높은 명품 고추.",
            "특산품_img": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?auto=format&fit=crop&w=600&q=80",
            "축제": "영양 산나물축제", "축제_설명": "봄철 싱싱한 산나물을 맛보고 경험하는 축제.",
            "축제_img": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [{"이름": "선바위가든", "평점": "★ 4.5 (62)", "주소": "영양읍 입암면 45", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=300&q=80"}]
        },
        {
            "id": 7, "지역": "경상북도 청송군", "위도": 36.4356, "경도": 129.0572, "점수": 82.8,
            "인구": "24,000명", "면적": "842.60㎢", "음식점수": "35개", "관광지수": "65개",
            "소개": "주왕산 국립공원의 절경과 달기약수탕, 꿀사과가 유명한 힐링 명소.",
            "대표음식": "달기약수백숙", "대표음식_설명": "탄산 약수로 끓여 닭고기가 부드럽고 국물이 깊은 약선 요리.",
            "대표음식_img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
            "특산품": "청송 사과", "특산품_설명": "해발이 높고 일교차가 크며 즙이 많은 명품 꿀사과.",
            "특산품_img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80",
            "축제": "청송 사과축제", "축제_설명": "가을철 사과 수확 기쁨을 나누는 경북 대표 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [{"이름": "서울여관식당", "평점": "★ 4.6 (140)", "주소": "청송읍 약수길 18", "img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=300&q=80"}]
        },
        {
            "id": 8, "지역": "충청남도 태안군", "위도": 36.7456, "경도": 126.2981, "점수": 81.9,
            "인구": "62,000명", "면적": "500.80㎢", "음식점수": "78개", "관광지수": "110개",
            "소개": "서해안 해안선과 안면도 소나무 숲, 풍부한 해산물이 어우러진 해양 도시.",
            "대표음식": "게국지", "대표음식_설명": "꽃게와 겉절이 김치를 넣고 시원하게 끓여낸 충남 향토 음식.",
            "대표음식_img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80",
            "특산품": "태안 꽃게", "특산품_설명": "살이 살찌고 알이 찬 서해안 청정 꽃게.",
            "특산품_img": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
            "축제": "태안 튤립꽃축제", "축제_설명": "세계 5대 튤립축제로 꼽히는 화려한 꽃의 향연.",
            "축제_img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [{"이름": "딴뚝통나무집", "평점": "★ 4.5 (410)", "주소": "안면읍 승언리 67", "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=300&q=80"}]
        },
        {
            "id": 9, "지역": "전라남도 고흥군", "위도": 34.6114, "경도": 127.2842, "점수": 80.4,
            "인구": "62,500명", "면적": "807.30㎢", "음식점수": "55개", "관광지수": "70개",
            "소개": "우주항공의 중심지이자 따뜻한 해양성 기후로 유자와 삼치가 유명한 곳.",
            "대표음식": "삼치회", "대표음식_설명": "입안에서 부드럽게 녹아내리는 신선한 삼치회.",
            "대표음식_img": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
            "특산품": "고흥 유자", "특산품_설명": "일조량이 풍부하여 향과 맛이 으뜸인 명품 유자.",
            "특산품_img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80",
            "축제": "고흥 우주항공축제", "축제_설명": "나로우주센터와 함께하는 이색 과학 테마 축제.",
            "축제_img": "https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [{"이름": "나로도수산식당", "평점": "★ 4.6 (95)", "주소": "동일면 봉영리 12", "img": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=300&q=80"}]
        },
        {
            "id": 10, "지역": "경상북도 울릉군", "위도": 37.4844, "경도": 130.9057, "점수": 79.8,
            "인구": "8,900명", "면적": "72.90㎢", "음식점수": "40개", "관광지수": "60개",
            "소개": "동해의 에메랄드빛 보석, 천혜의 화산섬 지형과 독도를 품은 신비로운 섬.",
            "대표음식": "오징어내장탕", "대표음식_설명": "울릉도 신선한 오징어로 끓여 시원하고 칼칼한 국물 요리.",
            "대표음식_img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
            "특산품": "울릉 명이나물", "특산품_설명": "울릉도 자생 산마늘로 담근 알싸하고 짭조름한 장아찌.",
            "특산품_img": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=600&q=80",
            "축제": "울릉도 오징어축제", "축제_설명": "동해안 대표 수산물 오징어를 테마로 한 체험형 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
            "맛집목록": [{"이름": "울릉약소마을", "평점": "★ 4.7 (130)", "주소": "울릉읍 도동리 88", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=300&q=80"}]
        }
    ]

data = load_data()
df = pd.DataFrame(data)

# 세션 상태 설정
if "selected_region_id" not in st.session_state:
    st.session_state.selected_region_id = 1

# =========================================================
# 4. 사이드바 (필터 컨트롤)
# =========================================================
with st.sidebar:
    st.markdown("<h4 style='font-weight:700; color:#ffffff;'>🔍 지역 탐색 필터</h4>", unsafe_allow_html=True)
    
    score_slider = st.slider("최소 숨은 지역 점수", 0, 100, 60)
    food_type = st.selectbox("선호 음식 타입", ["전체", "향토음식", "해산물", "산채요리", "육류"])
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>지도 표시 옵션</p>", unsafe_allow_html=True)
    chk_pin = st.checkbox("추천 지역 핀", value=True)
    chk_food = st.checkbox("음식점", value=True)
    chk_tour = st.checkbox("관광지", value=True)
    chk_fest = st.checkbox("축제/행사", value=True)
    chk_prod = st.checkbox("특산품", value=True)
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>정렬 기준</p>", unsafe_allow_html=True)
    sort_order = st.selectbox("", ["숨은 지역 점수 순", "인구 적은 순", "관광지 많은 순"], label_visibility="collapsed")
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>키워드 검색</p>", unsafe_allow_html=True)
    keyword = st.text_input("", placeholder="지역명 또는 키워드 입력", label_visibility="collapsed")
    
    st.button("검색", use_container_width=True, type="primary")
    
    if st.button("🔄 필터 초기화", use_container_width=True):
        st.session_state.selected_region_id = 1
        st.rerun()

# =========================================================
# 5. 헤더 타이틀 및 상단 카드
# =========================================================
st.markdown("""
<div class="main-header">
    <div>
        <div class="header-title-box">
            <span class="header-icon">🚗</span>
            <h1 class="header-title">SGIS(통계지리정보서비스)를 활용한 숨은 지역 발견</h1>
        </div>
        <div class="header-subtitle">SGIS(통계지리정보서비스)로 발견하는 대한민국의 숨은 지역과 로컬 경험</div>
    </div>
    <div class="fav-btn">♥ 찜한 지역 0</div>
</div>
""", unsafe_allow_html=True)

# 지표 계산
filtered_df = df[df["점수"] >= score_slider]
if keyword:
    filtered_df = filtered_df[filtered_df["지역"].str.contains(keyword) | filtered_df["소개"].str.contains(keyword)]

avg_score = filtered_df["점수"].mean() if not filtered_df.empty else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#1b382b; color:#2b8a3e;">★</div>
            <div>
                <div class="metric-label">추천 지역 수</div>
                <div class="metric-value">{len(filtered_df)}곳</div>
                <div class="metric-sub">조건에 맞는 지역</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#182c4d; color:#339af0;">📈</div>
            <div>
                <div class="metric-label">평균 숨은 점수</div>
                <div class="metric-value">{avg_score:.1f}점</div>
                <div class="metric-sub">상위 30% 지역</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#2b2353; color:#91a7ff;">💬</div>
            <div>
                <div class="metric-label">리뷰 수</div>
                <div class="metric-value">237개</div>
                <div class="metric-sub">실제 방문객 리뷰</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#423213; color:#fcc419;">🎁</div>
            <div>
                <div class="metric-label">특산품</div>
                <div class="metric-value">32개</div>
                <div class="metric-sub">지역 특산품</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 6. 지도 및 범례
# =========================================================
st.markdown("<h3 style='font-size:18px; font-weight:700; margin-top:25px; margin-bottom:10px; color:#ffffff;'>🗺️ 추천 지역 지도</h3>", unsafe_allow_html=True)

# 현재 선택된 데이터
curr_data = df[df["id"] == st.session_state.selected_region_id].iloc[0]

# 지도 생성 (다크 모드 레이어 타일 적용: CartoDB dark_all)
# Vworld WMTS 오픈 API 타일 URL (인증키 없이 사용 가능한 공용 오픈 URL 적용)
satellite_url = "https://map.vworld.kr/jquery/plugins/openlayers/theme/default/img/blank.gif" # fallback 예시

# Vworld 위성 지도 (Satellite)
m = folium.Map(
    location=[curr_data["위도"], curr_data["경도"]],
    zoom_start=8,
    tiles="https://xdworld.vworld.kr/2d/Satellite/service/{z}/{x}/{y}.jpeg",
    attr="Vworld Satellite"
)

# Vworld 지명/도로망 레이어 (Hybrid)
folium.TileLayer(
    tiles="https://xdworld.vworld.kr/2d/Hybrid/service/{z}/{x}/{y}.png",
    attr="Vworld Hybrid",
    name="Hybrid",
    overlay=True
).add_to(m)
# 마커 추가
for _, row in filtered_df.iterrows():
    is_sel = (row["id"] == st.session_state.selected_region_id)
    color = "red" if row["점수"] >= 85 else ("orange" if row["점수"] >= 80 else "blue")
    
    popup_html = f"""
    <div style='width:160px; font-family:sans-serif;'>
        <b>{row['지역']}</b><br>
        <span style='color:#e63946; font-size:12px;'>★ 숨은 지역 점수 {row['점수']}점</span><br>
        <span style='font-size:11px; color:#555;'>대표 음식: {row['대표음식']}</span>
    </div>
    """
    
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=200),
        tooltip=row["지역"],
        icon=folium.Icon(color="red" if is_sel else color, icon="star" if is_sel else "info-sign")
    ).add_to(m)

st_folium(m, use_container_width=True, height=450, returned_objects=[])

# 범례 표시
st.markdown("""
<div class="legend-container">
    <div class="legend-item"><div class="legend-dot" style="background:#e63946;"></div> 숨은 점수 90점 이상</div>
    <div class="legend-item"><div class="legend-dot" style="background:#f76707;"></div> 80~90점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#2f9e44;"></div> 70~80점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#1c7ed6;"></div> 60~70점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#868e96;"></div> 60점 이하</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. 지역 상세 정보 카드 & 길찾기 연동
# =========================================================
sec_col1, sec_col2 = st.columns([3, 1])
with sec_col1:
    st.markdown(f"<div class='section-title'>📍 {curr_data['지역']} 상세 정보</div>", unsafe_allow_html=True)
with sec_col2:
    selected_name = st.selectbox(
        "목록으로 돌아가기",
        df["지역"].tolist(),
        index=df["지역"].tolist().index(curr_data["지역"]),
        label_visibility="collapsed"
    )
    # 변경 시 업데이트
    new_id = df[df["지역"] == selected_name].iloc[0]["id"]
    if new_id != st.session_state.selected_region_id:
        st.session_state.selected_region_id = new_id
        st.rerun()

# 길찾기 URL 생성 (네이버 / 카카오)
encoded_region = urllib.parse.quote(curr_data['지역'])
naver_navi_url = f"https://map.naver.com/v5/directions/-/-/-/nat?e={curr_data['경도']},{curr_data['위도']},{encoded_region},,,ADDRESS_POI"
kakao_navi_url = f"https://map.kakao.com/link/to/{encoded_region},{curr_data['위도']},{curr_data['경도']}"

dc1, dc2, dc3, dc4 = st.columns([1.3, 1, 1, 1])

# 메인 카드가 포함된 4열 구조
with dc1:
    st.markdown(f"""
    <div class="main-region-card">
        <span class="badge-score">숨은 점수 {curr_data['점수']}점</span>
        <img src="{curr_data['메인이미지']}" class="main-region-img">
        <div class="main-region-body">
            <div class="main-region-desc">{curr_data['소개']}</div>
            <div class="stat-grid">
                <div>
                    <div class="stat-item-label">👥 인구</div>
                    <div class="stat-item-val">{curr_data['인구']}</div>
                </div>
                <div>
                    <div class="stat-item-label">📐 면적</div>
                    <div class="stat-item-val">{curr_data['면적']}</div>
                </div>
                <div>
                    <div class="stat-item-label">🍚 음식점</div>
                    <div class="stat-item-val">{curr_data['음식점수']}</div>
                </div>
                <div>
                    <div class="stat-item-label">🏞️ 관광지</div>
                    <div class="stat-item-val">{curr_data['관광지수']}</div>
                </div>
            </div>
            <div style="margin-top:15px; font-size:12px; font-weight:700; color:#ffffff;">🚗 길찾기</div>
            <div class="navi-btn-container">
                <a href="{naver_navi_url}" target="_blank" class="navi-btn-naver">네이버 지도</a>
                <a href="{kakao_navi_url}" target="_blank" class="navi-btn-kakao">카카오맵</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with dc2:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">대표 음식</div>
        <img src="{curr_data['대표음식_img']}" class="sub-info-img">
        <div class="sub-info-name">{curr_data['대표음식']}</div>
        <div class="sub-info-desc">{curr_data['대표음식_설명']}</div>
        <a href="#" class="btn-more">더 알아보기</a>
    </div>
    """, unsafe_allow_html=True)

with dc3:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">주요 특산품</div>
        <img src="{curr_data['특산품_img']}" class="sub-info-img">
        <div class="sub-info-name">{curr_data['특산품']}</div>
        <div class="sub-info-desc">{curr_data['특산품_설명']}</div>
        <a href="#" class="btn-more">더 알아보기</a>
    </div>
    """, unsafe_allow_html=True)

with dc4:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">대표 축제</div>
        <img src="{curr_data['축제_img']}" class="sub-info-img">
        <div class="sub-info-name">{curr_data['축제']}</div>
        <div class="sub-info-desc">{curr_data['축제_설명']}</div>
        <a href="#" class="btn-more">더 알아보기</a>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 8. 상세 하단 탭
# =========================================================
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🍚 음식&맛집", "🏞️ 관광지", "🎉 축제&행사", "🎁 특산품", "💬 리뷰 (32)"])

with tab1:
    tc1, tc2 = st.columns([1, 2.5])
    with tc1:
        st.markdown(f"""
        <div class="sub-info-card">
            <div class="sub-info-title">대표 음식</div>
            <img src="{curr_data['대표음식_img']}" style="width:100%; height:140px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
            <div class="sub-info-name">{curr_data['대표음식']}</div>
            <div class="sub-info-desc">{curr_data['대표음식_설명']}</div>
            <a href="#" class="btn-more">더 알아보기</a>
        </div>
        """, unsafe_allow_html=True)
    
    with tc2:
        st.markdown("<div class='sub-info-title' style='margin-bottom:10px;'>추천 맛집</div>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        
        for idx, res in enumerate(curr_data["맛집목록"]):
            target_col = [rc1, rc2, rc3][idx % 3]
            encoded_res_name = urllib.parse.quote(res['이름'])
            res_naver_url = f"https://map.naver.com/v5/search/{encoded_res_name}"
            
            with target_col:
                st.markdown(f"""
                <div class="place-card">
                    <img src="{res['img']}" class="place-img">
                    <div>
                        <div class="place-name">{res['이름']}</div>
                        <div class="place-star">{res['평점']}</div>
                        <div class="place-addr">📍 {res['주소']}</div>
                        <a href="{res_naver_url}" target="_blank" style="font-size:11px; color:#339af0; text-decoration:none; display:inline-block; margin-top:4px;">네이버 지도 보기 ></a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.info(f"{curr_data['지역']}의 주요 관광지 정보 페이지입니다.")

with tab3:
    st.info(f"{curr_data['지역']}의 주요 축제 및 행사 정보 페이지입니다.")

with tab4:
    st.info(f"{curr_data['지역']}의 주요 특산품 정보 페이지입니다.")

with tab5:
    st.markdown("<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'><span style='font-size:14px; font-weight:700; color:#ffffff;'>실제 방문객 리뷰</span><a href='#' style='font-size:12px; color:#339af0;'>전체 리뷰 보기 ></a></div>", unsafe_allow_html=True)
    
    rev_c1, rev_c2, rev_c3, rev_c4 = st.columns(4)
    
    reviews = [
        {"user": "여행매니아", "date": "2024.05.12", "text": "자연경관이 정말 아름답고 음식도 건강하고 맛있어요! 대표 음식 꼭 드셔보세요.", "star": "★★★★★ 5"},
        {"user": "산책러버", "date": "2024.04.28", "text": "전통시장 구경도 재밌고 주민들도 친절하세요. 지역 분위기가 정말 정겹습니다.", "star": "★★★★★ 5"},
        {"user": "맛집탐방가", "date": "2024.04.15", "text": "조용하고 깨끗해서 힐링하기 좋아요. 지방은 역시 식도락 여행이 최고!", "star": "★★★★☆ 4"},
        {"user": "캠핑가는부자", "date": "2024.03.10", "text": "주변 관광지와 산책로가 가을에 꼭 가보세요. 풍경이 정말 장관입니다.", "star": "★★★★★ 5"}
    ]
    
    for idx, rev in enumerate(reviews):
        with [rev_c1, rev_c2, rev_c3, rev_c4][idx]:
            st.markdown(f"""
            <div class="review-card">
                <div class="review-header">
                    <div class="review-user">
                        <div class="review-avatar">👤</div>
                        <div>
                            <div class="review-username">{rev['user']}</div>
                            <div style="font-size:10px; color:#fcc419;">{rev['star']}</div>
                        </div>
                    </div>
                    <div class="review-date">{rev['date']}</div>
                </div>
                <div class="review-text">{rev['text']}</div>
                <div class="review-imgs">
                    <img src="{curr_data['메인이미지']}" class="review-img">
                    <img src="{curr_data['대표음식_img']}" class="review-img">
                </div>
            </div>
            """, unsafe_allow_html=True)
