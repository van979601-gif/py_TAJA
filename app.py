import streamlit as st
from streamlit_ace import st_ace
import random
import time

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="🐍",
    layout="wide"
)

# -----------------------------
# 문제 데이터
# -----------------------------

BEGINNER = [
    "print('Hello World')",

    """for i in range(5):
    print(i)""",

    """x = 10
y = 20
print(x + y)"""
]

INTERMEDIATE = [
    """def add(a, b):
    return a + b

print(add(3, 5))""",

    """nums = [1, 2, 3]

squared = [n**2 for n in nums]

print(squared)"""
]

ADVANCED = [
    """class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"

p = Person("Tom")
print(p.greet())""",

    """def fibonacci(n):
    if n <= 1:
        return n

    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(6))"""
]

LEVELS = {
    "초급": BEGINNER,
    "중급": INTERMEDIATE,
    "고급": ADVANCED
}

# -----------------------------
# 세션 상태
# -----------------------------

if "target_code" not in st.session_state:
    st.session_state.target_code = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

# -----------------------------
# 제목
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

# -----------------------------
# 상단 설정
# -----------------------------

col_top1, col_top2 = st.columns(2)

with col_top1:
    user_name = st.text_input(
        "👤 이름",
        placeholder="이름 입력"
    )

with col_top2:
    difficulty = st.selectbox(
        "난이도",
        ["초급", "중급", "고급"]
    )

# -----------------------------
# 시작 버튼
# -----------------------------

if st.button("🚀 문제 시작"):

    if user_name.strip() == "":
        st.warning("이름을 입력하세요.")
        st.stop()

    st.session_state.target_code = random.choice(
        LEVELS[difficulty]
    )

    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.start_time = 0

# -----------------------------
# 문제 표시
# -----------------------------

if st.session_state.target_code:

    left, right = st.columns(2)

    # -----------------------------
    # 왼쪽 = 문제 코드
    # -----------------------------

    with left:

        st.subheader("📝 제시 코드")

        st.code(
            st.session_state.target_code,
            language="python"
        )

    # -----------------------------
    # 오른쪽 = 코드 입력창
    # -----------------------------

    with right:

        st.subheader("⌨️ 코드 입력")

        user_input = st_ace(
            placeholder="여기에 Python 코드를 입력하세요...",
            language="python",
            theme="monokai",
            keybinding="vscode",
            font_size=16,
            tab_size=4,
            show_gutter=True,
            wrap=True,
            auto_update=True,
            height=400
        )

    # -----------------------------
    # 타이머 시작
    # -----------------------------

    if user_input and not st.session_state.started:
        st.session_state.started = True
        st.session_state.start_time = time.time()

    # -----------------------------
    # 정확도 계산
    # -----------------------------

    if user_input:

        target = st.session_state.target_code

        correct = 0

        for a, b in zip(user_input, target):
            if a == b:
                correct += 1

        accuracy = (correct / len(target)) * 100

        st.progress(min(int(accuracy), 100))

        st.info(f"🎯 정확도: {accuracy:.1f}%")

    # -----------------------------
    # 정답 처리
    # -----------------------------

    if (
        user_input
        and user_input.strip()
        == st.session_state.target_code.strip()
        and not st.session_state.finished
    ):

        st.session_state.finished = True

        elapsed = time.time() - st.session_state.start_time

        chars = len(st.session_state.target_code)

        cpm = (chars / elapsed) * 60

        st.success(
            f"🎉 {user_name}님 성공!"
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "⏱️ 시간",
                f"{elapsed:.2f}초"
            )

        with c2:
            st.metric(
                "⚡ CPM",
                f"{cpm:.1f}"
            )
