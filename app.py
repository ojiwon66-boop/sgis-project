import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =========================================================
# 1. 페이지 설정 및 CSS
# =========================================================
st.set_page_config(page_title="SGIS 로컬 큐레이션", page_icon="📍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #121212 !important; color: #e0e0e0 !important; font-family: 'Pretendard', sans-serif;}
.main .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; max-width: 1280px !important; }
section[data-testid="stSidebar"] { background-color: #1e1e1e !important; border-right: 1px solid #2d2d2d !important; }
.main-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.header-title-box { display: flex; align-items: center; gap: 10px; }
.header-icon { font-size: 28px; color: #ff6b6b; }
.header-title { font-size: 28px; font-weight: 800; color: #ffffff !important; margin: 0; }
.header-subtitle { font-size: 14px; color: #a0a0a0; margin-top: 4px; }
.metric-card { background: #1e1e1e; border-radius: 12px; padding: 16px 20px; border: 1px solid #2d2d2d; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: space-between; }
.metric-left { display: flex; align-items: center; gap: 12px; }
.metric-icon { width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.metric-label { font-size: 12px; color: #a0a0a0; font-weight: 600; }
.metric-value { font-size: 20px; font-weight: 800; color: #ffffff; }
.metric-sub { font-size: 11px; color: #707070; margin-top: 2px; }
.main-region-card { background: #1e1e1e; border-radius: 12px; border: 1px solid #2d2d2d; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.3); height: 100%; position: relative; }
.main-region-img { width: 100%; height: 160px; object-fit: cover; }
.badge-theme { position: absolute; top: 12px; right: 12px; background: #339af0; color: white; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.5); }
.main-region-body { padding: 16px; }
.main-region-desc { font-size: 13px; color: #cccccc; line-height: 1.5; margin-bottom: 15px; }
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; border-top: 1px solid #2d2d2d; padding-top: 12px; text-align: center; }
.stat-item-label { font-size: 11px; color: #ff6b6b; font-weight:600; }
.stat-item-val { font-size: 14px; font-weight: 800; color: #ffffff; margin-top:2px; }
.navi-btn-container { display: flex; gap: 8px; margin-top: 15px; }
.navi-btn-naver { flex: 1; background-color: #03C75A; color: white !important; text-align: center; padding: 10px 0; border-radius: 6px; font-size: 12px; font-weight: 700; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. 데이터 로드 
# =========================================================
@st.cache_data
def load_data():
    return [
        {
            "id": 1, "지역": "전라남도 구례군", "위도": 35.2025, "경도": 127.4628, 
            "테마": "완벽한 언택트 휴식", "추천이유": "인구 밀도 하위 5%, 프랜차이즈 없는 진짜 시골",
            "언택트지수": 98, "노포비율": 75, "프랜차이즈율": 2, "워라밸지수": 90,
            "소개": "반경 1km 내 대형 마트와 프랜차이즈 카페가 단 한 곳도 없는 곳. 지리산 자락에서 사람 마주칠 일 없이 완벽한 고립과 힐링을 원한다면 최적의 장소입니다.",
            "대표음식": "지리산 산채정식", "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 2, "지역": "경상북도 청송군", "위도": 36.4356, "경도": 129.0572, 
            "테마": "로컬 찐 노포 탐험", "추천이유": "10년 이상 생존한 백년가게 밀집 구역",
            "언택트지수": 85, "노포비율": 88, "프랜차이즈율": 5, "워라밸지수": 82,
            "소개": "관광객용 식당은 없습니다. SGIS 사업체 생애주기 분석 결과, 평균 영업 기간 15년 이상의 '진짜 현지인 맛집'만 살아남은 궁극의 미식 골목이 숨어있습니다.",
            "대표음식": "달기약수백숙", "메인이미지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 3, "지역": "전라북도 무주군", "위도": 35.9861, "경도": 127.6606, 
            "테마": "차박/캠핑 명당", "추천이유": "공중화장실+자연경관 교집합 격자 발견",
            "언택트지수": 92, "노포비율": 60, "프랜차이즈율": 8, "워라밸지수": 95,
            "소개": "금강 상류의 평탄한 지형이면서도 반경 500m 내에 편의점과 개방 화장실이 존재하는, SGIS 공간 분석이 찾아낸 '완벽한 차박/노지 캠핑' 스팟입니다.",
            "대표음식": "어죽", "메인이미지": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 4, "지역": "경상남도 의령군", "위도": 35.3222, "경도": 128.2617, 
            "테마": "촌캉스/워케이션", "추천이유": "저렴한 빈집 밀집도 + 청년 유입 증가 추세",
            "언택트지수": 88, "노포비율": 70, "프랜차이즈율": 4, "워라밸지수": 97,
            "소개": "노트북 하나 들고 한 달 살기 좋은 곳. 빈집을 개조한 감성 숙소와 청년 창업 카페들이 SGIS 통계상 최근 3년간 급증하고 있는 떠오르는 로컬 성지입니다.",
            "대표음식": "의령소바", "메인이미지": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1000&q=80"
        }
    ]

data = load_data()
df = pd.DataFrame(data)

# =========================================================
# 3. 사이드바 (기본 지역 검색 + 테마 필터 통합)
# =========================================================
with st.sidebar:
    st.markdown("<h4 style='font-weight:700; color:#ffffff;'>🔍 로컬 탐색 필터</h4>", unsafe_allow_html=True)
    st.caption("SGIS 격자 데이터 기반 맞춤형 분석")
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>1. 지역명으로 바로 찾기</p>", unsafe_allow_html=True)
    search_keyword = st.text_input("", placeholder="예: 구례, 청송, 무주...", label_visibility="collapsed")
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>2. 여행 취향(테마)으로 찾기</p>", unsafe_allow_html=True)
    selected_theme = st.selectbox("", ["전체", "완벽한 언택트 휴식", "로컬 찐 노포 탐험", "차박/캠핑 명당", "촌캉스/워케이션"], label_visibility="collapsed")
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>3. 데이터 딥다이브 슬라이더</p>", unsafe_allow_html=True)
    min_untact = st.slider("최소 언택트 지수 (유동인구 적은순)", 0, 100, 50)
    min_nopo = st.slider("최소 로컬 노포 비율 (%)", 0, 100, 30)
    
    st.button("조건 검색", use_container_width=True, type="primary")

# 필터 적용 로직
filtered_df = df
if search_keyword:
    filtered_df = filtered_df[filtered_df["지역"].str.contains(search_keyword)]
if selected_theme != "전체":
    filtered_df = filtered_df[filtered_df["테마"] == selected_theme]
filtered_df = filtered_df[filtered_df["언택트지수"] >= min_untact]
filtered_df = filtered_df[filtered_df["노포비율"] >= min_nopo]

# =========================================================
# 4. 헤더 및 메인 지표
# =========================================================
st.markdown("""
<div class="main-header">
    <div>
        <div class="header-title-box">
            <span class="header-icon">🎯</span>
            <h1 class="header-title">SGIS 로컬 라이프스타일 큐레이션</h1>
        </div>
        <div class="header-subtitle">단순한 지도가 아닙니다. 공간 통계가 당신의 취향에 맞는 완벽한 '격자'를 찾아냅니다.</div>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-left'><div class='metric-icon' style='background:#1b382b; color:#2b8a3e;'>🗺️</div><div><div class='metric-label'>검색된 맞춤 격자</div><div class='metric-value'>{len(filtered_df)}곳</div><div class='metric-sub'>조건 일치 구역</div></div></div></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-card'><div class='metric-left'><div class='metric-icon' style='background:#182c4d; color:#339af0;'>🚫</div><div><div class='metric-label'>평균 프랜차이즈율</div><div class='metric-value'>4.7%</div><div class='metric-sub'>대자본 없는 찐 로컬</div></div></div></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-card'><div class='metric-left'><div class='metric-icon' style='background:#2b2353; color:#91a7ff;'>👵</div><div><div class='metric-label'>로컬 노포 생존율</div><div class='metric-value'>73%</div><div class='metric-sub'>10년 이상 업력 유지</div></div></div></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='metric-card'><div class='metric-left'><div class='metric-icon' style='background:#423213; color:#fcc419;'>🏕️</div><div><div class='metric-label'>언택트 지수 평균</div><div class='metric-value'>90점</div><div class='metric-sub'>유동인구 최저 구역</div></div></div></div>", unsafe_allow_html=True)

# =========================================================
# 5. 지도 및 상세 정보 연동 (레이아웃 개선)
# =========================================================
st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

if not filtered_df.empty:
    curr_data = filtered_df.iloc[0] # 검색 결과 중 첫 번째 자동 선택
    
    # 🌟 스크롤을 내리지 않고도 한눈에 보이게 2단 구조로 변경!
    map_col, detail_col = st.columns([1.2, 1])
    
    with map_col:
        st.markdown("<h3 style='margin-bottom:10px; font-size:18px;'>🗺️ 취향 매칭 격자 지도</h3>", unsafe_allow_html=True)
        m = folium.Map(location=[curr_data["위도"], curr_data["경도"]], zoom_start=8, tiles="https://xdworld.vworld.kr/2d/Satellite/service/{z}/{x}/{y}.jpeg", attr="Vworld")
        folium.TileLayer(tiles="https://xdworld.vworld.kr/2d/Hybrid/service/{z}/{x}/{y}.png", attr="Vworld Hybrid", overlay=True).add_to(m)
        
        for _, row in filtered_df.iterrows():
            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=15, color="#ff6b6b", fill=True, fill_color="#ff6b6b", fill_opacity=0.6,
                popup=f"<b>{row['지역']}</b><br>{row['테마']}"
            ).add_to(m)

        st_folium(m, use_container_width=True, height=450, returned_objects=[])

    with detail_col:
        st.markdown(f"<h3 style='margin-bottom:10px; font-size:18px;'>📍 큐레이션 리포트: {curr_data['지역']}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="main-region-card">
            <span class="badge-theme">{curr_data['테마']} 99% 매칭</span>
            <img src="{curr_data['메인이미지']}" class="main-region-img">
            <div class="main-region-body">
                <div style="color:#339af0; font-size:12px; font-weight:700; margin-bottom:5px;">SGIS AI 분석 코멘트</div>
                <div class="main-region-desc">"{curr_data['추천이유']}"<br><br>{curr_data['소개']}</div>
                
                <div class="stat-grid">
                    <div>
                        <div class="stat-item-label">언택트 지수</div>
                        <div class="stat-item-val">{curr_data['언택트지수']}점</div>
                    </div>
                    <div>
                        <div class="stat-item-label">노포 생존율</div>
                        <div class="stat-item-val">{curr_data['노포비율']}%</div>
                    </div>
                    <div>
                        <div class="stat-item-label">프랜차이즈</div>
                        <div class="stat-item-val">{curr_data['프랜차이즈율']}%</div>
                    </div>
                    <div>
                        <div class="stat-item-label">워라밸 지수</div>
                        <div class="stat-item-val">{curr_data['워라밸지수']}점</div>
                    </div>
                </div>
                
                <div style="margin-top:15px;">
                    <a href="#" class="navi-btn-naver">네이버 지도로 이 격자 구역 안내받기</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("조건에 맞는 로컬 구역이 없습니다. 검색어(예: 구례)를 다시 확인하거나 필터를 조정해 보세요.")
