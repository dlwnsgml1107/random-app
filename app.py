import random
import streamlit as st

# 1. 세션 상태(session_state) 초기화: 버튼 클릭 후에도 점수와 전적을 기억하기 위함
if "total_wins" not in st.session_state:
    st.session_state.total_wins = 0
if "total_losses" not in st.session_state:
    st.session_state.total_losses = 0
if "total_draws" not in st.session_state:
    st.session_state.total_draws = 0

# 삼세판(3판 2선승제) 현재 매치 점수
if "match_user" not in st.session_state:
    st.session_state.match_user = 0
if "match_comp" not in st.session_state:
    st.session_state.match_comp = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False


def reset_match():
    """현재 삼세판 점수를 초기화하고 새 게임을 시작하는 함수"""
    st.session_state.match_user = 0
    st.session_state.match_comp = 0
    st.session_state.game_over = False


def reset_all():
    """누적 전적과 삼세판 점수를 모두 초기화하는 함수"""
    reset_match()
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.total_draws = 0


# 2. 상황별 유머러스한 멘트 목록
comp_lose_comments = [
    "앗, 이번엔 봐드린 겁니다! 😤",
    "우연일 뿐이에요... 다시 한 판 붙어요!",
    "제 알고리즘에 잠깐 버그가 났나 봐요 😱",
    "운이 좋으셨네요! 다음 판은 절대 안 집니다.",
]

comp_win_comments = [
    "조금 더 노력해보세요 ㅋㅋ 😎",
    "이 정도는 식은 죽 먹기죠~",
    "혹시 낼 거 미리 알려주신 건가요? ㅋㅋ",
    "AI의 승리입니다! 인간 시대의 끝이 도래했다 🤖",
]

draw_comments = [
    "찌찌뽕! 우리 꽤 잘 통하는데요? 👀",
    "막상막하의 승부군요!",
    "어라? 제 생각을 읽으셨나요?",
]

# 3. 화면 상단 제목 및 안내 문구
st.title("🎮 컴퓨터와 삼세판! 가위바위보 게임")
st.write(
    "먼저 **2승**을 달성하면 최종 승리하는 **삼세판(3판 2선승제)** 모드입니다!"
)

choices = ["✌️ 가위", "✊ 바위", "✋ 보"]
user_choice = None

# 4. 가위/바위/보 버튼 3개 나란히 배치 (삼세판이 끝나면 버튼 비활성화)
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

# 5. 대결 로직 및 결과 출력
if user_choice:
    computer_choice = random.choice(choices)

    st.divider()
    st.subheader(f"나: {user_choice}  🆚  컴퓨터: {computer_choice}")

    if user_choice == computer_choice:
        st.session_state.total_draws += 1
        comment = random.choice(draw_comments)
        st.warning(f"🤝 **비겼습니다!** — {comment}")

    elif (
        (user_choice == "✌️ 가위" and computer_choice == "✋ 보")
        or (user_choice == "✊ 바위" and computer_choice == "✌️ 가위")
        or (user_choice == "✋ 보" and computer_choice == "✊ 바위")
    ):
        st.session_state.total_wins += 1
        st.session_state.match_user += 1
        comment = random.choice(comp_lose_comments)
        st.success(f"🎉 **이겼습니다!** — {comment}")

    else:
        st.session_state.total_losses += 1
        st.session_state.match_comp += 1
        comment = random.choice(comp_win_comments)
        st.error(f"😭 **졌습니다!** — {comment}")

    # 6. 삼세판(3판 2선승제) 최종 승패 판정
    if st.session_state.match_user == 2:
        st.session_state.game_over = True
        st.balloons()
        st.success(
            "🏆 **최종 승리!** 삼세판에서 컴퓨터를 완벽하게 이겼습니다!"
        )
    elif st.session_state.match_comp == 2:
        st.session_state.game_over = True
        st.error("💀 **최종 패배...** 컴퓨터가 삼세판의 승자가 되었습니다!")

# 삼세판 종료 시 새 게임 버튼 표시
if st.session_state.game_over:
    st.button("🔄 새 삼세판 시작하기", on_click=reset_match, type="primary")

# 7. 현재 삼세판 현황 및 누적 승률 전적판
st.divider()
st.subheader("🔥 현재 삼세판 스코어 (2승 선취)")
m_col1, m_col2 = st.columns(2)
m_col1.metric("나의 승수", f"{st.session_state.match_user} 승")
m_col2.metric("컴퓨터 승수", f"{st.session_state.match_comp} 승")

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
s_col1.metric("승리", f"{st.session_state.total_wins}회")
s_col2.metric("패배", f"{st.session_state.total_losses}회")
s_col3.metric("무승부", f"{st.session_state.total_draws}회")
s_col4.metric("승률", f"{win_rate:.1f}%")

st.button("🗑️ 전체 전적 초기화", on_click=reset_all)
