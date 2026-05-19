import streamlit as st
import datetime

# 1. 페이지 레이아웃 및 모던 모바일 UI 스타일 커스텀 정의
st.set_page_config(page_title="스위치온 다이어트 플래너", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경 회색 톤으로 모던하게 조정 */
    .stApp { background-color: #F8F9FA; }
    
    /* 모바일 카드 스타일 컨테이너 (그림자 및 테두리 라운드) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04) !important;
        border: none !important;
        padding: 16px !important;
        margin-bottom: 10px;
    }
    
    /* 상단 메인 날짜 및 타이틀 디자인 */
    .date-main { color: #333333; font-size: 15px; font-weight: 700; text-align: center; margin-bottom: 4px; }
    .day-main { color: #2F80ED; font-size: 24px; font-weight: 800; text-align: center; margin-bottom: 16px; }
    
    /* [달력 상단 날짜 카드 커스텀 디자인] */
    .cal-date-card {
        text-align: center;
        padding: 6px 2px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        line-height: 1.4;
        box-shadow: inset 0 0 0 1px #E0E0E0;
    }
    /* 요일별 글자 색상 세팅 */
    .cal-date-wd { background-color: #FFFFFF; color: #333333; } /* 평일: 검정 */
    .cal-date-sat { background-color: #FFFFFF; color: #2F80ED; } /* 토요일: 파란색 */
    .cal-date-sun { background-color: #FFFFFF; color: #EB5757; } /* 일요일: 빨간색 */
    
    /* 오늘 날짜: 완벽한 파란색 채우기 버튼 스타일 + 흰색 글씨 */
    .cal-date-today { 
        background-color: #2F80ED !important; 
        color: #FFFFFF !important; 
        box-shadow: 0 4px 10px rgba(47, 128, 237, 0.3) !important;
    }
    
    /* 달력 탭 내부 요약 식단/운동 템플릿 기본 스타일 */
    .cal-meal-text {
        font-size: 11px;
        padding: 4px 6px;
        border-radius: 6px;
        margin-top: 5px;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 600;
    }
    
    /* [달력 아이콘 상태별 배경색 지정] */
    .meal-status-normal { background-color: #F2F4F7; color: #4F4F4F; }
    .meal-status-done { background-color: #E8F5E9; color: #2E7D32; border: 1px solid #C8E6C9; }
    .meal-status-fail { background-color: #E0E0E0; color: #828282; text-decoration: line-through; }
    
    /* 주차별 타이틀 격차 여백 조정 */
    .week-title {
        font-size: 16px;
        font-weight: 700;
        color: #333333;
        margin-top: 25px !important;
        margin-bottom: 10px !important;
    }
    
    /* 오늘의 식단 텍스트-체크박스 라인 중앙 정렬 세팅 */
    .lbl-text {
        font-size: 14px;
        color: #333333;
        font-weight: 600;
        display: flex;
        align-items: center;
        height: 38px;
        background-color: #F2F4F7;
        padding-left: 14px;
        border-radius: 10px;
        margin: 0 !important;
    }
    
    div[data-testid="stColumn"] button {
        margin-top: 1px !important;
        height: 38px !important;
        padding: 0 !important;
    }
    
    /* 라디오 버튼 메뉴를 상단 탭 핀 형태로 스타일 최적화 */
    div[data-testid="stRadio"] > label { display: none; }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        flex-direction: row !important;
        justify-content: center;
        gap: 10px;
        background-color: #E0E0E0;
        padding: 6px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: transparent !important;
        border: none !important;
        padding: 6px 16px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #4F4F4F !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        color: #2F80ED !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 세션 상태 제어 ---
if "check_status" not in st.session_state:
    st.session_state.check_status = {day: {item: False for item in ["아침", "점심", "간식", "저녁", "운동"]} for day in range(1, 29)}

if "start_date" not in st.session_state:
    st.session_state.start_date = None

# --- 3. 최초 접속 시 다이어트 시작일 입력 레이어 ---
if st.session_state.start_date is None:
    st.title("🔥 스위치온 다이어트 플래너")
    st.write("반갑습니다, 영은님! 나만의 다이어트 어플 세팅을 위해 시작일을 먼저 선택해 주세요.")
    init_date = st.date_input("📅 다이어트 시작일 선택", datetime.date.today(), key="init_date_input")
    if st.button("🚀 나만의 어플 시작하기", type="primary"):
        st.session_state.start_date = init_date
        st.rerun()
    st.stop()

WEEKS_KOR = ["월", "화", "수", "목", "금", "토", "일"]

# --- 4. PDF 원본 기반 데이터 정의 및 아이콘 변환 함수 ---
FOOD_W1_3 = "두부, 무가당 플레인 요거트, 녹차, 허브티, 각종 채소류(오이, 브로콜리, 파프리카 등), 냉압착 오일류"
FOOD_W1_4 = "1~3일차 식품 + 잡곡밥 반공기, 생선, 회, 해산물 전 종류, 참치, 닭고기, 달걀, 버섯, 해조류, 삶은 고기류(수육, 샤브샤브), 김치"
FOOD_W2 = "1주차 식품 + 퀴노아, 콩류, 견과류, 블랙커피(오전 1잔), 우유 2잔, 무염치즈, 등푸른생선, 흰쌀밥"
FOOD_W3 = "2주차 식품 + 닭고기/소고기/돼지고기 등 육류(지방 적은 부위), 고구마, 바나나, 단호박, 밤, 토마토"
FOOD_W4 = "3주차 식품 + 과일 허용 (하루 딱 1개만)"

def get_day_data(day):
    data = {"아침": "쉐이크", "점심": "저탄수식", "간식": "쉐이크", "저녁": "무탄고단식", "식품": "주차별 허용식품"}
    if 1 <= day <= 3:
        data["점심"], data["저녁"] = "쉐이크", "쉐이크"; data["식품"] = FOOD_W1_3
    elif 4 <= day <= 7:
        data["점심"] = "저탄수식"; data["저녁"] = "쉐이크"; data["식품"] = FOOD_W1_4
    elif 8 <= day <= 14:
        data["식품"] = FOOD_W2
        if day == 10: data["아침"], data["점심"], data["간식"] = "단식", "단식", "단식"; data["식품"] = "2주차 단식일"
    elif 15 <= day <= 21:
        data["저녁"] = "무탄고단식"; data["식품"] = FOOD_W3
        if day in [16, 19]: data["아침"], data["점심"], data["간식"] = "단식", "단식", "단식"; data["식품"] = "3주차 단식일"
    elif 22 <= day <= 28:
        data["점심"], data["저녁"] = "일반식", "저탄수식"; data["식품"] = FOOD_W4
        if day in [23, 25, 27]: data["아침"], data["점심"], data["간식"] = "단식", "단식", "단식"
        elif day == 28: data["점심"], data["간식"], data["저녁"] = "자유식", "자유식", "자유식"; data["식품"] = "최종일 자유식"
    return data

def get_meal_icon_text(meal_name):
    if "쉐이크" in meal_name: return f"🍼 {meal_name}"
    elif "저탄수식" in meal_name: return f"🥗 {meal_name}"
    elif "무탄고단식" in meal_name: return f"🥩 {meal_name}"
    elif "단식" in meal_name: return f"❌ {meal_name}"
    elif "일반식" in meal_name or "자유식" in meal_name: return f"🍳 {meal_name}"
    elif "운동" in meal_name: return f"🏋️ {meal_name}"
    return meal_name

# --- 오늘 날짜 기준 플래너 일차 고정 기틀 세팅 ---
today = datetime.date.today()
elapsed_days = (today - st.session_state.start_date).days + 1
current_today_day = max(1, min(28, elapsed_days))

# --- 5. 상단 모바일 내비게이션 토글 바 ---
menu_options = ["🍽️ 오늘의 식단", "📅 전체 달력"]
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "🍽️ 오늘의 식단"

selected_tab = st.radio(
    label="메뉴",
    options=menu_options,
    index=menu_options.index(st.session_state.current_tab),
    key="tab_selector"
)

# ---------------------------------------------------------
# [화면 1] 오늘의 식단 페이지
# ---------------------------------------------------------
if selected_tab == "🍽️ 오늘의 식단":
    day_info = get_day_data(current_today_day)
    
    target_date = st.session_state.start_date + datetime.timedelta(days=current_today_day - 1)
    weekday_idx = target_date.weekday()
    day_of_week = WEEKS_KOR[weekday_idx]
    
    if weekday_idx == 5: color = "#2F80ED"
    elif weekday_idx == 6: color = "#EB5757"
    else: color = "#333333"
        
    st.markdown(f"<div class='date-main' style='color:{color};'>{target_date.strftime('%Y년 %m월 %d일')} ({day_of_week})</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='day-main'>Day {current_today_day}</div>", unsafe_allow_html=True)
            
    with st.container(border=True):
        # [수정] 영양제 항목은 리스트에서 완벽 제거
        task_items = [
            ("아침", f"아침: {day_info['아침']}"),
            ("점심", f"점심: {day_info['점심']}"),
            ("간식", f"간식: {day_info['간식']}"),
            ("저녁", f"저녁: {day_info['저녁']}"),
            ("운동", "운동")
        ]
        
        for item_key, item_label in task_items:
            is_done = st.session_state.check_status[current_today_day][item_key]
            btn_label = "✅" if is_done else "⬜"
            
            c_txt, c_btn = st.columns([4, 1])
            with c_txt:
                st.markdown(f"<div class='lbl-text'>{get_meal_icon_text(item_label)}</div>", unsafe_allow_html=True)
            with c_btn:
                if st.button(btn_label, key=f"main_b_{current_today_day}_{item_key}", use_container_width=True):
                    st.session_state.check_status[current_today_day][item_key] = not is_done
                    st.rerun()
                    
        st.write("")
        with st.popover("🍏 오늘의 허용식품 확인", use_container_width=True):
            st.write(day_info["식품"])

# ---------------------------------------------------------
# [화면 2] 전체 달력 페이지
# ---------------------------------------------------------
else:
    def get_style_class(target_day, item_key):
        is_completed = st.session_state.check_status[target_day][item_key]
        if is_completed: return "meal-status-done"
        elif target_day < current_today_day: return "meal-status-fail"
        return "meal-status-normal"

    for week in range(4):
        st.markdown(f"<div class='week-title'>📌 {week+1}주차</div>", unsafe_allow_html=True)
        cols = st.columns(7)
        
        for i in range(7):
            day_num = week * 7 + i + 1
            cal_day_info = get_day_data(day_num)
            
            cal_date = st.session_state.start_date + datetime.timedelta(days=day_num - 1)
            cal_weekday = cal_date.weekday()
            
            weekday_str = WEEKS_KOR[cal_weekday]
            date_display_text = f"Day {day_num}<br>{cal_date.strftime('%m/%d')}({weekday_str})"
            
            is_today = (day_num == current_today_day)
            
            # [복구 및 검증 완료] 요일별 커스텀 스타일 완벽 적용
            if is_today:
                date_card_class = "cal-date-card cal-date-today" # 오늘: 파란색 배경 + 흰색 글씨
            elif cal_weekday == 5:
                date_card_class = "cal-date-card cal-date-sat"   # 토요일: 파란색 글씨
            elif cal_weekday == 6:
                date_card_class = "cal-date-card cal-date-sun"   # 일요일: 빨간색 글씨
            else:
                date_card_class = "cal-date-card cal-date-wd"    # 평일: 검정색 글씨
            
            with cols[i]:
                st.markdown(f"<div class='{date_card_class}'>{date_display_text}</div>", unsafe_allow_html=True)
                
                # 아침, 점심, 간식, 저녁 + 운동까지 완벽히 연동 포함
                st.markdown(f"""
                    <div class='cal-meal-text {get_style_class(day_num, "아침")}'>{get_meal_icon_text(cal_day_info['아침'])}</div>
                    <div class='cal-meal-text {get_style_class(day_num, "점심")}'>{get_meal_icon_text(cal_day_info['점심'])}</div>
                    <div class='cal-meal-text {get_style_class(day_num, "간식")}'>{get_meal_icon_text(cal_day_info['간식'])}</div>
                    <div class='cal-meal-text {get_style_class(day_num, "저녁")}'>{get_meal_icon_text(cal_day_info['저녁'])}</div>
                    <div class='cal-meal-text {get_style_class(day_num, "운동")}'>{get_meal_icon_text("운동")}</div>
                """, unsafe_allow_html=True)

# --- 6. 환경설정 창 (앱 최하단 숨김 레이어) ---
st.markdown("---")
with st.expander("⚙️ 다이어트 시작일 변경 및 데이터 리셋"):
    change_date = st.date_input("새로운 시작일 설정", st.session_state.start_date)
    if st.button("🔄 날짜 재반영 및 시스템 초기화"):
        st.session_state.start_date = change_date
        st.rerun()

st.caption("🚨 공통 수칙: 14시간 공복 유지, 30분마다 일어나서 움직이기 필수!")