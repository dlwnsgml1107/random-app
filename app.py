
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. 회로 계산 함수
# ------------------------------------------------------------

def cutoff_frequency(resistance_ohm, capacitance_f):
    """차단 주파수 계산"""
    if resistance_ohm <= 0 or capacitance_f <= 0:
        raise ValueError("저항과 커패시터 값은 0보다 커야 합니다.")

    return 1.0 / (2.0 * np.pi * resistance_ohm * capacitance_f)


def calculate_response(filter_type, frequencies_hz,
                       resistance_ohm, capacitance_f):
    """전압 이득과 위상차 계산"""

    frequencies = np.asarray(frequencies_hz, dtype=float)

    if resistance_ohm <= 0 or capacitance_f <= 0:
        raise ValueError("저항과 커패시터 값은 0보다 커야 합니다.")

    if np.any(frequencies <= 0):
        raise ValueError("주파수는 0보다 커야 합니다.")

    x = 2.0 * np.pi * frequencies * resistance_ohm * capacitance_f

    # 선택구조: 필터 종류에 따른 계산
    if filter_type == "저역통과":
        gain = 1.0 / np.sqrt(1.0 + x**2)
        phase_deg = -np.degrees(np.arctan(x))

    elif filter_type == "고역통과":
        gain = x / np.sqrt(1.0 + x**2)
        phase_deg = np.degrees(np.arctan2(1.0, x))

    else:
        raise ValueError("지원하지 않는 필터입니다.")

    gain_db = 20.0 * np.log10(np.maximum(gain, 1e-15))

    return gain, gain_db, phase_deg


# ------------------------------------------------------------
# 2. 반복구조와 리스트를 이용한 출력 전압 계산 함수
# ------------------------------------------------------------

def calculate_output_voltages(input_voltage, gains):
    """for문과 리스트를 이용하여 출력 전압 계산"""

    output_voltage_list = []

    # 반복구조: 각 주파수의 전압 이득을 순서대로 계산
    for i in range(len(gains)):
        output_voltage = input_voltage * float(gains[i])

        # 리스트에 계산 결과 추가
        output_voltage_list.append(output_voltage)

    return output_voltage_list


# ------------------------------------------------------------
# 3. 자동 검증 함수
# ------------------------------------------------------------

def run_self_tests():

    r = 1000.0
    c = 1e-6

    fc = cutoff_frequency(r, c)

    lp_gain, _, lp_phase = calculate_response(
        "저역통과", [fc], r, c
    )

    hp_gain, _, hp_phase = calculate_response(
        "고역통과", [fc], r, c
    )

    assert abs(float(lp_gain[0]) - 1 / np.sqrt(2)) < 1e-10
    assert abs(float(hp_gain[0]) - 1 / np.sqrt(2)) < 1e-10

    assert abs(float(lp_phase[0]) + 45.0) < 1e-8
    assert abs(float(hp_phase[0]) - 45.0) < 1e-8

    return True


# ------------------------------------------------------------
# 4. Streamlit 화면 설정
# ------------------------------------------------------------

st.set_page_config(
    page_title="전자 필터 설계 및 분석기",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 전자 필터 설계 및 주파수 응답 분석기")

st.write(
    "저항과 커패시터 값을 입력하면 RC 필터의 차단 주파수, "
    "출력 전압, 전압 이득 및 위상 변화를 분석합니다."
)


# ------------------------------------------------------------
# 5. 용어 설명
# ------------------------------------------------------------

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if st.button("📘 전자 필터 용어 설명 보기 / 닫기"):
    st.session_state.show_explanation = not st.session_state.show_explanation

if st.session_state.show_explanation:

    with st.container(border=True):

        st.subheader("프로그램에 사용되는 기본 용어")

        st.markdown(r"""
        **저항(R)**

        전류의 흐름을 제한하는 전자 부품입니다. 단위는 옴(Ω)입니다.

        **커패시터(C)**

        전기 에너지를 전기장 형태로 저장하고 방출하는 부품입니다.
        단위는 패럿(F)입니다.

        **주파수(Hz)**

        전기 신호가 1초 동안 반복되는 횟수입니다.

        **전자 필터**

        특정 주파수의 신호는 통과시키고 다른 주파수의 신호는 약하게 만드는 회로입니다.

        **저역통과 필터**

        낮은 주파수는 잘 통과시키고 높은 주파수는 약하게 만듭니다.

        **고역통과 필터**

        높은 주파수는 잘 통과시키고 낮은 주파수는 약하게 만듭니다.

        **차단 주파수**

        출력 전압의 크기가 입력 전압의 약 70.7%가 되는 기준 주파수입니다.

        **전압 이득**

        출력 전압을 입력 전압으로 나눈 값입니다.

        **위상차**

        입력 신호와 출력 신호의 시간상 차이를 각도로 나타낸 값입니다.

        **차단 주파수 공식**

        \[
        f_c = \frac{1}{2\pi RC}
        \]
        """)


st.info(
    "이 프로그램은 이상적인 1차 RC 저역통과·고역통과 필터를 분석합니다."
)


# ------------------------------------------------------------
# 6. 사용자 입력
# ------------------------------------------------------------

st.sidebar.header("회로 및 분석 조건 입력")

filter_type = st.sidebar.selectbox(
    "필터 종류",
    ["저역통과", "고역통과"]
)

resistance_kohm = st.sidebar.number_input(
    "저항값 R (kΩ)",
    min_value=0.001,
    max_value=10000.0,
    value=1.0,
    step=0.1
)

capacitance_uf = st.sidebar.number_input(
    "커패시터값 C (μF)",
    min_value=0.001,
    max_value=100000.0,
    value=1.0,
    step=0.1
)

input_voltage = st.sidebar.number_input(
    "입력 전압 크기 (V)",
    min_value=0.001,
    max_value=100000.0,
    value=5.0
)

start_frequency = st.sidebar.number_input(
    "분석 시작 주파수 (Hz)",
    min_value=0.001,
    max_value=1e9,
    value=10.0
)

end_frequency = st.sidebar.number_input(
    "분석 종료 주파수 (Hz)",
    min_value=0.002,
    max_value=1e12,
    value=100000.0
)

number_of_points = st.sidebar.slider(
    "그래프 계산 지점 수",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)

test_frequency = st.sidebar.number_input(
    "별도로 확인할 주파수 (Hz)",
    min_value=0.001,
    max_value=1e12,
    value=1000.0
)


# ------------------------------------------------------------
# 7. 입력값 검증 및 계산
# ------------------------------------------------------------

r_ohm = resistance_kohm * 1000.0
c_f = capacitance_uf * 1e-6

# 선택구조: 입력값 확인
if end_frequency <= start_frequency:

    st.error("종료 주파수는 시작 주파수보다 커야 합니다.")
    st.stop()

else:

    try:

        fc = cutoff_frequency(r_ohm, c_f)

        frequencies = np.logspace(
            np.log10(start_frequency),
            np.log10(end_frequency),
            number_of_points
        )

        gain, gain_db, phase_deg = calculate_response(
            filter_type,
            frequencies,
            r_ohm,
            c_f
        )

        point_gain, point_gain_db, point_phase = calculate_response(
            filter_type,
            [test_frequency],
            r_ohm,
            c_f
        )

    except ValueError as error:

        st.error(f"계산 오류: {error}")
        st.stop()


# ------------------------------------------------------------
# 8. 리스트와 반복문을 이용한 데이터 처리
# ------------------------------------------------------------

# NumPy 배열을 파이썬 리스트로 변환
frequency_list = frequencies.tolist()
gain_list = gain.tolist()
gain_db_list = gain_db.tolist()
phase_list = phase_deg.tolist()

# for문과 리스트를 이용한 출력 전압 계산
output_voltage_list = calculate_output_voltages(
    input_voltage,
    gain_list
)


# ------------------------------------------------------------
# 9. 계산 결과 표시
# ------------------------------------------------------------

st.header("계산 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "차단 주파수",
    f"{fc:,.2f} Hz"
)

col2.metric(
    "확인 주파수의 전압 이득",
    f"{float(point_gain[0]):.4f} 배"
)

col3.metric(
    "확인 주파수의 위상차",
    f"{float(point_phase[0]):.2f}°"
)

output_voltage = input_voltage * float(point_gain[0])

st.metric(
    f"{test_frequency:,.2f} Hz에서의 출력 전압",
    f"{output_voltage:.4f} V"
)

st.caption(
    f"저항 = {r_ohm:,.2f} Ω / "
    f"커패시터 = {c_f:.8g} F"
)


# ------------------------------------------------------------
# 10. 주파수에 따른 전압 이득 그래프
# ------------------------------------------------------------

st.subheader("① 주파수에 따른 전압 이득")

fig1, ax1 = plt.subplots(figsize=(9, 4))

ax1.semilogx(frequency_list, gain_db_list)

ax1.axvline(
    fc,
    linestyle="--",
    label=f"Cutoff = {fc:.2f} Hz"
)

ax1.axhline(
    -3.0103,
    linestyle=":",
    label="-3.01 dB"
)

ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Voltage gain (dB)")
ax1.set_title(f"{filter_type} filter frequency response")
ax1.grid(True, which="both", alpha=0.3)
ax1.legend()

st.pyplot(fig1)
plt.close(fig1)


# ------------------------------------------------------------
# 11. 주파수에 따른 위상 변화 그래프
# ------------------------------------------------------------

st.subheader("② 주파수에 따른 위상 변화")

fig2, ax2 = plt.subplots(figsize=(9, 4))

ax2.semilogx(frequency_list, phase_list)

ax2.axvline(
    fc,
    linestyle="--",
    label=f"Cutoff = {fc:.2f} Hz"
)

ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Phase difference (degrees)")
ax2.set_title(f"{filter_type} filter phase response")
ax2.grid(True, which="both", alpha=0.3)
ax2.legend()

st.pyplot(fig2)
plt.close(fig2)


# ------------------------------------------------------------
# 12. 계산 데이터 표 및 CSV 다운로드
# ------------------------------------------------------------

st.subheader("③ 계산 데이터")

result_df = pd.DataFrame({

    "주파수(Hz)": frequency_list,
    "전압 이득(배)": gain_list,
    "전압 이득(dB)": gain_db_list,
    "위상차(도)": phase_list,
    "출력 전압(V)": output_voltage_list

})

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)

csv_data = result_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "📥 분석 결과 CSV 다운로드",
    data=csv_data,
    file_name="rc_filter_analysis.csv",
    mime="text/csv"
)


# ------------------------------------------------------------
# 13. 원하는 차단 주파수에 맞는 저항값 계산
# ------------------------------------------------------------

st.subheader("④ 설계 역산 기능")

target_fc = st.number_input(
    "목표 차단 주파수 (Hz)",
    min_value=0.001,
    max_value=1e9,
    value=1000.0
)

required_r = 1.0 / (2.0 * np.pi * target_fc * c_f)

st.write(
    f"현재 커패시터값 {capacitance_uf:g} μF를 유지한다면 "
    f"필요한 저항은 **{required_r:,.2f} Ω "
    f"({required_r/1000:.4f} kΩ)** 입니다."
)


# ------------------------------------------------------------
# 14. 자동 검증
# ------------------------------------------------------------

with st.expander("계산 공식 자동 검증 결과 보기"):

    try:

        run_self_tests()

        st.success(
            "검증 통과! 차단 주파수, 전압 이득, "
            "위상차 계산이 이론값과 일치합니다."
        )

    except AssertionError:

        st.error("검증 실패: 계산 공식을 확인해야 합니다.")


st.caption(
    "교육용 시뮬레이터입니다. 실제 회로 제작 전에는 "
    "부품의 허용오차와 정격을 확인해야 합니다."
)
