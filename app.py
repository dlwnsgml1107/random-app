
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullFormatter

# ------------------------------------------------------------
# 1. 화면 설정 및 디자인
# ------------------------------------------------------------

st.set_page_config(
    page_title="RC Filter Analyzer",
    page_icon="🔌",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

h1 {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.3rem !important;
}

h2 {
    font-size: 1.25rem !important;
    font-weight: 650 !important;
}

h3 {
    font-size: 1.05rem !important;
}

p, label, .stMarkdown {
    font-size: 0.88rem;
}

.stCaption {
    font-size: 0.75rem;
}

[data-testid="stMetric"] {
    background-color: rgba(128, 128, 128, 0.07);
    padding: 12px 15px;
    border-radius: 10px;
    border: 1px solid rgba(128, 128, 128, 0.15);
}

[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
    font-weight: 650;
}

.stNumberInput, .stSelectbox {
    margin-bottom: 0.35rem;
}

.stButton button,
.stDownloadButton button {
    border-radius: 8px;
    font-size: 0.85rem;
}

hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] {
    min-width: 270px;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# 2. 회로 계산 함수
# ------------------------------------------------------------

def cutoff_frequency(resistance_ohm, capacitance_f):

    if resistance_ohm <= 0 or capacitance_f <= 0:
        raise ValueError("저항과 커패시터 값은 0보다 커야 합니다.")

    return 1.0 / (2.0 * np.pi * resistance_ohm * capacitance_f)


def calculate_response(filter_type, frequencies_hz,
                       resistance_ohm, capacitance_f):

    frequencies = np.asarray(frequencies_hz, dtype=float)

    if resistance_ohm <= 0 or capacitance_f <= 0:
        raise ValueError("저항과 커패시터 값은 0보다 커야 합니다.")

    if np.any(frequencies <= 0):
        raise ValueError("주파수는 0보다 커야 합니다.")

    x = 2.0 * np.pi * frequencies * resistance_ohm * capacitance_f

    # 선택구조
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
# 3. 반복문과 리스트를 이용한 출력 전압 계산
# ------------------------------------------------------------

def calculate_output_voltages(input_voltage, gains):

    output_voltage_list = []

    # 반복구조
    for i in range(len(gains)):

        output_voltage = input_voltage * float(gains[i])

        # 리스트에 결과 저장
        output_voltage_list.append(output_voltage)

    return output_voltage_list


# ------------------------------------------------------------
# 4. 자동 검증 함수
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
# 5. 메인 화면
# ------------------------------------------------------------

st.title("🔌 전자 필터 설계 및 주파수 응답 분석기")

st.caption("RC Filter Design & Frequency Response Analyzer")

st.write(
    "저항과 커패시터 값을 입력하면 RC 필터의 차단 주파수, "
    "출력 전압, 전압 이득 및 위상 변화를 분석합니다."
)

st.divider()


# ------------------------------------------------------------
# 6. 프로그램 목적 및 작동 원리 설명
# ------------------------------------------------------------

with st.expander("📖 프로그램의 목적과 작동 원리 알아보기", expanded=False):

    st.markdown("""
    ### ① 프로그램의 목적

    이 프로그램은 저항(R)과 커패시터(C)로 구성된 RC 필터의
    전기적 특성을 분석하고 설계하는 것을 목적으로 합니다.

    사용자가 저항과 커패시터의 값을 입력하면 차단 주파수를 계산하고,
    주파수 변화에 따라 출력 전압과 전압 이득, 위상차가
    어떻게 달라지는지 그래프와 표로 확인할 수 있습니다.

    또한 원하는 차단 주파수를 설정하면 필요한 저항값을
    역으로 계산하여 회로 설계에 활용할 수 있습니다.

    ---

    ### ② RC 필터의 작동 원리

    RC 필터는 저항(R)과 커패시터(C)를 이용하여
    입력 신호의 주파수에 따라 출력 신호의 크기를 조절하는 회로입니다.

    커패시터는 주파수에 따라 교류 신호에 대한 저항 성분인
    용량 리액턴스가 달라집니다.

    주파수가 높아질수록 용량 리액턴스는 작아지고,
    주파수가 낮아질수록 용량 리액턴스는 커집니다.

    이러한 특성을 이용하면 특정 주파수 영역의 신호를
    통과시키거나 약하게 만들 수 있습니다.

    **저역통과 필터**

    낮은 주파수의 신호는 잘 통과시키고,
    높은 주파수의 신호는 약하게 만듭니다.

    **고역통과 필터**

    높은 주파수의 신호는 잘 통과시키고,
    낮은 주파수의 신호는 약하게 만듭니다.

    ---

    ### ③ 차단 주파수의 계산 원리

    RC 필터의 차단 주파수는 다음 공식으로 계산합니다.

    \[
    f_c = \frac{1}{2\pi RC}
    \]

    - R: 저항값(Ω)
    - C: 커패시터의 정전용량(F)
    - fc: 차단 주파수(Hz)

    저항이나 커패시터의 값이 커지면 차단 주파수는 낮아지고,
    두 값이 작아지면 차단 주파수는 높아집니다.

    차단 주파수에서 출력 전압의 크기는 입력 전압의 약 70.7%가 됩니다.

    ---

    ### ④ 프로그램의 분석 과정

    1. 사용자가 필터 종류, 저항, 커패시터, 입력 전압을 설정합니다.
    2. 입력된 저항과 커패시터 값으로 차단 주파수를 계산합니다.
    3. 설정한 주파수 범위에서 각 주파수의 전압 이득과 위상차를 계산합니다.
    4. 전압 이득을 입력 전압에 곱하여 출력 전압을 구합니다.
    5. 계산 결과를 그래프와 표로 표시하고 CSV 파일로 저장할 수 있습니다.

    ---

    **활용 목적**

    이 프로그램을 통해 저항과 커패시터의 변화가 필터의 특성에
    어떤 영향을 주는지 직접 확인하고,
    RC 회로의 주파수 응답 원리를 이해할 수 있습니다.
    """)


# ------------------------------------------------------------
# 7. 용어 설명
# ------------------------------------------------------------

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if st.button("📘 전자 필터 용어 설명 보기 / 닫기"):

    st.session_state.show_explanation = not st.session_state.show_explanation

if st.session_state.show_explanation:

    with st.container(border=True):

        st.subheader("프로그램에 사용되는 기본 용어")

        st.markdown("""
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
# 8. 사용자 입력
# ------------------------------------------------------------

st.sidebar.header("⚙️ 회로 및 분석 조건")

filter_type = st.sidebar.selectbox(
    "필터 종류",
    ["저역통과", "고역통과"]
)

# 모든 숫자 입력의 증가 및 감소 간격을 1로 설정

resistance_kohm = st.sidebar.number_input(
    "저항값 R (kΩ)",
    min_value=0.001,
    max_value=10000.0,
    value=1.0,
    step=1.0
)

capacitance_uf = st.sidebar.number_input(
    "커패시터값 C (μF)",
    min_value=0.001,
    max_value=100000.0,
    value=1.0,
    step=1.0
)

input_voltage = st.sidebar.number_input(
    "입력 전압 크기 (V)",
    min_value=0.001,
    max_value=100000.0,
    value=5.0,
    step=1.0
)

st.sidebar.divider()

st.sidebar.subheader("주파수 분석")

start_frequency = st.sidebar.number_input(
    "분석 시작 주파수 (Hz)",
    min_value=0.001,
    max_value=1e9,
    value=10.0,
    step=1.0
)

end_frequency = st.sidebar.number_input(
    "분석 종료 주파수 (Hz)",
    min_value=0.002,
    max_value=1e12,
    value=100000.0,
    step=1.0
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
    value=1000.0,
    step=1.0
)


# ------------------------------------------------------------
# 9. 계산 및 입력값 검증
# ------------------------------------------------------------

r_ohm = resistance_kohm * 1000.0
c_f = capacitance_uf * 1e-6

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
# 10. 리스트와 반복문을 이용한 데이터 처리
# ------------------------------------------------------------

frequency_list = frequencies.tolist()
gain_list = gain.tolist()
gain_db_list = gain_db.tolist()
phase_list = phase_deg.tolist()

output_voltage_list = calculate_output_voltages(
    input_voltage,
    gain_list
)


# ------------------------------------------------------------
# 11. 계산 결과
# ------------------------------------------------------------

st.subheader("📊 분석 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "차단 주파수",
    f"{fc:,.2f} Hz"
)

col2.metric(
    "전압 이득",
    f"{float(point_gain[0]):.4f} 배"
)

col3.metric(
    "위상차",
    f"{float(point_phase[0]):.2f}°"
)

output_voltage = input_voltage * float(point_gain[0])

st.metric(
    f"{test_frequency:,.2f} Hz에서의 출력 전압",
    f"{output_voltage:.4f} V"
)

st.caption(
    f"저항 = {r_ohm:,.2f} Ω  |  "
    f"커패시터 = {c_f:.8g} F  |  "
    f"입력 전압 = {input_voltage:g} V"
)

st.divider()


# ------------------------------------------------------------
# 12. 주파수 응답 그래프
# ------------------------------------------------------------

st.subheader("📈 주파수 응답 분석")

graph_col1, graph_col2 = st.columns(2)


# 전압 이득 그래프

with graph_col1:

    st.markdown("**① 주파수에 따른 전압 이득**")

    fig1, ax1 = plt.subplots(figsize=(5.2, 2.7), dpi=100)

    ax1.semilogx(
        frequency_list,
        gain_db_list,
        linewidth=1.8,
        label="Gain"
    )

    # 로그 축의 눈금을 수학 기호가 아닌 일반 숫자로 표시
    ax1.xaxis.set_major_formatter(
        FuncFormatter(lambda value, position: f"{value:,.0f}")
    )
    ax1.xaxis.set_minor_formatter(NullFormatter())

    ax1.axvline(
        fc,
        linestyle="--",
        linewidth=1,
        label="Cutoff"
    )

    ax1.axhline(
        -3.0103,
        linestyle=":",
        linewidth=1,
        label="-3.01 dB"
    )

    ax1.set_xlabel("Frequency (Hz)", fontsize=8)
    ax1.set_ylabel("Gain (dB)", fontsize=8)
    ax1.set_title(f"{filter_type} filter", fontsize=10)

    ax1.tick_params(labelsize=7)
    ax1.grid(True, which="both", alpha=0.25)
    ax1.legend(fontsize=7, loc="best")

    fig1.tight_layout()

    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)


# 위상차 그래프

with graph_col2:

    st.markdown("**② 주파수에 따른 위상 변화**")

    fig2, ax2 = plt.subplots(figsize=(5.2, 2.7), dpi=100)

    ax2.semilogx(
        frequency_list,
        phase_list,
        linewidth=1.8,
        label="Phase"
    )

    # 로그 축의 눈금을 수학 기호가 아닌 일반 숫자로 표시
    ax2.xaxis.set_major_formatter(
        FuncFormatter(lambda value, position: f"{value:,.0f}")
    )
    ax2.xaxis.set_minor_formatter(NullFormatter())

    ax2.axvline(
        fc,
        linestyle="--",
        linewidth=1,
        label="Cutoff"
    )

    ax2.set_xlabel("Frequency (Hz)", fontsize=8)
    ax2.set_ylabel("Phase (degrees)", fontsize=8)

    ax2.set_title(f"{filter_type} filter", fontsize=10)

    ax2.tick_params(labelsize=7)
    ax2.grid(True, which="both", alpha=0.25)
    ax2.legend(fontsize=7, loc="best")

    fig2.tight_layout()

    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


st.divider()


# ------------------------------------------------------------
# 13. 계산 데이터 및 CSV 다운로드
# ------------------------------------------------------------

st.subheader("📋 계산 데이터")

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
    hide_index=True,
    height=250
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


st.divider()


# ------------------------------------------------------------
# 14. 설계 역산 기능
# ------------------------------------------------------------

st.subheader("④ 설계 역산 기능")

st.write(
    "원하는 차단 주파수에 맞는 저항값을 계산합니다."
)

target_fc = st.number_input(
    "목표 차단 주파수 (Hz)",
    min_value=0.001,
    max_value=1e9,
    value=1000.0,
    step=1.0
)

required_r = 1.0 / (2.0 * np.pi * target_fc * c_f)

st.success(
    f"현재 커패시터값 {capacitance_uf:g} μF를 유지한다면 "
    f"필요한 저항은 {required_r:,.2f} Ω "
    f"({required_r/1000:.4f} kΩ) 입니다."
)


st.divider()


# ------------------------------------------------------------
# 15. 자동 검증
# ------------------------------------------------------------

with st.expander("🔍 계산 공식 자동 검증 결과 보기"):

    try:

        run_self_tests()

        st.success(
            "검증 통과! 차단 주파수, 전압 이득, "
            "위상차 계산이 이론값과 일치합니다."
        )

    except AssertionError:

        st.error("검증 실패: 계산 공식을 확인해야 합니다.")


# ------------------------------------------------------------
# 16. 하단 안내
# ------------------------------------------------------------

st.divider()

st.caption(
    "교육용 시뮬레이터입니다. 실제 회로 제작 전에는 "
    "부품의 허용오차와 정격을 확인해야 합니다."
)
