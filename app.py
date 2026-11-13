import random
import streamlit as st

# 1. 페이지 기본 설정 (파스텔 톤 타이틀 및 아이콘)
st.set_page_config(
    page_title="먼작귀 가위바위보!",
    page_icon="🎀",
    layout="centered",
)

# 2. 먼작귀 감성 커스텀 CSS 적용 (파스텔 배경, 둥근 버튼, 말풍선 카드)
st.markdown(
    """
    <style>
    /* 전체 배경을 포근한 파스텔 핑크 & 크림 그라데이션으로 설정 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #FFF9FB 0%, #FFF0F5 100%);
    }

    /* 상단 타이틀 배너 박스 */
    .chiikawa-banner {
        background-color: #FFFFFF;
        border: 3px solid #FFB7C5;
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 183, 197, 0.3);
        margin-bottom: 20px;
    }
    .chiikawa-banner h1 {
        color: #FF6B8B;
        font-size: 2rem;
        margin-bottom: 8px;
    }
    .chiikawa-banner p {
        color: #666666;
        font-size: 1rem;
        margin: 0;
    }

    /* 가위바위보 버튼 스타일 꾸미기 */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #4A4A4A;
        border: 2.5px solid #FFB7C5;
        border-radius: 20px;
        padding: 12px 10px;
        font-size: 1.15rem;
        font-weight: bold;
        box-shadow: 0 3px 6px rgba(255, 183, 197, 0.25);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #FFE4EC;
        border-color: #FF6B8B;
        color: #FF4D73;
        transform: translateY(-2px);
    }

    /* 캐릭터 말풍선 대결 카드 */
    .speech-card {
        background-color: #FFFFFF;
        border: 3px dashed #A2D2FF;
        border-radius: 22px;
        padding: 18px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(162, 210, 255, 0.25);
    }
    .char-face {
        font-size: 2.2rem;
        margin-bottom: 6px;
    }
    .char-quote {
        font-size: 1.15rem;
        font-weight: bold;
        color: #333333;
        background-color: #F4F9FF;
        padding: 10px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-top: 8px;
    }

    /* 전적판 메트릭 카드 스타일 */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 2px solid #FDE2E4;
        border-radius: 18px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 세션 상태 초기화
if "total_wins" not in st.session_state:
    st.session_state.total_wins = 0
if "total_losses" not in st.session_state:
    st.session_state.total_losses = 0
if "total_draws" not in st.session_state:
    st.session_state.total_draws = 0
if "match_user" not in st.session_state:
    st.session_state.match_user = 0
if "match_comp" not in st.session_state:
    st.session_state.match_comp = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False


def reset_match():
    st.session_state.match_user = 0
    st.session_state.match_comp = 0
    st.session_state.game_over = False


def reset_all():
    reset_match()
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.total_draws = 0


# 4. 먼작귀 캐릭터 데이터 (이모티콘 + 상황별 시그니처 대사)
characters = {
    "치이카와 🐹": {
        "face": "૮꒰ ˶• ༝ •˶꒱ა 🎀",
        "color": "#FFB7C5",
        "win_quotes": [
            "와아...! 이, 이겼다...!! ( ˶ˆᗜˆ˵ ) ✨",
            "해냈어...! 에헤헤... ( ⸝⸝•ᴗ•⸝⸝ )੭⁾⁾",
        ],
        "lose_quotes": [
            "으... 으아앙... 져버렸어... ( ; ω ; ) 💧",
            "히잉... 다음엔 안 질 거야... ( •̥ ˍ •̥ )",
        ],
        "draw_quotes": [
            "어라...? 똑같은 거 냈다...! (・o・) !",
            "찌찌뽕...! 신기해... ( ˶˙ᵕ˙˶ )",
        ],
    },
    "하치와레 🐱": {
        "face": "ฅ^•ﻌ•^ฅ 💙",
        "color": "#90DBF4",
        "win_quotes": [
            "해냈다~! 어떻게든 됐어! ✧٩(ˊωˋ*)و✧",
            "이겼다~! 오늘 간식은 맛있는 거 먹어야지! 🍜",
        ],
        "lose_quotes": [
            "앗, 져버렸네... 다음엔 꼭 이길 거야! (๑•̀ㅂ•́)و✧",
            "괜찮아! 아직 기회는 있으니까~! ( •̀ᴗ•́ )و",
        ],
        "draw_quotes": [
            "찌찌뽕! 우리 마음이 통했나 봐! ♪(´▽｀)",
            "막상막하인데?! 다시 한 번 승부하자! 🐾",
        ],
    },
    "우사기 🐰": {
        "face": "ᕱ⑅ᕱ 💛",
        "color": "#FDE4CF",
        "win_quotes": [
            "우라!! 야하~!! ٩( ᐛ )و 🎉",
            "하아?! 이 정도쯤이야! 푸루루루~ 🍮",
        ],
        "lose_quotes": [
            "하아?! 우라라라...!! ( ˘•ω•˘ ) 💥",
            "츠츠우라라... 다음 판 내놔!! (ง •̀_•́)ง",
        ],
        "draw_quotes": [
            "푸루루루~ 야하! ( ˙꒳​˙ ) ✨",
            "하아? 똑같잖아! 우라! 🐰",
        ],
    },
}

# 5. 상단 배너 UI
st.markdown(
    """
    <div class="chiikawa-banner">
        <h1>🎀 먼작귀 친구들과 삼세판 가위바위보! 🎀</h1>
        <p>귀여운 친구들과 <b>3판 2선승제</b> 대결을 펼쳐보세요! 먼저 2승을 하면 승리합니다 ✨</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. 대결할 먼작귀 캐릭터 선택
selected_char_name = st.radio(
    "✨ 대결할 먼작귀 친구를 골라주세요!",
    list(characters.keys()),
    horizontal=True,
)
char_info = characters[selected_char_name]

st.write("")

# 7. 가위/바위/보 버튼 3개 배치
choices = ["✌️ 가위", "✊ 바위", "✋ 보"]
user_choice = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button(
        "✌️ 가위", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✌️ 가위"
with col2:
    if st.button(
        "✊ 바위", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✊ 바위"
with col3:
    if st.button(
        "✋ 보", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✋ 보"

# 8. 대결 결과 및 캐릭터 말풍선 출력
if user_choice:
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        st.session_state.total_draws += 1
        quote = random.choice(char_info["draw_quotes"])
        result_badge = "🤝 비겼어요!"
        alert_type = "warning"
    elif (
        (user_choice == "✌️ 가위" and computer_choice == "✋ 보")
        or (user_choice == "✊ 바위" and computer_choice == "✌️ 가위")
        or (user_choice == "✋ 보" and computer_choice == "✊ 바위")
    ):
        st.session_state.total_wins += 1
        st.session_state.match_user += 1
        quote = random.choice(char_info["lose_quotes"])
        result_badge = "🎉 내가 이겼어요!"
        alert_type = "success"
    else:
        st.session_state.total_losses += 1
        st.session_state.match_comp += 1
        quote = random.choice(char_info["win_quotes"])
        result_badge = f"😭 {selected_char_name}의 승리!"
        alert_type = "error"

    # 캐릭터 말풍선 카드 렌더링
    st.markdown(
        f"""
        <div class="speech-card" style="border-color: {char_info['color']};">
            <div class="char-face">{char_info['face']}</div>
            <div style="font-size: 1.1rem; color: #555;">
                <b>나:</b> {user_choice} &nbsp;🆚&nbsp; <b>{selected_char_name}:</b> {computer_choice}
            </div>
            <div class="char-quote">"{quote}"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if alert_type == "success":
        st.success(f"{result_badge} 점수를 1점 획득했습니다!")
    elif alert_type == "error":
        st.error(f"{result_badge} 상대방이 1점을 획득했습니다!")
    else:
        st.warning(f"{result_badge} 점수는 그대로 유지됩니다.")

    # 삼세판 최종 승패 판정
    if st.session_state.match_user == 2:
        st.session_state.game_over = True
        st.balloons()
        st.success(
            f"🏆 **최종 우승!** {selected_char_name}에게서 삼세판 승리를 거뒀어요!"
        )
    elif st.session_state.match_comp == 2:
        st.session_state.game_over = True
        st.error(
            f"💦 **최종 패배...** {selected_char_name}가 삼세판에서 이겼어요!"
        )

if st.session_state.game_over:
    st.button("🔄 새로운 삼세판 시작하기", on_click=reset_match, type="primary")

# 9. 삼세판 스코어 및 누적 전적판
st.divider()
st.subheader("🎀 현재 삼세판 스코어 (2승 선취)")
m_col1, m_col2 = st.columns(2)
m_col1.metric("나의 승수 🧑", f"{st.session_state.match_user} 승")
m_col2.metric(
    f"{selected_char_name} 승수", f"{st.session_state.match_comp} 승"
)

st.subheader("📊 누적 승률 전적판")
total_games = (
    st.session_state.total_wins
    + st.session_state.total_losses
    + st.session_state.total_draws
)
win_rate = (
    (st.session_state.total_wins / total_games * 100) if total_games > 0 else 0.0
)

s_col1, s_col2, s_col3, s_col4 = st.columns(4)
s_col1.metric("승리 🏆", f"{st.session_state.total_wins}회")
s_col2.metric("패배 💧", f"{st.session_state.total_losses}회")
s_col3.metric("무승부 🤝", f"{st.session_state.total_draws}회")
s_col4.metric("승률 ✨", f"{win_rate:.1f}%")

st.write("")
st.button("🗑️ 전체 전적 초기화", on_click=reset_all)
