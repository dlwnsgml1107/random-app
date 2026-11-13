import random
import streamlit as st

# 앱 제목 및 안내 문구
st.title("🍱 오늘의 점심 메뉴 추천기")
st.write("버튼을 눌러 오늘 먹을 점심 메뉴를 랜덤으로 골라보세요!")

# 추천할 점심 메뉴 목록 (원하는 메뉴를 자유롭게 추가/수정하세요)
lunch_menus = [
    "김치찌개",
    "된장찌개",
    "제육볶음",
    "돈가스",
    "초밥",
    "짜장면",
    "짬뽕",
    "쌀국수",
    "파스타",
    "햄버거",
    "비빔밥",
    "순대국밥",
    "마라탕",
    "샌드위치",
]

# 버튼을 누르면 랜덤으로 메뉴 하나를 선택해 출력
if st.button("오늘 뭐 먹지? 🎲"):
    today_menu = random.choice(lunch_menus)
    st.success(f"오늘의 추천 메뉴는 **{today_menu}**입니다! 맛있게 드세요 😋")
