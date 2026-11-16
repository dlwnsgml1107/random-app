import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="먼작귀 가위바위보 대결!", page_icon="🐹", layout="centered"
)

# 2. 먼작귀 감성 커스텀 CSS 적용
st.markdown(
    """
<style>
    /* 전체 배경 파스텔 톤 */
    .stApp {
        background-color: #FFF9FB;
    }
    /* 타이틀 스타일 */
    .main-title {
        text-align: center;
        color: #FF6B9E;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 0px #FFE3EC;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #5C6B73;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    /* 버튼 스타일링 */
    div.stButton > button {
        width: 100%;
        height: 75px;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: 3px solid #FFD1DC !important;
        background-color: #FFFFFF !important;
        color: #4A4A4A !important;
        box-shadow: 0 4px 6px rgba(255, 182, 193, 0.3);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #FFE3EC !important;
        border-color: #FF6B9E !important;
        transform: translateY(-3px);
    }
    /* 전적판 & 스코어보드 박스 */
    .board-box {
        background-color: #FFFFFF;
        border: 2px dashed #A2D2FF;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .character-quote {
        font-size: 1.15rem;
        font-weight: 600;
        padding: 12px;
        border-radius: 12px;
        background-color: #F0F8FF;
        border-left: 5px solid #89CFF0;
        margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. 세션 상태(Session State) 초기화
if "total_win" not in st.session_state:
  st.session_state.total_win = 0
if "total_lose" not in st.session_state:
  st.session_state.total_lose = 0
if "total_draw" not in st.session_state:
  st.session_state.total_draw = 0

# 삼세판(3판 2선승제)용 상태
if "round_user" not in st.session_state:
  st.session_state.round_user = 0
if "round_com" not in st.session_state:
  st.session_state.round_com = 0
if "last_result" not in st.session_state:
  st.session_state.last_result = None

# 4. 먼작귀 캐릭터 멘트 데이터
WIN_QUOTES = [
    "🐹 치이카와: 에…?! 이겼어…!! 와아아!! (감격의 눈물)",
    "🐱 하치와레: 해냈잖아!! 오늘 저녁은 맛있는 거 먹자!",
    "🐰 우사기: 우라!! 야하!! (신나서 춤추는 중)",
    "🐹 치이카와: 우… 와아…! 엄청 강해…!!",
]

LOSE_QUOTES = [
    "🐰 우사기: 하아? 졌다니… 푸르르르!! (약 올리는 중)",
    "🐱 하치와레: 어… 어라?! 방금 건 실수지? 조금 더 노력해보세요 ㅋㅋ",
    "🐹 치이카와: 히잉… 져버렸어… 다음엔 꼭 이길 수 있어…!",
    "🐰 우사기: 이야하하하! (배 잡고 웃는 중)",
]

DRAW_QUOTES = [
    "🐱 하치와레: 오! 똑같은 걸 냈네! 마음이 통했나 봐!",
    "🐹 치이카와: 음… 비겼어…! 한 번 더!!",
    "🐰 우사기: 우라? (고개를 갸웃거린다)",
]

# 5. 상단 헤더 영역
st.markdown(
    '<div class="main-title">🐹 먼작귀 가위바위보 대결! 🐰</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">치이카와 친구들과 함께하는 <b>삼세판(3판 2선승제)</b>'
    " 승부! 먼저 2승을 달성하세요!</div>",
    unsafe_allow_html=True,
)

# 6. 현재 삼세판 스코어보드
st.markdown(
    f"""
<div class="board-box">
    <h4 style="margin:0; color:#4A90E2;">⚔️ 현재 삼세판 스코어 (2선승제) ⚔️</h4>
    <p style="font-size: 1.6rem; font-weight: bold; margin: 8px 0;">
        🐹 나: <span style="color:#FF6B9E;">{st.session_state.round_user}승</span> &nbsp; VS &nbsp; 
        🐰 먼작귀 친구들: <span style="color:#4A90E2;">{st.session_state.round_com}승</span>
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# 7. 게임 진행 여부 확인 (누군가 2승을 먼저 달성했는지 체크)
match_over = (
    st.session_state.round_user == 2 or st.session_state.round_com == 2
)


# 게임 로직 함수
def play_round(user_choice):
  choices = ["✌️ 가위", "✊ 바위", "✋ 보"]
  com_choice = random.choice(choices)

  # 승패 판정
  if user_choice == com_choice:
    outcome = "draw"
    st.session_state.total_draw += 1
    quote = random.choice(DRAW_QUOTES)
  elif (
      (user_choice == "✌️ 가위" and com_choice == "✋ 보")
      or (user_choice == "✊ 바위" and com_choice == "✌️ 가위")
      or (user_choice == "✋ 보" and com_choice == "✊ 바위")
  ):
    outcome = "win"
    st.session_state.total_win += 1
    st.session_state.round_user += 1
    quote = random.choice(WIN_QUOTES)
  else:
    outcome = "lose"
    st.session_state.total_lose += 1
    st.session_state.round_com += 1
    quote = random.choice(LOSE_QUOTES)

  st.session_state.last_result = {
      "user": user_choice,
      "com": com_choice,
      "outcome": outcome,
      "quote": quote,
  }


# 8. [✌️ 가위], [✊ 바위], [✋ 보] 버튼 3개 나란히 배치
if not match_over:
  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("✌️ 가위"):
      play_round("✌️ 가위")
      st.rerun()
  with col2:
    if st.button("✊ 바위"):
      play_round("✊ 바위")
      st.rerun()
  with col3:
    if st.button("✋ 보"):
      play_round("✋ 보")
      st.rerun()

# 9. 대결 결과 출력 영역
if st.session_state.last_result:
  res = st.session_state.last_result
  st.markdown("---")
  st.markdown(
      f"<h4 style='text-align:center;'>나: {res['user']} &nbsp;🆚&nbsp;"
      f" 먼작귀: {res['com']}</h4>",
      unsafe_allow_html=True,
  )

  # 라운드별 색깔 상자 & 축하 효과
  if res["outcome"] == "win":
    st.success("🎉 이번 라운드 승리! 정말 대단해요!")
    st.balloons()
  elif res["outcome"] == "lose":
    st.error("😭 이번 라운드 패배... 아쉽네요!")
  else:
    st.warning("🤝 무승부! 다시 한 번 승부해요!")

  # 먼작귀 유머러스 멘트 출력
  st.markdown(
      f'<div class="character-quote">{res["quote"]}</div>',
      unsafe_allow_html=True,
  )

# 10. 삼세판 최종 우승/패배 안내 및 다시 시작 버튼
if match_over:
  st.markdown("---")
  if st.session_state.round_user == 2:
    st.success(
        "🏆 **최종 승리!** 삼세판 승부에서 먼작귀 친구들을 이겼습니다! 🎊"
    )
    st.balloons()
  else:
    st.error(
        "💀 **최종 패배!** 먼작귀 친구들이 삼세판에서 먼저 2승을 가져갔습니다!"
    )

  if st.button("🔄 새로운 삼세판 시작하기"):
    st.session_state.round_user = 0
    st.session_state.round_com = 0
    st.session_state.last_result = None
    st.rerun()

# 11. 누적 승률 전적판 (하단)
st.markdown("---")
st.subheader("📊 누적 승률 전적판")

total_games = (
    st.session_state.total_win
    + st.session_state.total_lose
    + st.session_state.total_draw
)
win_rate = (
    (st.session_state.total_win / total_games * 100) if total_games > 0 else 0.0
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("🏆 승리", f"{st.session_state.total_win}회")
m2.metric("💧 패배", f"{st.session_state.total_lose}회")
m3.metric("🤝 무승부", f"{st.session_state.total_draw}회")
m4.metric("📈 승률", f"{win_rate:.1f}%")
