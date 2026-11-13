import random
import streamlit as st

# 1. 화면 상단 제목 및 안내 문구
st.title("🎮 컴퓨터와 한판 승부! 가위바위보 게임")
st.write("아래 세 가지 버튼 중 하나를 눌러 컴퓨터와 대결해 보세요!")

# 선택지 목록
choices = ["✌️ 가위", "✊ 바위", "✋ 보"]
user_choice = None

# 2. 버튼 3개를 나란히 배치 (3개의 열 생성)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✌️ 가위", use_container_width=True):
        user_choice = "✌️ 가위"

with col2:
    if st.button("✊ 바위", use_container_width=True):
        user_choice = "✊ 바위"

with col3:
    if st.button("✋ 보", use_container_width=True):
        user_choice = "✋ 보"

# 3. 사용자가 버튼을 눌렀을 때 실행되는 대결 로직
if user_choice:
    computer_choice = random.choice(choices)

    st.divider()
    st.subheader(f"나: {user_choice}  🆚  컴퓨터: {computer_choice}")

    # 4. 승/패/무승부 판정 및 결과 표시
    if user_choice == computer_choice:
        st.warning("🤝 비겼습니다! 다시 한 번 도전해 보세요.")
    elif (
        (user_choice == "✌️ 가위" and computer_choice == "✋ 보")
        or (user_choice == "✊ 바위" and computer_choice == "✌️ 가위")
        or (user_choice == "✋ 보" and computer_choice == "✊ 바위")
    ):
        st.success("🎉 축하합니다! 당신이 이겼습니다!")
        st.balloons()
    else:
        st.error("😭 아쉽네요! 컴퓨터가 이겼습니다.")
