import streamlit as st
import datetime
import json
import os
import calendar

DATA_FILE = os.path.join(os.path.dirname(__file__), "diet_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if raw.get("start_date"):
                raw["start_date"] = datetime.date.fromisoformat(raw["start_date"])
            if raw.get("check_status"):
                raw["check_status"] = {int(k): v for k, v in raw["check_status"].items()}
            return raw
        except Exception:
            pass
    return {"start_date": None, "check_status": None}

def save_data():
    payload = {
        "start_date": st.session_state.start_date.isoformat() if st.session_state.start_date else None,
        "check_status": st.session_state.check_status,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="스위치온 다이어트", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background-color: #F2F4F7; }
.block-container { padding: 16px 12px 60px !important; max-width: 480px !important; margin: 0 auto; }

.month-header {
    text-align: center;
    font-size: 20px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 12px;
}
.wd-row {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    margin-bottom: 4px;
}
.wd-cell {
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 0;
    color: #64748B;
}
.wd-cell.sat { color: #2563EB; }
.wd-cell.sun { color: #DC2626; }

/* ── 달력 셀: 셀 클릭 ── */
.cal-cell-wrap {
    position: relative;
    width: 100%;
    margin-bottom: 3px;
}
.cal-cell {
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    min-height: 68px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5px 2px;
    transition: border-color 0.15s, background 0.15s;
    gap: 2px;
}
.cal-cell.empty {
    background: transparent;
    border-color: transparent;
}
.cal-cell.today { background: #2563EB; border-color: #2563EB; }
.cal-cell.today .cell-date { color: #FFFFFF; }
.cal-cell.today .cell-day  { color: #BFDBFE; }
.cal-cell.selected { background: #DBEAFE; border-color: #2563EB; }
.cal-cell.today.selected { background: #2563EB; border-color: #1D4ED8; box-shadow: 0 0 0 3px #BFDBFE; }
.cal-cell.past { opacity: 0.55; }
.cal-cell.sat .cell-date { color: #2563EB; }
.cal-cell.sun .cell-date { color: #DC2626; }

.cell-date { font-size: 16px; font-weight: 800; color: #1E293B; line-height: 1.1; }
.cell-day { font-size: 9px; font-weight: 600; color: #94A3B8; line-height: 1.2; }
.cell-dots { display: flex; gap: 3px; align-items: center; margin-top: 3px; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: #E2E8F0; flex-shrink: 0; }
.dot.green { background: #22C55E; }
.dot.blue  { background: #3B82F6; }

div[data-testid="stColumn"]:has(.cal-cell) {
    position: relative;
}
div[data-testid="stColumn"]:has(.cal-cell) div.element-container:has(button) {
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    width: 100% !important; height: 100% !important;
    z-index: 10 !important;
}
div[data-testid="stColumn"]:has(.cal-cell) button {
    width: 100% !important; height: 100% !important;
    opacity: 0 !important; cursor: pointer !important;
    border: none !important; background: transparent !important;
}

/* 🚀 핵심 해결 부분: 모바일 좁은 화면에서도 세로로 깨지지 않고 PC처럼 가로 유지 */
div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    align-items: center !important;
}
div[data-testid="stColumn"] {
    min-width: 0 !important;
}

/* ── 하단 상세 패널 ── */
.detail-panel {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 18px 16px 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-top: 6px;
}
.detail-title { font-size: 16px; font-weight: 800; color: #1E293B; margin-bottom: 12px; }
.detail-subtitle { font-size: 12px; color: #94A3B8; font-weight: 600; margin-left: 6px; }

.food-box {
    margin-top: 10px;
    padding: 10px 12px;
    background: #F0FDF4;
    border-radius: 10px;
    font-size: 11px;
    color: #166534;
    font-weight: 600;
    line-height: 1.65;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    border: none !important;
    padding: 14px !important;
}
.stCaption { font-size: 11px !important; color: #94A3B8 !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ── 세션 초기화 ─────────────────────────────────────────────────
if "data_loaded" not in st.session_state:
    saved = load_data()
    st.session_state.start_date = saved.get("start_date")
    default_status = {d: {k: False for k in ["아침","점심","간식","저녁","운동"]} for d in range(1, 29)}
    if saved.get("check_status"):
        for d in range(1, 29):
            if d in saved["check_status"]:
                default_status[d].update(saved["check_status"][d])
    st.session_state.check_status = default_status
    st.session_state.selected_day_num = None
    st.session_state.data_loaded = True

WEEKS_KOR  = ["월","화","수","목","금","토","일"]
MONTHS_KOR = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]

FOOD_W1_3 = "두부, 무가당 플레인 요거트, 녹차, 허브티, 각종 채소류(오이, 브로콜리, 파프리카 등), 냉압착 오일류"
FOOD_W1_4 = "1~3일차 식품 + 잡곡밥 반공기, 생선·회·해산물, 참치, 닭고기, 달걀, 버섯, 해조류, 삶은 고기류, 김치"
FOOD_W2   = "1주차 식품 + 퀴노아, 콩류, 견과류, 블랙커피(오전 1잔), 우유 2잔, 무염치즈, 등푸른생선, 흰쌀밥"
FOOD_W3   = "2주차 식품 + 닭/소/돼지(지방 적은 부위), 고구마, 바나나, 단호박, 밤, 토마토"
FOOD_W4   = "3주차 식품 + 과일 허용 (하루 딱 1개만)"

def get_day_data(day):
    d = {"아침":"쉐이크","점심":"저탄수식","간식":"쉐이크","저녁":"무탄고단식","식품":"주차별 허용식품"}
    if 1 <= day <= 3:
        d["점심"] = "쉐이크"; d["저녁"] = "쉐이크"; d["식품"] = FOOD_W1_3
    elif 4 <= day <= 7:
        d["점심"] = "저탄수식"; d["저녁"] = "쉐이크"; d["식품"] = FOOD_W1_4
    elif 8 <= day <= 14:
        d["식품"] = FOOD_W2
        if day == 10:
            d["아침"] = d["점심"] = d["간식"] = "단식"; d["식품"] = "2주차 단식일"
    elif 15 <= day <= 21:
        d["저녁"] = "무탄고단식"; d["식품"] = FOOD_W3
        if day in [16, 19]:
            d["아침"] = d["점심"] = d["간식"] = "단식"; d["식품"] = "3주차 단식일"
    elif 22 <= day <= 28:
        d["점심"] = "일반식"; d["저녁"] = "저탄수식"; d["식품"] = FOOD_W4
        if day in [23, 25, 27]:
            d["아침"] = d["점심"] = d["간식"] = "단식"
        elif day == 28:
            d["점심"] = d["간식"] = d["저녁"] = "자유식"; d["식품"] = "최종일 자유식"
    return d

MEAL_ICONS = {"쉐이크":"🍼","저탄수식":"🥗","무탄고단식":"🥩","단식":"❌","일반식":"🍳","자유식":"🎉","운동":"🏋️"}
def meal_icon(name):
    for k, v in MEAL_ICONS.items():
        if k in name: return f"{v} {name}"
    return name

today = datetime.date.today()

def get_current_day():
    if st.session_state.start_date is None: return None
    elapsed = (today - st.session_state.start_date).days + 1
    return elapsed if 1 <= elapsed <= 28 else None

# ── 시작일 입력 (최초 1회) ───────────────────────────────────────
if st.session_state.start_date is None:
    st.title("🔥 스위치온 다이어트")
    st.write("반갑습니다, 영은님! 시작일을 한 번만 설정하면 앱을 껐다 켜도 유지됩니다.")
    init_date = st.date_input("📅 다이어트 시작일 선택", today, key="init_date_input")
    if st.button("🚀 시작하기", type="primary"):
        st.session_state.start_date = init_date
        st.session_state.selected_day_num = None
        save_data()
        st.rerun()
    st.stop()

current_day = get_current_day()
start = st.session_state.start_date
end   = start + datetime.timedelta(days=27)

if st.session_state.selected_day_num is None and current_day is not None:
    st.session_state.selected_day_num = current_day

def date_to_daynum(d):
    delta = (d - start).days + 1
    return delta if 1 <= delta <= 28 else None

months_to_show = []
cur = datetime.date(start.year, start.month, 1)
last_month = datetime.date(end.year, end.month, 1)
while cur <= last_month:
    months_to_show.append((cur.year, cur.month))
    nm = cur.month + 1 if cur.month < 12 else 1
    ny = cur.year if cur.month < 12 else cur.year + 1
    cur = datetime.date(ny, nm, 1)

def dots_html(day_num):
    status = st.session_state.check_status[day_num]
    html = "<div class='cell-dots'>"
    for k in ["아침","점심","간식","저녁"]:
        cls = "dot green" if status[k] else "dot"
        html += f"<div class='{cls}'></div>"
    cls = "dot blue" if status["운동"] else "dot"
    html += f"<div class='{cls}'></div>"
    html += "</div>"
    return html

# ════════════════════════════════════════════════════════════════
# 달력 렌더링
# ════════════════════════════════════════════════════════════════
for (yr, mo) in months_to_show:
    st.markdown(f"<div class='month-header'>{yr}년 {MONTHS_KOR[mo-1]}</div>", unsafe_allow_html=True)

    wd_html = "<div class='wd-row'>"
    for lbl, cls in [("월",""),("화",""),("수",""),("목",""),("금",""),("토","sat"),("일","sun")]:
        wd_html += f"<div class='wd-cell {cls}'>{lbl}</div>"
    wd_html += "</div>"
    st.markdown(wd_html, unsafe_allow_html=True)

    first_wd      = datetime.date(yr, mo, 1).weekday()
    days_in_month = calendar.monthrange(yr, mo)[1]
    cells = [None] * first_wd + [datetime.date(yr, mo, d) for d in range(1, days_in_month + 1)]
    while len(cells) % 7 != 0:
        cells.append(None)

    for week_start in range(0, len(cells), 7):
        week_cells = cells[week_start:week_start+7]
        if not any(c is not None and start <= c <= end for c in week_cells):
            continue

        cols = st.columns(7)
        for i, cell_date in enumerate(week_cells):
            with cols[i]:
                if cell_date is None:
                    st.markdown("<div class='cal-cell-wrap empty-wrap'><div class='cal-cell empty'></div></div>", unsafe_allow_html=True)
                    continue

                day_num     = date_to_daynum(cell_date)
                wd_idx      = cell_date.weekday()
                is_today    = (cell_date == today)
                is_selected = (day_num is not None and day_num == st.session_state.selected_day_num)
                is_diet     = (day_num is not None)
                is_past     = (cell_date < today)

                cls_list = ["cal-cell"]
                if not is_diet:
                    cls_list.append("empty")
                else:
                    if is_today:    cls_list.append("today")
                    if is_selected: cls_list.append("selected")
                    if is_past and not is_today: cls_list.append("past")
                    if wd_idx == 5 and not is_today: cls_list.append("sat")
                    if wd_idx == 6 and not is_today: cls_list.append("sun")

                cell_cls = " ".join(cls_list)
                wrap_cls = "cal-cell-wrap" + (" empty-wrap" if not is_diet else "")
                d_html = dots_html(day_num) if is_diet else ""

                cell_html = f"""
                <div class='{wrap_cls}'>
                  <div class='{cell_cls}'>
                    <div class='cell-date'>{cell_date.day}</div>
                    <div class='cell-day'>{'Day ' + str(day_num) if is_diet else ''}</div>
                    {d_html}
                  </div>
                </div>
                """
                st.markdown(cell_html, unsafe_allow_html=True)

                if is_diet:
                    if st.button(" ", key=f"cal_{yr}_{mo}_{cell_date.day}", use_container_width=True):
                        st.session_state.selected_day_num = day_num
                        st.rerun()

# ════════════════════════════════════════════════════════════════
# 하단 상세 패널
# ════════════════════════════════════════════════════════════════
sel = st.session_state.selected_day_num

if sel is not None:
    sel_info    = get_day_data(sel)
    sel_date    = start + datetime.timedelta(days=sel - 1)
    sel_wd      = sel_date.weekday()
    sel_color   = {5:"#2563EB", 6:"#DC2626"}.get(sel_wd, "#1E293B")
    is_past_day = (sel_date < today)

    st.markdown(f"""
    <div class='detail-panel'>
      <div class='detail-title'>
        <span style='color:{sel_color}'>Day {sel}</span>
        <span class='detail-subtitle'>{sel_date.strftime('%m/%d')} ({WEEKS_KOR[sel_wd]})</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    items = [
        ("아침", f"아침: {sel_info['아침']}"),
        ("점심", f"점심: {sel_info['점심']}"),
        ("간식", f"간식: {sel_info['간식']}"),
        ("저녁", f"저녁: {sel_info['저녁']}"),
        ("운동", "운동"),
    ]

    with st.container(border=True):
        for item_key, item_label in items:
            is_done = st.session_state.check_status[sel][item_key]
            
            text_style = "font-size: 14px; font-weight: 600; color: #1E293B;"
            if is_done:
                text_style = "font-size: 14px; font-weight: 600; color: #15803D; text-decoration: line-through; opacity: 0.85;"
            elif is_past_day:
                text_style = "font-size: 14px; font-weight: 600; color: #94A3B8;"

            col_txt, col_btn = st.columns([6, 1], vertical_alignment="center")
            with col_txt:
                st.markdown(f"<div style='{text_style}'>{meal_icon(item_label)}</div>", unsafe_allow_html=True)
            with col_btn:
                if st.button("✅" if is_done else "⬜", key=f"chk_{sel}_{item_key}", use_container_width=True):
                    st.session_state.check_status[sel][item_key] = not is_done
                    save_data()
                    st.rerun()

        st.markdown(f"<div class='food-box'>🍏 허용식품: {sel_info['식품']}</div>", unsafe_allow_html=True)

else:
    st.markdown(
        "<div style='text-align:center;color:#94A3B8;font-size:13px;"
        "font-weight:600;padding:24px 0;'>날짜를 눌러 식단을 확인하세요 👆</div>",
        unsafe_allow_html=True
    )

# ── 환경설정 ─────────────────────────────────────────────────────
st.markdown("---")
with st.expander("⚙️ 시작일 변경 및 데이터 초기화"):
    change_date = st.date_input("새로운 시작일", st.session_state.start_date)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 날짜만 변경"):
            st.session_state.start_date = change_date
            save_data()
            st.rerun()
    with col2:
        if st.button("🗑️ 전체 초기화", type="secondary"):
            st.session_state.check_status = {
                d: {k: False for k in ["아침","점심","간식","저녁","운동"]}
                for d in range(1, 29)
            }
            st.session_state.start_date = change_date
            save_data()
            st.rerun()

st.caption("🚨 공통 수칙: 14시간 공복 유지 · 30분마다 일어나서 움직이기 필수!")