import streamlit as st
import random
import time

# HTML, CSS를 활용한 커스텀 스타일 및 애니메이션
st.markdown(
    """
    <style>
    /* 전체 컨테이너를 가운데 정렬 */
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* 반짝이는 효과를 위한 애니메이션 */
    @keyframes sparkle {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    
    /* 반짝이는 제목 스타일 */
    .sparkle {
        font-size: 2.5em;
        font-weight: bold;
        color: #ffcc00;
        text-align: center;
        animation: sparkle 1s infinite;
    }

    /* 커스텀 버튼 스타일 */
    .custom-button {
        padding: 10px 20px;
        margin: 20px 0;
        font-size: 1.5em;
        color: #ff0000;
        border: 2px solid #ff0000;
        border-radius: 10px;
        background-color: transparent;
        cursor: pointer;
        text-align: center;
    }

    .custom-button:hover {
        background-color: #ffcccc;
    }

    /* 행운의 번호 스타일 */
    .lucky-number {
        font-size: 1.5em;
        color: purple;
        margin-top: 10px;
    }

    /* 번호 스타일 */
    .number {
        font-size: 1.5em;
        color: green;
    }

    /* 간단한 페이드 인 애니메이션 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 중앙 정렬을 위한 컨테이너
st.markdown('<div class="center-container">', unsafe_allow_html=True)

# 반짝이는 제목
st.markdown('<div class="sparkle">✨ 로또 번호 생성기 ✨</div>', unsafe_allow_html=True)

# 로또 번호 생성 함수
def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

# 로또 번호 생성 버튼
if st.button('로또 번호 생성'):
    st.write('생성된 로또 번호:')
    for i in range(5):
        lotto_numbers = generate_lotto_numbers()
        # 순차적 출력과 애니메이션 효과 추가
        st.markdown(f'<div class="lucky-number fade-in">행운의 번호 {i + 1}: <span class="number">{lotto_numbers}</span></div>', unsafe_allow_html=True)
        # 출력 딜레이 추가
        time.sleep(0.5)

# 중앙 정렬 컨테이너 닫기
st.markdown('</div>', unsafe_allow_html=True)
