import streamlit as st
import time
import random

st.set_page_config(
    page_title="타자 연습 앱",
    page_icon="⌨️",
    layout="centered"
)

# 연습 문장들
sentences = [
    "Python is a powerful programming language.",
    "Streamlit makes web apps easy to build.",
    "Practice typing every day to improve speed.",
    "GitHub is useful for version control.",
    "Coding becomes easier with consistent practice."
]

# 세션 상태 초기화
if "target_sentence" not in st.session_state:
    st.session_state.target_sentence = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("⌨️ 타자 연습 웹앱")

st.write("아래 문장을 최대한 빠르고 정확하게 입력하세요.")

# 목표 문장 출력
target = st.session_state.target_sentence

st.markdown(
    f"""
    <div style="
        padding:15px;
        border-radius:10px;
        background-color:#f0f2f6;
        font-size:22px;
        font-weight:bold;
    ">
    {target}
    </div>
    """,
    unsafe_allow_html=True
)

# 사용자 입력
user_input = st.text_input("여기에 입력하세요")

# 타이머 시작
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 결과 계산
if user_input == target and not st.session_state.finished:

    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time

    # 단어 수 계산
    words = len(target.split())

    # WPM 계산
    wpm = (words / elapsed_time) * 60

    # 정확도 계산
    correct_chars = sum(
        1 for a, b in zip(user_input, target) if a == b
    )

    accuracy = (correct_chars / len(target)) * 100

    st.session_state.finished = True

    st.success("완료!")

    st.metric("⌛ 걸린 시간", f"{elapsed_time:.2f} 초")
    st.metric("⚡ 타자 속도", f"{wpm:.2f} WPM")
    st.metric("🎯 정확도", f"{accuracy:.2f}%")

# 다시하기 버튼
if st.button("다시하기"):

    st.session_state.target_sentence = random.choice(sentences)
    st.session_state.start_time = None
    st.session_state.finished = False

    st.rerun()
